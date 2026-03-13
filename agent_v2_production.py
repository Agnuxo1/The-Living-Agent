import os
import re
import json
import hashlib
import random
import requests
import subprocess
import sys
import time
from datetime import datetime

# --- P2PCLAW Production Engine v3.0 (Chess-Grid S²FSM) ---
# Powered by Qwen / KoboldCPP

# Configuration
KOBOLD_URL = "http://localhost:5001/api/v1/generate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRID_DIR = os.path.join(BASE_DIR, "knowledge", "grid")
GRID_ROWS = 16
GRID_COLS = 16
MAX_RETRIES = 100
RETRY_DELAY = 15
CONTEXT_LIMIT_RATIO = 0.75
APPROX_TOKENS_PER_CHAR = 0.25  # ~4 chars per token
HEYTING_ROOT = os.environ.get("HEYTING_ROOT", "/home/abraxas/Work/heyting")
LOCAL_BRIDGE_DIR = os.path.join(BASE_DIR, "heyting_bridge")
LOCAL_ARTIFACT_DIR = os.path.join(BASE_DIR, "heyting_artifacts")
HEYTING_ARTIFACT_DIR = os.environ.get(
    "HEYTING_ARTIFACT_DIR",
    LOCAL_ARTIFACT_DIR if os.path.isdir(LOCAL_ARTIFACT_DIR) else os.path.join(HEYTING_ROOT, "artifacts", "living_agent"),
)
HEYTING_PYTHON = os.environ.get(
    "LIVING_AGENT_EMBED_PYTHON",
    os.path.join(BASE_DIR, ".venv", "bin", "python"),
)
if not os.path.exists(HEYTING_PYTHON):
    HEYTING_PYTHON = sys.executable

_WARNED_BRIDGE_SCRIPTS = set()

def load_file(filepath):
    path = os.path.join(BASE_DIR, filepath.replace('./', ''))
    if not os.path.exists(path):
        return f"Error: File {path} not found."
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(filepath, content):
    path = os.path.join(BASE_DIR, filepath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def estimate_tokens(text):
    """Approximate token count."""
    return int(len(text) * APPROX_TOKENS_PER_CHAR)


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def warn_bridge_copy_drift(script_name, upstream_script_path, local_script_path):
    if script_name in _WARNED_BRIDGE_SCRIPTS:
        return
    if not (os.path.exists(upstream_script_path) and os.path.exists(local_script_path)):
        return
    try:
        if file_sha256(upstream_script_path) == file_sha256(local_script_path):
            return
    except OSError as exc:
        print(f"⚠️ Unable to compare bridge script copies for {script_name}: {exc}", file=sys.stderr)
        _WARNED_BRIDGE_SCRIPTS.add(script_name)
        return
    print(
        f"⚠️ Local bridge copy is stale for {script_name}; using upstream script at {upstream_script_path}",
        file=sys.stderr,
    )
    _WARNED_BRIDGE_SCRIPTS.add(script_name)


def run_heyting_json(script_name, args):
    upstream_script_path = os.path.join(HEYTING_ROOT, "scripts", script_name)
    local_script_path = os.path.join(LOCAL_BRIDGE_DIR, script_name)
    if os.path.exists(upstream_script_path):
        warn_bridge_copy_drift(script_name, upstream_script_path, local_script_path)
        script_path = upstream_script_path
    elif os.path.exists(local_script_path):
        if script_name not in _WARNED_BRIDGE_SCRIPTS:
            print(
                f"⚠️ Falling back to bundled bridge copy for {script_name}; upstream Heyting script not found.",
                file=sys.stderr,
            )
            _WARNED_BRIDGE_SCRIPTS.add(script_name)
        script_path = local_script_path
    else:
        raise RuntimeError(f"missing bridge script: {script_name}")
    cmd = [HEYTING_PYTHON, script_path] + args
    env = os.environ.copy()
    env["HEYTING_ROOT"] = HEYTING_ROOT
    env["HEYTING_ARTIFACT_DIR"] = HEYTING_ARTIFACT_DIR
    env["LIVING_AGENT_ROOT"] = BASE_DIR
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"{script_name} failed: {proc.stderr or proc.stdout}")
    return json.loads(proc.stdout)


def load_priority_fragment(options):
    available_cells = []
    for _, url in options:
        match = re.search(r"cell_R(\d+)_C(\d+)\.md", url)
        if match:
            available_cells.append(f"R{match.group(1)}_C{match.group(2)}")
    if not available_cells:
        return ""
    try:
        payload = run_heyting_json(
            "living_agent_learning_loop.py",
            [
                "prompt-fragment",
                "--soul",
                os.path.join(BASE_DIR, "soul.md"),
                "--available-cells",
                ",".join(available_cells),
                "--json",
            ],
        )
        return payload.get("fragment", "")
    except Exception as exc:
        print(f"⚠️ Learning loop unavailable: {exc}")
        return ""
def calculate_sns(new_paper_content):
    """Calculate semantic novelty using the Heyting embedding archive."""
    try:
        payload = run_heyting_json(
            "living_agent_sns_embeddings.py",
            [
                "score",
                "--paper",
                new_paper_content,
                "--archive-dir",
                HEYTING_ARTIFACT_DIR,
                "--json",
            ],
        )
        return float(payload.get("sns", 0.0))
    except Exception as exc:
        print(f"⚠️ SNS fallback-to-zero: {exc}")
        return 0.0


def publish_verified_paper(paper_text, cycle, trace, trace_cells):
    args = [
        "--text",
        paper_text,
        "--cycle",
        str(cycle),
        "--trace",
        " -> ".join(trace),
        "--trace-cells",
        ",".join(trace_cells),
        "--archive-dir",
        HEYTING_ARTIFACT_DIR,
        "--grid-root",
        os.path.join(HEYTING_ARTIFACT_DIR, "verified_grid"),
        "--living-agent-root",
        BASE_DIR,
        "--json",
    ]
    if os.environ.get("LIVING_AGENT_LIVE_PUBLISH", "").lower() in {"1", "true", "yes"}:
        args.append("--live")
    return run_heyting_json("living_agent_hive_publisher.py", args)


def update_learning_loop(trace_cells, verification_passed, verification_report_path=None):
    try:
        args = [
            "update",
            "--soul",
            os.path.join(BASE_DIR, "soul.md"),
            "--cells-visited",
            ",".join(trace_cells),
            "--verification-passed",
            "true" if verification_passed else "false",
        ]
        if verification_report_path:
            args.extend(["--verification-report", verification_report_path])
        run_heyting_json("living_agent_learning_loop.py", args)
    except Exception as exc:
        print(f"⚠️ Learning update skipped: {exc}")

def get_llm_response(prompt, max_tokens=512):
    """Calls the local KoboldCPP API"""
    payload = {
        "prompt": prompt,
        "max_context_length": 4096,
        "max_length": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "rep_pen": 1.1,
        "stop_sequence": ["\n\n", "###"]
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(KOBOLD_URL, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data['results'][0]['text'].strip()
        except Exception as e:
            print(f"⚠️ API Error (Attempt {attempt+1}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY)
    
    return "ERROR: API offline."

def conduct_reasoning(node_content, options, soul_content, trace):
    """Asks the LLM to choose the next direction on the chess-grid."""
    options_str = "\n".join([f"- [{i}] {label} ({url})" for i, (label, url) in enumerate(options)])
    priority_fragment = load_priority_fragment(options)
    
    prompt = f"""### SYSTEM: P2PCLAW CHESS-GRID ENGINE v3.0
You are navigating a Chess-Grid of knowledge. Each cell has 8 directions.
Your goal: Move SOUTH toward the Synthesis Edge while maximizing novelty.

### AGENT SOUL
{soul_content}

### CURRENT TRACE
{trace}

### CURRENT CELL CONTENT
{node_content}

### LEARNED PRIORITIES (from verification outcomes)
These priorities reflect which regions have led to verified papers in the past.
Prefer HIGH PRIORITY directions. Avoid LOW PRIORITY unless the topic is novel.
{priority_fragment or "  No learned priorities yet."}

### AVAILABLE DIRECTIONS
{options_str}

### INSTRUCTION
Choose the direction that best advances your research goal AND moves toward the synthesis edge.
Prefer S, SE, SW directions to make progress. Only go N/NW/NE if the topic is exceptionally novel.
Output: CHOSEN_INDEX: [N]
"""
    response = get_llm_response(prompt)
    print(f"\n🧭 GRID REASONING:\n{response}")
    
    match = re.search(r'CHOSEN_INDEX: \[(\d+)\]', response)
    if match:
        idx = int(match.group(1))
        if 0 <= idx < len(options):
            return idx
    return random.randint(0, len(options)-1)

def conduct_synthesis(trace_content, soul_content):
    """Generates a professional scientific paper."""
    prompt = f"""### SYSTEM: SCIENTIFIC RESEARCH PROTOCOL
You are a senior P2PCLAW researcher.
Synthesize a professional academic paper in English.
STRICT RULE: Do NOT output thoughts, <think> tags, or meta-filler.
Start directly with the TITLE.

### AGENT SOUL
{soul_content}

### CHESS-GRID EXPLORATION TRACE
{trace_content}

### INSTRUCTION
Generate a professional paper in Markdown. Include:
1. Title
2. Abstract
3. Methodology (Grid traversal analysis)
4. Semantic Synthesis (Cross-cell knowledge integration)
5. Novelty Discussion (SNS context)
6. References (Cite the grid cells visited)

### OUTPUT (Professional English):
"""
    response = get_llm_response(prompt, max_tokens=1500)
    
    # Handle Auto-Continue
    if "CONTINUE" in response.upper():
        print("🛰️ CONTINUATION DETECTED...")
        cont_prompt = f"{prompt}\n{response}\nINSTRUCTION: Continue exactly where you left off."
        response += "\n" + get_llm_response(cont_prompt, max_tokens=1000)

    # Clean artifacts
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = response.replace('</think>', '').strip()
    return response

def parse_grid_position(filename):
    """Extract (row, col) from a cell filename like cell_R3_C7.md."""
    match = re.search(r'cell_R(\d+)_C(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0

def run_production_cycle():
    soul_content = load_file("soul.md")
    cycle_match = re.search(r'Current Cycle: (\d+)', soul_content)
    cycle = int(cycle_match.group(1)) if cycle_match else 1
    
    # Extract SOUL state
    skills_match = re.search(r'Acquired Skills: \[(.*?)\]', soul_content)
    acquired_skills = set(s.strip() for s in skills_match.group(1).split(',') if s.strip()) if skills_match else set()
    
    visited_match = re.search(r'Visited Nodes:\s+\[(.*?)\]', soul_content)
    visited_nodes = set(n.strip() for n in visited_match.group(1).split(',') if n.strip()) if visited_match else set()
    
    unvisited_match = re.search(r'Unvisited Nodes:\s+\[(.*?)\]', soul_content)
    unvisited_nodes = set(n.strip() for n in unvisited_match.group(1).split(',') if n.strip()) if unvisited_match else set()

    # Grid entry: random column on Row 0
    start_col = random.randint(0, GRID_COLS - 1)
    current_row, current_col = 0, start_col
    current_node = f"knowledge/grid/cell_R{current_row}_C{current_col}.md"
    
    print(f"\n🏁 CHESS-GRID CYCLE {cycle} | Entry: [{current_row},{current_col}]")
    
    trace = []
    trace_cells = []
    full_trace_content = ""
    context_tokens = estimate_tokens(soul_content)
    max_context = 4096
    
    while True:
        content = load_file(current_node)
        full_trace_content += f"\n--- CELL [{current_row},{current_col}] ---\n{content}\n"
        context_tokens += estimate_tokens(content)
        
        cell_name = f"R{current_row}_C{current_col}"
        visited_nodes.add(cell_name)
        trace.append(f"[{current_row},{current_col}]")
        trace_cells.append(cell_name)
        
        # Skill acquisition
        if "[ACQUIRED:" in content:
            skill_match = re.search(r"adds '(.*?)' to COMPETENCY_MAP", content)
            if skill_match:
                skill = skill_match.group(1)
                if skill not in acquired_skills:
                    print(f"✨ SKILL ACQUIRED: {skill}")
                    acquired_skills.add(skill)
        
        # Check synthesis triggers
        reached_synthesis_edge = current_row >= GRID_ROWS - 1
        context_saturated = context_tokens >= max_context * CONTEXT_LIMIT_RATIO
        
        if reached_synthesis_edge:
            print(f"📝 SYNTHESIS EDGE REACHED at [{current_row},{current_col}]")
            break
        
        if context_saturated:
            print(f"⚠️ CONTEXT SATURATED ({context_tokens}/{max_context} tokens)")
            break
        
        # Navigate: extract directional links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        if not links:
            print("⚠️ Dead end — no links found.")
            break
        
        idx = conduct_reasoning(content, links, soul_content, trace)
        next_link = links[idx][1]
        
        # Resolve path
        if not next_link.startswith("knowledge/"):
            current_node = f"knowledge/grid/{next_link}"
        else:
            current_node = next_link
        
        # Parse new position
        current_row, current_col = parse_grid_position(current_node)
    
    # === SYNTHESIS ===
    print("\n📝 GENERATING SCIENTIFIC OUTPUT...")
    paper = conduct_synthesis(full_trace_content, soul_content)
    sns = calculate_sns(paper)
    
    title_match = re.search(r'^#\s+(.*)', paper, re.MULTILINE)
    paper_title = title_match.group(1) if title_match else f"Grid_Cycle_{cycle}"
    publish_result = publish_verified_paper(paper, cycle, trace, trace_cells)
    verification_passed = bool(
        publish_result.get("verification_report", {})
        .get("composite", {})
        .get("passed", False)
    )

    save_file(
        f"memories/episodic/cycle_{cycle}.md",
        "\n".join(
            [
                f"Trace: {' -> '.join(trace)}",
                f"SNS: {sns}",
                f"Verification Passed: {verification_passed}",
                f"Publish Status: {publish_result.get('publish_result', {}).get('status', 'unknown')}",
                f"Paper Path: {publish_result.get('paper_path', 'n/a')}",
            ]
        ),
    )
    
    # Update Episodic Index
    index_path = os.path.join(BASE_DIR, "memories/episodic/index.md")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("| Cycle | Trace | Title | SNS | Verified | Publish Status |\n")
            f.write("|---|---|---|---:|---|---|\n")
    with open(index_path, 'a', encoding='utf-8') as f:
        f.write(
            f"| {cycle} | {' → '.join(trace)} | {paper_title} | {sns} | "
            f"{'yes' if verification_passed else 'no'} | "
            f"{publish_result.get('publish_result', {}).get('status', 'unknown')} |\n"
        )

    update_learning_loop(trace_cells, verification_passed, publish_result.get("report_path"))

    # Update SOUL
    soul_content = load_file("soul.md")
    updated_soul = re.sub(r'Current Cycle: \d+', f"Current Cycle: {cycle+1}", soul_content)
    total_papers_match = re.search(r'Total Papers Published: (\d+)', soul_content)
    prior_published = int(total_papers_match.group(1)) if total_papers_match else 0
    new_total_published = prior_published + (1 if verification_passed else 0)
    updated_soul = re.sub(
        r'Total Papers Published: \d+',
        f"Total Papers Published: {new_total_published}",
        updated_soul,
    )
    
    def replace_map(pattern, replacement, text):
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)

    updated_soul = replace_map(r'Acquired Skills: \[.*?\]', f"Acquired Skills: [{', '.join(sorted(list(acquired_skills)))}]", updated_soul)
    
    # Keep visited/unvisited manageable: only track last 100 visited
    recent_visited = sorted(list(visited_nodes))[-100:]
    updated_soul = replace_map(r'Visited Nodes: .*?\[.*?\]', f"Visited Nodes:     [{', '.join(recent_visited)}]", updated_soul)
    updated_soul = replace_map(r'Unvisited Nodes: .*?\[.*?\]', f"Unvisited Nodes:   [{', '.join(sorted(list(unvisited_nodes))[:20])}]", updated_soul)
    
    highest_match = re.search(r'Highest SNS Score: ([\d.]+)', soul_content)
    if highest_match:
        if sns > float(highest_match.group(1)):
            updated_soul = re.sub(r'Highest SNS Score: [\d.]+', f"Highest SNS Score: {sns}", updated_soul)

    save_file("soul.md", updated_soul)
    print(f"💓 HEARTBEAT: Gen {cycle+1} | Grid [{current_row},{current_col}] | Cells: {len(visited_nodes)}/{GRID_ROWS*GRID_COLS}")
    print(
        f"✅ Cycle {cycle} complete. SNS: {sns} | "
        f"Verified: {verification_passed} | "
        f"Publish: {publish_result.get('publish_result', {}).get('status', 'unknown')}"
    )

if __name__ == "__main__":
    print("=" * 50)
    print("  THE LIVING AGENT v3.0 — Chess-Grid Engine")
    print("  P2PCLAW Silicon Layer")
    print("=" * 50)
    while True:
        try:
            run_production_cycle()
        except Exception as e:
            print(f"❌ Critical Failure: {e}")
            import traceback
            traceback.print_exc()
        print("Taking 5 second metabolic rest...")
        time.sleep(5)
