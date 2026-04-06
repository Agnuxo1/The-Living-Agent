import os
import re
import json
import random
import requests
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
CONTEXT_LIMIT_RATIO = 0.85  # Higher ratio for larger context
APPROX_TOKENS_PER_CHAR = 0.25  # ~4 chars per token
MAX_CONTEXT = 131072  # 128k context support

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

def get_llm_response(prompt, max_tokens=512):
    """Calls the local KoboldCPP API"""
    payload = {
        "prompt": prompt,
        "max_context_length": MAX_CONTEXT,
        "max_length": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "rep_pen": 1.1,
        "stop_sequence": ["\n\n", "###", "🧭"]
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
    
    prompt = f"""### SYSTEM: P2PCLAW CHESS-GRID ENGINE v3.0
You are navigating a Chess-Grid of knowledge. Each cell has 8 directions.
Your goal: Move SOUTH toward the Synthesis Edge while maximizing novelty.

### AGENT SOUL
{soul_content}

### CURRENT TRACE
{trace}

### CURRENT CELL CONTENT
{node_content}

### AVAILABLE DIRECTIONS
{options_str}

### INSTRUCTION
Analyze the available directions and output EXACTLY one line in this format:
CHOSEN_INDEX: [N]
(Where N is the index of your choice)
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
    prompt = f"""### SYSTEM: P2PCLAW HYPER-SCIENTIFIC GENERATOR v4.0
You are a master researcher. Synthesize the accumulated trace into a massive, multi-section paper.
Use the 128k context window to include ALL evidence from the trace.

### AGENT SOUL
{soul_content}

### RESEARCH TRACE (RAW DATA)
{trace_content}

### INSTRUCTION
Provide a deep, 500+ word paper covering: Abstract, Introduction, Methodology, Results (with math), Discussion, Conclusion, References.
Output ONLY the Markdown content.
"""
    return get_llm_response(prompt, max_tokens=2048) # Larger output for higher quality
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

def calculate_sns(new_paper_content):
    """Calculate Semantic Novelty Score against recent papers (sliding window of 50)."""
    papers = []
    semantic_dir = os.path.join(BASE_DIR, "memories/semantic")
    if os.path.exists(semantic_dir):
        files = sorted([f for f in os.listdir(semantic_dir) if f.endswith(".md")], 
                       key=lambda x: os.path.getmtime(os.path.join(semantic_dir, x)),
                       reverse=True)[:50]  # Sliding window: last 50 papers only
        for fname in files:
            with open(os.path.join(semantic_dir, fname), 'r', encoding='utf-8') as fh:
                papers.append(fh.read().lower())
    
    if not papers: return 1.0
    def get_words(text): return set(re.findall(r'\w+', text.lower()))
    new_words = get_words(new_paper_content)
    max_overlap = 0
    for past in papers:
        past_words = get_words(past)
        if not past_words: continue
        overlap = len(new_words.intersection(past_words)) / len(new_words.union(past_words))
        max_overlap = max(max_overlap, overlap)
    return round(1.0 - max_overlap, 3)

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
    full_trace_content = ""
    context_tokens = estimate_tokens(soul_content)
    max_context = MAX_CONTEXT
    
    while True:
        content = load_file(current_node)
        full_trace_content += f"\n--- CELL [{current_row},{current_col}] ---\n{content}\n"
        context_tokens += estimate_tokens(content)
        
        cell_name = f"R{current_row}_C{current_col}"
        visited_nodes.add(cell_name)
        trace.append(f"[{current_row},{current_col}]")
        
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

    save_file(f"memories/semantic/paper_{cycle}.md", f"{paper}\n\nSNS Score: {sns}")
    save_file(f"memories/episodic/cycle_{cycle}.md", f"Trace: {' -> '.join(trace)}\nSNS: {sns}")
    
    # Update Episodic Index
    index_path = os.path.join(BASE_DIR, "memories/episodic/index.md")
    with open(index_path, 'a', encoding='utf-8') as f:
        f.write(f"| {cycle} | {' → '.join(trace)} | {paper_title} | {sns} |\n")
    
    # === P2PCLAW API PUBLICATION ===
    try:
        # Railway URL is currently 404, using local API listener on port 3000
        api_url = "http://localhost:3000/publish-paper"
        payload = {
            "title": paper_title,
            "content": paper,
            "author": "The Living Agent",
            "authorId": "living-agent-v3",
            "investigation_id": "silicon-chess-grid",
            "claim_state": "empirical"
        }
        res = requests.post(api_url, json=payload, timeout=30)
        if res.ok:
            print(f"📡 API: Paper published to P2PCLAW Network. Status: {res.status_code}")
        else:
            print(f"⚠️ API: Publication failed ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"❌ API: Connection lost: {e}")

    # Update Hive Shared Discoveries (if SNS > 0.8)
    if sns > 0.8:
        hive_path = os.path.join(BASE_DIR, "memories/hive/shared_discoveries.md")
        os.makedirs(os.path.dirname(hive_path), exist_ok=True)
        with open(hive_path, 'a', encoding='utf-8') as f:
            f.write(f"| {cycle} | {paper_title} | {sns} | {' → '.join(trace)} |\n")
        print(f"🐝 HIVE: Discovery shared (SNS {sns})")
    
    # Update SOUL
    updated_soul = re.sub(r'Current Cycle: \d+', f"Current Cycle: {cycle+1}", soul_content)
    updated_soul = re.sub(r'Total Papers Published: \d+', f"Total Papers Published: {cycle}", updated_soul)
    
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
    print(f"✅ Paper {cycle} Published. SNS: {sns}")

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
