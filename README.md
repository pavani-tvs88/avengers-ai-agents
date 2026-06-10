# ⚡ Avengers AI Agents

A multi-agent AI system where **JARVIS** orchestrates a squad of specialist agents — each powered by Claude — to tackle any mission: research, reasoning, data extraction, code generation, and synthesis.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🦸 The Squad

| Agent | Role | Speciality |
|-------|------|------------|
| 🦾 **JARVIS** | Orchestrator | Decomposes missions, routes to the right agents, coordinates outputs |
| 🐾 **Black Panther** | Research Specialist | Deep research, factual exploration, structured findings |
| ⚔️ **Wonder Woman** | Reasoning & Ethics | Argument analysis, logical evaluation, balanced perspectives |
| 🕷️ **Black Widow** | Data Extraction | Summarisation, pattern spotting, intelligence briefing |
| 🤖 **Iron Man** | Code & Engineering | Code writing, technical problem solving, explanations |
| 🕶️ **Nick Fury** | Mission Synthesiser | Assembles all agent outputs into one final executive briefing |

---

## 🚀 How It Works

1. **You give JARVIS a mission** — any task, any domain
2. **JARVIS plans** — decides which agents are needed and assigns each a specific sub-task
3. **Agents execute in parallel** — each brings their unique expertise
4. **Nick Fury synthesises** — assembles a final, cohesive briefing from all reports

```
User Mission
     │
     ▼
  🦾 JARVIS (planner)
     │
     ├──► 🐾 Black Panther (research)
     ├──► ⚔️ Wonder Woman (reasoning)
     ├──► 🕷️ Black Widow (extraction)
     ├──► 🤖 Iron Man (code)
     │
     ▼
  🕶️ Nick Fury (synthesis)
     │
     ▼
  Final Briefing
```

---

## 🛠️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/pavani-tvs88/avengers-ai-agents.git
cd avengers-ai-agents
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

Or export directly:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

---

## 🖥️ Running the App

### Streamlit UI (recommended)
```bash
streamlit run app.py
```

### CLI (for quick testing)
```bash
python run_mission.py "Explain quantum computing and write a Python example"
python run_mission.py "Is remote work better than office work? Analyse the evidence."
python run_mission.py "Write a web scraper in Python and explain how it works"
```

---

## 📁 Project Structure

```
avengers-ai-agents/
├── agents.py          # Agent definitions, JARVIS orchestrator, mission runner
├── app.py             # Streamlit UI
├── run_mission.py     # CLI runner
├── requirements.txt   # Dependencies
├── .env.example       # API key template
└── README.md
```

---

## 💡 Example Missions

- `"Explain machine learning and write a simple classifier in Python"`
- `"What are the pros and cons of nuclear energy? Analyse both sides."`
- `"Research the history of the internet and summarise key milestones"`
- `"Write a Python REST API with Flask and explain each part"`
- `"Is social media harmful to democracy? Give a balanced analysis."`

---

## 🧠 Technical Details

- **Model**: `claude-sonnet-4-20250514` (Anthropic)
- **Pattern**: Multi-agent orchestration with specialised system prompts
- **Orchestration**: JARVIS uses structured JSON planning to route tasks
- **Memory**: Each agent operates independently; Nick Fury receives all context for synthesis
- **UI**: Streamlit with real-time agent status updates

---

## 🔑 API Key

Get your key at [console.anthropic.com](https://console.anthropic.com).
Store it in `.env` — never commit it to GitHub.

---

## 📄 License

MIT — build on it, fork it, make it your own.
