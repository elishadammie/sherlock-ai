# 🧠 Sherlock AI

**Conversational Agent for Querying, Visualizing, and Explaining Business Data**

---

## 🚀 Project Overview

Sherlock AI is an agent-powered analytics assistant that lets users query structured business data using natural language. It automatically:

- Generates SQL queries
- Executes them on a demo PostgreSQL/SQLite database
- Visualizes results
- Explains insights in plain English

Built with LangChain, LangGraph, OpenAI's GPT models, and a lightweight UI using Streamlit or FastAPI.

---

## 🛠️ Tech Stack

| Layer               | Stack                                                                 |
|---------------------|-----------------------------------------------------------------------|
| LLM Backbone        | OpenAI GPT-4 / GPT-3.5-turbo                                          |
| Agent Orchestration | LangChain + LangGraph                                                 |
| Embeddings          | FAISS / pgvector                                                      |
| Visualization       | Plotly, Altair, Matplotlib                                            |
| Backend             | Streamlit or FastAPI                                                  |
| Database            | PostgreSQL (preferred) or SQLite                                      |
| Tooling             | LangChain SQLToolkit, custom agents, JSON/Markdown exports            |
| Testing             | Pytest, LangChain Tracer                                              |

---

## 🧱 Folder Structure

```

sherlock-ai/
├── app/                 # Core logic, agents, and tools
├── database/            # Schema, data seeds, connectors
├── interface/           # Streamlit or FastAPI front-end
├── prompts/             # Custom prompt templates
├── tests/               # Unit and integration tests
├── export/              # Markdown/HTML report outputs
├── data/                # Local SQLite DB or CSV mock data
├── .env                 # API keys and DB config
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Packaging (optional)
└── README.md

````

The database used for this demo is the popular chinook database it is available for download here https://www.sqlitetutorial.net/sqlite-sample-database/

---

## ⚙️ Quick Start

```bash
# Clone the repo
git clone https://github.com/elishadammie/sherlock-ai.git
cd sherlock-ai

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
````

---

## ✅ Project Goals

* Ask questions like **"Compare Q1 and Q2 revenue trends"**
* Get:

  * 📊 SQL query + execution
  * 📈 Visual chart (e.g., line or bar)
  * 💬 AI-generated explanation

---

## 📄 License

MIT License

````

---
