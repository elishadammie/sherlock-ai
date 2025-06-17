# 🧠 Sherlock AI

**Conversational Agent for Querying, Visualizing, and Explaining Business Data**

---

## 🚀 Project Overview

An Agent-Powered Conversational BI Assistant

Sherlock AI is an advanced, conversational business intelligence (BI) assistant designed to bridge the gap between complex business data and natural language questions. It leverages a multi-agent system, orchestrated by LangGraph, to understand user queries, generate and execute SQL, synthesize insights, and create data visualizations on the fly.

✨ Core Features
- Natural Language to SQL: Ask complex questions like "What were the total sales for the top 5 countries?" and get immediate results.

- Agentic Reasoning: Utilizes a graph-based agent system that can reason about the steps needed to answer a question.

- Self-Correction: The agent can debug its own SQL queries. If a query fails, it analyzes the error and attempts to rewrite it correctly.

- Insight Synthesis: Goes beyond raw data by using an LLM to generate a clear, human-readable summary of the findings.

- Automatic Visualization: Intelligently chooses the best chart type (bar, pie, etc.) to visualize the data and generates a plot using Plotly.

- Interactive UI: A clean, modern, and user-friendly interface built with Streamlit that showcases the agent's full "thought process."

Built with LangChain, LangGraph, Plotly, SQLite, SQLAlchemy, OpenAI's GPT models, and a lightweight UI using Streamlit .

---

## 🛠️ Tech Stack

| Layer               | Stack                                                                 |
|---------------------|-----------------------------------------------------------------------|
| LLM Backbone        | OpenAI GPT-4 / GPT-3.5-turbo                                          |
| Agent Orchestration | LangChain + LangGraph                                                 |
| Embeddings          | FAISS / pgvector                                                      |
| Visualization       | Plotly Matplotlib                                                     |
| Backend             | Streamlit                                                             |
| Database            | SQLite                                                                |
| Tooling             | LangChain SQLToolkit, custom agents, JSON/Markdown exports            |
| Testing             | LangChain Tracer                                                      |

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
