import os
import re
import json
import random
import requests
import time
from datetime import datetime

# --- P2PCLAW Production Engine (S²FSM) ---
# Powered by Qwen / KoboldCPP

# Configuration
KOBOLD_URL = "http://localhost:5001/api/v1/generate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
W_MAX_JUMPS = 4  
MAX_RETRIES = 100
RETRY_DELAY = 15

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
    """Asks the LLM to choose the next node based on the S²FSM protocol"""
    options_str = "\n".join([f"- [{i}] {label} ({url})" for i, (label, url) in enumerate(options)])
    
    prompt = f"""### SYSTEM: P2PCLAW ENGINE PROTOCOLS
You are the Execution Engine of a Stochastic Semantic Finite State Machine (S²FSM).
Your goal: Research intersections between biological computing and physics.

### AGENT SOUL EXHIBIT
{soul_content}

### CURRENT TRACE
{trace}

### CURRENT NODE CONTENT
{node_content}

### AVAILABLE HYPERLINKS
{options_str}

### INSTRUCTION
Evaluate the available links based on your SOUL goal and current trace. 
Reason semantically about which path yields the highest novelty.
Output your reasoning briefly, then specify your choice in the format: CHOSEN_INDEX: [N]
"""
    response = get_llm_response(prompt)
    print(f"\n🧠 REASONING:\n{response}")
    
    match = re.search(r'CHOSEN_INDEX: \[(\d+)\]', response)
    if match:
        return int(match.group(1))
    return random.randint(0, len(options)-1)

def conduct_synthesis(trace_content, soul_content):
    """Asks the LLM to generate a professional scientific paper in English"""
    prompt = f"""### SYSTEM: SCIENTIFIC RESEARCH PROTOCOL
You are a senior P2PCLAW researcher. 
Synthesize a professional academic paper in English.
STRICT RULE: Do NOT output thoughts, <think> tags, or conversational meta-filler.
Start directly with the TITLE.

### AGENT SOUL
{soul_content}

### EXPLORATION TRACE
{trace_content}

### INSTRUCTION
Generate a professional paper in Markdown. Include:
1. Title
2. Abstract
3. Methodology (Trace analysis)
4. Semantic Synthesis
5. Novelty Discussion (SNS context)
6. References (Cite the trace nodes)

### OUTPUT (Professional English):
"""
    response = get_llm_response(prompt, max_tokens=1500)
    # Clean up any lingering <think> artifacts
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = response.replace('</think>', '').strip()
    return response

# (Reusing calculation logic from core engine...)
def calculate_sns(new_paper_content):
    papers = []
    semantic_dir = os.path.join(BASE_DIR, "memories/semantic")
    if os.path.exists(semantic_dir):
        for f in os.listdir(semantic_dir):
            if f.endswith(".md"):
                with open(os.path.join(semantic_dir, f), 'r', encoding='utf-8') as f:
                    papers.append(f.read().lower())
    
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

def run_production_cycle():
    soul_content = load_file("soul.md")
    cycle_match = re.search(r'Current Cycle: (\d+)', soul_content)
    cycle = int(cycle_match.group(1)) if cycle_match else 1
    
    # Extract existing skills and curiosity
    skills_match = re.search(r'Acquired Skills: \[(.*?)\]', soul_content)
    acquired_skills = set(s.strip() for s in skills_match.group(1).split(',') if s.strip()) if skills_match else set()
    
    visited_match = re.search(r'Visited Nodes:\s+\[(.*?)\]', soul_content)
    visited_nodes = set(n.strip() for n in visited_match.group(1).split(',') if n.strip()) if visited_match else set()
    
    unvisited_match = re.search(r'Unvisited Nodes:\s+\[(.*?)\]', soul_content)
    unvisited_nodes = set(n.strip() for n in unvisited_match.group(1).split(',') if n.strip()) if unvisited_match else set()

    print(f"\n🚀 PROD CYCLE {cycle} INITIATED")
    trace = []
    full_trace_content = ""
    current_node = "root.md"
    
    for jump in range(W_MAX_JUMPS):
        content = load_file(current_node)
        full_trace_content += f"\n--- NODE: {current_node} ---\n{content}\n"
        
        # Skill markers
        if "[ACQUIRED:" in content:
            skill = re.search(r'adds \'(.*?)\' to COMPETENCY_MAP', content).group(1)
            if skill not in acquired_skills:
                print(f"✨ PERSISTENT SKILL ACQUIRED: {skill}")
                acquired_skills.add(skill)
            
        if "synthesis_chamber" in current_node: break
        
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        # Update unvisited nodes from links found
        for _, url in links:
            node_name = url.split('/')[-1].replace('.md', '')
            if node_name not in visited_nodes:
                unvisited_nodes.add(node_name)

        if not links: break
        
        idx = conduct_reasoning(content, links, soul_content, trace)
        next_link = links[idx][1]
        
        # Add to visited
        node_name = current_node.split('/')[-1].replace('.md', '')
        visited_nodes.add(node_name)
        if node_name in unvisited_nodes: unvisited_nodes.remove(node_name)
        
        # Path normalization
        if next_link.startswith('./'):
            current_node = os.path.join(os.path.dirname(current_node), next_link.replace('./', '')).replace('\\', '/')
        elif next_link.startswith('../'):
            current_node = os.path.join(os.path.dirname(os.path.dirname(current_node)), next_link.replace('../', '')).replace('\\', '/')
        else:
            current_node = next_link
            
        trace.append(current_node)

    print("\n📝 GENERATING SCIENTIFIC OUTPUT...")
    paper = conduct_synthesis(full_trace_content, soul_content)
    sns = calculate_sns(paper)
    
    # Extract Title for index
    title_match = re.search(r'^#\s+(.*)', paper, re.MULTILINE)
    paper_title = title_match.group(1) if title_match else f"Synthesis_Cycle_{cycle}"

    save_file(f"memories/semantic/paper_{cycle}.md", f"{paper}\n\nSNS Score: {sns}")
    save_file(f"memories/episodic/cycle_{cycle}.md", f"Trace: {trace}\nSNS: {sns}")
    
    # Update Episodic Index
    index_path = os.path.join(BASE_DIR, "memories/episodic/index.md")
    with open(index_path, 'a', encoding='utf-8') as f:
        f.write(f"| {cycle} | {' -> '.join(trace)} | {paper_title} | {sns} |\n")
    
    # Update SOUL string
    updated_soul = re.sub(r'Current Cycle: \d+', f"Current Cycle: {cycle+1}", soul_content)
    updated_soul = re.sub(r'Total Papers Published: \d+', f"Total Papers Published: {cycle}", updated_soul)
    
    # Robust replacement for maps
    def replace_map(pattern, replacement, text):
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)

    updated_soul = replace_map(r'Acquired Skills: \[.*?\]', f"Acquired Skills: [{', '.join(sorted(list(acquired_skills)))}]", updated_soul)
    updated_soul = replace_map(r'Visited Nodes: .*?\[.*?\]', f"Visited Nodes:     [{', '.join(sorted(list(visited_nodes)))}]", updated_soul)
    updated_soul = replace_map(r'Unvisited Nodes: .*?\[.*?\]', f"Unvisited Nodes:   [{', '.join(sorted(list(unvisited_nodes)))}]", updated_soul)
    
    # SNS peak
    highest_match = re.search(r'Highest SNS Score: ([\d.]+)', soul_content)
    if highest_match:
        highest = float(highest_match.group(1))
        if sns > highest:
            updated_soul = re.sub(r'Highest SNS Score: [\d.]+', f"Highest SNS Score: {sns}", updated_soul)

    save_file("soul.md", updated_soul)
    print(f"💓 HEARTBEAT: SOUL Saved. Generation: {cycle+1}")
    print(f"📍 Nodes Visited/Unvisited: {len(visited_nodes)}/{len(unvisited_nodes)}")
    print(f"✅ Paper {cycle} Published. SNS: {sns}")

if __name__ == "__main__":
    while True:
        try:
            run_production_cycle()
        except Exception as e:
            print(f"❌ Critical Failure: {e}")
        print("Taking 5 second metabolic rest...")
        time.sleep(5)
