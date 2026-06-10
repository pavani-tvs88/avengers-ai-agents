"""
app.py — Streamlit UI for the Avengers AI Agent System.
JARVIS orchestrates specialist agents to tackle any mission.
"""

import streamlit as st
from agents import run_mission, AGENTS, jarvis_plan

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Avengers AI Agents",
    page_icon="⚡",
    layout="wide",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Dark theme base */
    .stApp { background-color: #0f172a; }

    /* Mission input */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
    }

    /* Agent cards */
    .agent-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-left: 4px solid;
    }
    .agent-header {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .agent-output {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* JARVIS header */
    .jarvis-banner {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 24px;
        border: 1px solid #4c1d9540;
    }

    /* Nick Fury synthesis box */
    .fury-box {
        background: linear-gradient(135deg, #1c1917, #292524);
        border-radius: 12px;
        padding: 20px 24px;
        border: 2px solid #f59e0b40;
        margin-top: 10px;
    }

    /* Squad cards */
    .squad-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 12px 14px;
        text-align: center;
        border: 1px solid #334155;
    }

    h1, h2, h3 { color: #f1f5f9 !important; }
    p, li { color: #94a3b8; }

    .stButton button {
        background: linear-gradient(135deg, #4c1d95, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 32px !important;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #5b21b6, #8b5cf6) !important;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────

st.markdown("""
<div class="jarvis-banner">
    <div style="font-size: 11px; font-weight: 700; color: #a78bfa; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px;">
        Powered by Claude API · Multi-Agent System
    </div>
    <h1 style="font-size: 28px; font-weight: 900; color: #f1f5f9; margin: 0;">
        ⚡ Avengers AI Agents
    </h1>
    <p style="color: #94a3b8; margin-top: 8px; font-size: 14px;">
        JARVIS assembles the right squad for every mission. Research, reasoning, data extraction, code — all working together.
    </p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Squad overview
# ──────────────────────────────────────────────

with st.expander("🦸 Meet the Squad", expanded=False):
    cols = st.columns(5)
    squad = [
        ("🦾", "JARVIS", "Orchestrator", "#7c3aed"),
        ("🐾", "Black Panther", "Research", "#6366f1"),
        ("⚔️", "Wonder Woman", "Reasoning", "#ec4899"),
        ("🕷️", "Black Widow", "Data Extraction", "#94a3b8"),
        ("🤖", "Iron Man", "Code & Engineering", "#ef4444"),
        ("🕶️", "Nick Fury", "Mission Synthesis", "#f59e0b"),
    ]
    cols = st.columns(6)
    for col, (emoji, name, role, color) in zip(cols, squad):
        with col:
            st.markdown(f"""
            <div class="squad-card">
                <div style="font-size: 28px">{emoji}</div>
                <div style="font-weight: 700; color: {color}; font-size: 13px; margin-top: 6px">{name}</div>
                <div style="color: #64748b; font-size: 11px; margin-top: 2px">{role}</div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Example missions
# ──────────────────────────────────────────────

st.markdown("### 🎯 Your Mission")

examples = [
    "Explain quantum computing and write a Python simulation of a simple qubit",
    "What are the pros and cons of remote work? Analyse the evidence.",
    "Research the history of AI and summarise the key milestones",
    "Write a Python web scraper and explain how it works",
    "Is social media good or bad for society? Give a balanced analysis.",
]

selected_example = st.selectbox(
    "Try an example mission or write your own below:",
    ["— choose an example —"] + examples,
    label_visibility="collapsed",
)

mission_input = st.text_area(
    "Mission",
    value=selected_example if selected_example != "— choose an example —" else "",
    placeholder="Type any mission: research a topic, solve a problem, write code, analyse an argument...",
    height=100,
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    launch = st.button("⚡ Assemble the Squad", use_container_width=True)


# ──────────────────────────────────────────────
# Mission execution
# ──────────────────────────────────────────────

AGENT_COLORS = {
    "black_panther": "#6366f1",
    "wonder_woman": "#ec4899",
    "black_widow": "#94a3b8",
    "iron_man": "#ef4444",
    "nick_fury": "#f59e0b",
}

if launch and mission_input.strip():
    st.markdown("---")
    st.markdown("### 🚀 Mission in Progress")

    # Status area
    status_placeholder = st.empty()
    status_placeholder.info("🦾 JARVIS is analysing the mission...")

    # Results containers — pre-create so they appear in order
    jarvis_container = st.container()
    agent_containers = {}
    fury_container = st.container()

    try:
        # Step 1: Get JARVIS plan
        plan = jarvis_plan(mission_input.strip())
        deployed = [s["agent"] for s in plan["agents"] if s["agent"] != "nick_fury"]
        fury_step = next((s for s in plan["agents"] if s["agent"] == "nick_fury"), None)

        with jarvis_container:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1b4b, #1e293b); border-radius: 12px;
                        padding: 16px 20px; margin-bottom: 16px; border: 1px solid #7c3aed40;">
                <div style="font-size: 11px; font-weight: 700; color: #a78bfa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">
                    🦾 JARVIS — Mission Briefing
                </div>
                <div style="font-size: 14px; color: #c4b5fd; font-weight: 600; margin-bottom: 8px;">
                    {plan['mission_summary']}
                </div>
                <div style="font-size: 12px; color: #64748b;">
                    Deploying: {' · '.join([AGENTS[a]['emoji'] + ' ' + AGENTS[a]['name'] for a in deployed])} · 🕶️ Nick Fury
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Step 2: Run each specialist agent
        agent_outputs = {}

        for step in plan["agents"]:
            agent_key = step["agent"]
            if agent_key == "nick_fury":
                continue

            agent_info = AGENTS[agent_key]
            status_placeholder.info(f"{agent_info['emoji']} {agent_info['name']} is on the mission...")

            output = None
            placeholder = st.empty()

            # Show thinking state
            placeholder.markdown(f"""
            <div class="agent-card" style="border-color: {AGENT_COLORS[agent_key]}; opacity: 0.6;">
                <div class="agent-header" style="color: {AGENT_COLORS[agent_key]};">
                    {agent_info['emoji']} {agent_info['name']} <span style="color: #475569; font-weight: 400;">— {agent_info['title']}</span>
                </div>
                <div style="color: #475569; font-size: 13px; font-style: italic;">Working on: {step['task'][:80]}...</div>
            </div>
            """, unsafe_allow_html=True)

            from agents import run_agent
            output = run_agent(agent_key, step["task"])
            agent_outputs[agent_key] = {"task": step["task"], "output": output}

            # Show completed result
            placeholder.markdown(f"""
            <div class="agent-card" style="border-color: {AGENT_COLORS[agent_key]};">
                <div class="agent-header" style="color: {AGENT_COLORS[agent_key]};">
                    {agent_info['emoji']} {agent_info['name']} <span style="color: #475569; font-weight: 400;">— {agent_info['title']}</span>
                </div>
                <div class="agent-output">{output}</div>
            </div>
            """, unsafe_allow_html=True)

        # Step 3: Nick Fury synthesis
        status_placeholder.info("🕶️ Nick Fury is assembling the final briefing...")

        fury_context = f"Mission: {mission_input}\n\n"
        for key, data in agent_outputs.items():
            fury_context += f"--- {AGENTS[key]['name']}'s Report ---\n{data['output']}\n\n"

        fury_task = fury_step["task"] if fury_step else "Synthesise all reports into a final mission briefing."
        from agents import run_agent
        fury_output = run_agent("nick_fury", fury_context + fury_task)

        with fury_container:
            st.markdown(f"""
            <div class="fury-box">
                <div style="font-size: 11px; font-weight: 700; color: #f59e0b; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px;">
                    🕶️ Nick Fury — Final Mission Briefing
                </div>
                <div style="font-size: 13px; color: #e2e8f0; line-height: 1.8; white-space: pre-wrap;">{fury_output}</div>
            </div>
            """, unsafe_allow_html=True)

        status_placeholder.success("✅ Mission complete. Avengers, stand down.")

    except Exception as e:
        status_placeholder.error(f"Mission failed: {str(e)}")
        st.exception(e)

elif launch and not mission_input.strip():
    st.warning("Please enter a mission before assembling the squad.")


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #334155; font-size: 12px; padding: 10px 0;">
    Built with Claude API (claude-sonnet-4) · Multi-agent orchestration · 
    <a href="https://github.com/pavani-tvs88/avengers-ai-agents" style="color: #6366f1;">GitHub</a>
</div>
""", unsafe_allow_html=True)
