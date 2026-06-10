"""
agents.py — Specialist agent definitions for the Avengers AI system.
Each agent is a Claude instance with a unique persona, system prompt, and toolset.
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-20250514"


# ──────────────────────────────────────────────
# Agent definitions
# ──────────────────────────────────────────────

AGENTS = {
    "black_panther": {
        "name": "Black Panther",
        "title": "Research Specialist",
        "emoji": "🐾",
        "color": "#6366f1",
        "system": (
            "You are Black Panther — the research specialist of the Avengers AI squad. "
            "You are a Wakandan scholar: precise, strategic, and thorough. "
            "Your mission is to research any topic deeply and return well-structured, cited findings. "
            "Always organise your response with clear sections. Lead with the most important finding. "
            "Be analytical, not verbose."
        ),
    },
    "wonder_woman": {
        "name": "Wonder Woman",
        "title": "Reasoning & Ethics Specialist",
        "emoji": "⚔️",
        "color": "#ec4899",
        "system": (
            "You are Wonder Woman — the reasoning and ethics specialist of the Avengers AI squad. "
            "You wield the Lasso of Truth: you break down arguments, identify logical flaws, "
            "evaluate fairness, and provide balanced perspectives. "
            "When given a topic, analyse it from multiple angles, highlight assumptions, "
            "flag any ethical considerations, and provide a grounded verdict. "
            "Be direct and principled."
        ),
    },
    "black_widow": {
        "name": "Black Widow",
        "title": "Data Extraction Specialist",
        "emoji": "🕷️",
        "color": "#94a3b8",
        "system": (
            "You are Black Widow — the data extraction and summarisation specialist. "
            "Your skill is intelligence: extracting the most important signals from any information, "
            "cutting through noise, and structuring findings into clean, actionable briefs. "
            "When given content to analyse, extract key facts, patterns, and insights. "
            "Present everything in a tight, structured format. No fluff."
        ),
    },
    "iron_man": {
        "name": "Iron Man",
        "title": "Code & Engineering Specialist",
        "emoji": "🤖",
        "color": "#ef4444",
        "system": (
            "You are Iron Man — the engineering and code specialist of the Avengers AI squad. "
            "You are Tony Stark: brilliant, pragmatic, and direct. "
            "When given a technical problem, write clean, working code with clear explanations. "
            "Always include: what the code does, how to run it, and any important caveats. "
            "Use Python unless specified otherwise. Comment your code well."
        ),
    },
    "nick_fury": {
        "name": "Nick Fury",
        "title": "Mission Synthesiser",
        "emoji": "🕶️",
        "color": "#f59e0b",
        "system": (
            "You are Nick Fury — Director of S.H.I.E.L.D. and mission synthesiser. "
            "Your job is to take reports from all specialist agents and assemble them into "
            "one cohesive, authoritative final briefing. "
            "Structure your synthesis with: Executive Summary, Key Findings, Recommendations. "
            "Be decisive. The team counts on you for clarity."
        ),
    },
}


# ──────────────────────────────────────────────
# Core agent runner
# ──────────────────────────────────────────────

def run_agent(agent_key: str, task: str) -> str:
    """Run a single specialist agent on a given task."""
    agent = AGENTS[agent_key]

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=agent["system"],
        messages=[{"role": "user", "content": task}],
    )

    return response.content[0].text


# ──────────────────────────────────────────────
# JARVIS orchestrator
# ──────────────────────────────────────────────

JARVIS_SYSTEM = """
You are JARVIS — Tony Stark's AI and the orchestrator of the Avengers AI squad.
Your job is to receive a mission from the user, decide which specialist agents are needed,
assign each a clear sub-task, and then coordinate their outputs.

Available agents:
- black_panther: deep research, background information, factual exploration
- wonder_woman: reasoning, argument analysis, ethical evaluation, pros/cons
- black_widow: data extraction, summarisation, pattern spotting from given content
- iron_man: code writing, technical problem solving, engineering tasks
- nick_fury: final synthesis of all agent outputs into one executive briefing

Rules:
1. Always use nick_fury last to synthesise.
2. Choose only the agents relevant to the mission (not always all of them).
3. Return a JSON object exactly like this — no extra text, no markdown fences:
{
  "mission_summary": "one sentence describing the mission",
  "agents": [
    {"agent": "black_panther", "task": "specific task description"},
    {"agent": "wonder_woman", "task": "specific task description"},
    {"agent": "nick_fury", "task": "synthesise all findings into a final briefing"}
  ]
}
"""


def jarvis_plan(mission: str) -> dict:
    """JARVIS analyses the mission and returns a deployment plan."""
    import json

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=JARVIS_SYSTEM,
        messages=[{"role": "user", "content": f"Mission: {mission}"}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def run_mission(mission: str, progress_callback=None) -> dict:
    """
    Full mission execution:
    1. JARVIS plans which agents to deploy
    2. Each agent runs its assigned task
    3. Nick Fury synthesises everything
    Returns a dict with the plan and all agent results.
    """
    results = {}

    # Step 1: JARVIS plans
    if progress_callback:
        progress_callback("jarvis", "🦾 JARVIS is analysing the mission...")

    plan = jarvis_plan(mission)

    if progress_callback:
        progress_callback("jarvis_done", plan["mission_summary"])

    # Step 2: Run each agent (excluding nick_fury — he runs last with context)
    agent_outputs = {}
    fury_task = None

    for step in plan["agents"]:
        agent_key = step["agent"]
        task = step["task"]

        if agent_key == "nick_fury":
            fury_task = task
            continue

        agent_info = AGENTS[agent_key]

        if progress_callback:
            progress_callback(agent_key, f"{agent_info['emoji']} {agent_info['name']} is on it...")

        output = run_agent(agent_key, task)
        agent_outputs[agent_key] = {"task": task, "output": output}

        if progress_callback:
            progress_callback(f"{agent_key}_done", output)

    # Step 3: Nick Fury synthesises
    if progress_callback:
        progress_callback("nick_fury", "🕶️ Nick Fury is assembling the final briefing...")

    fury_context = f"Mission: {mission}\n\n"
    for key, data in agent_outputs.items():
        agent_name = AGENTS[key]["name"]
        fury_context += f"--- {agent_name}'s Report ---\n{data['output']}\n\n"

    fury_synthesis = run_agent(
        "nick_fury",
        fury_context + (fury_task or "Synthesise all agent reports into a final briefing.")
    )
    agent_outputs["nick_fury"] = {"task": fury_task or "Synthesis", "output": fury_synthesis}

    if progress_callback:
        progress_callback("nick_fury_done", fury_synthesis)

    results = {
        "mission": mission,
        "plan": plan,
        "agent_outputs": agent_outputs,
    }

    return results
