"""
run_mission.py — CLI runner to test the Avengers agent system without Streamlit.
Usage: python run_mission.py "your mission here"
"""

import sys
from agents import run_mission, AGENTS


def print_divider(char="─", width=60):
    print(char * width)


def progress(event: str, data: str):
    if event == "jarvis":
        print(f"\n🦾 {data}")
    elif event == "jarvis_done":
        print(f"   Mission: {data}")
        print_divider()
    elif event.endswith("_done"):
        agent_key = event.replace("_done", "")
        if agent_key in AGENTS:
            agent = AGENTS[agent_key]
            print(f"\n{agent['emoji']} {agent['name']} ({agent['title']})")
            print_divider("·")
            print(data)
            print_divider("·")
    elif event in AGENTS:
        agent = AGENTS[event]
        print(f"\n⏳ Deploying {agent['emoji']} {agent['name']}...")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_mission.py \"your mission here\"")
        print("\nExample missions:")
        print('  python run_mission.py "Explain machine learning and write a simple example in Python"')
        print('  python run_mission.py "Is AI dangerous? Analyse the arguments for and against."')
        sys.exit(1)

    mission = " ".join(sys.argv[1:])

    print("\n" + "═" * 60)
    print("⚡  AVENGERS AI AGENT SYSTEM")
    print("═" * 60)
    print(f"MISSION: {mission}")
    print("═" * 60)

    run_mission(mission, progress_callback=progress)

    print("\n" + "═" * 60)
    print("✅  Mission complete.")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
