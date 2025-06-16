# insightgpt/interface/streamlit_app.py

import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# --- 1. SETUP ---
# Load environment variables from .env file
load_dotenv()
# Add project root to Python path for reliable imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from app.langgraph_flow import app

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Sherlock AI", layout="wide")

# --- 3. CUSTOM CSS INJECTION ---
# Function to load and inject the CSS file
def load_custom_css():
    css_file = project_root / "interface" / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

# --- 4. SESSION STATE INITIALIZATION ---
# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. STATIC UI LAYOUT (HEADER) ---
# This HTML block creates the persistent header.
use_blinking_dot = os.getenv("ENABLE_BLINKING_DOT", "false").lower() == "true"
blinking_class = "blinking-dot" if use_blinking_dot else ""

st.markdown(f"""
    <header class="header">
        <div class="header-title">Sherlock AI</div>
        <div class="status-indicator">
            <span class="status-dot {blinking_class}"></span>
            Database Connected
        </div>
    </header>
""", unsafe_allow_html=True)

# --- 6. CONDITIONAL WELCOME MESSAGE ---
# Display the centered "Hello, Elisha" message only if the chat is empty.
if not st.session_state.messages:
    st.markdown("""
        <div class="main-container">
            <div class="welcome-message">
                Hello, <span style='color: #89b3f7;'>Eli</span><span style='color: #ef476f;'>sha</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. CHAT HISTORY DISPLAY ---
# This will display the conversation history below the welcome message once it starts.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, dict):
            # Display structured response from the agent
            st.write(content.get("final_answer"))
            if content.get("chart_image"):
                st.image(content["chart_image"], caption="Generated Chart")
            with st.expander("Show the agent's work"):
                st.code(content.get("sql_query"), language="sql")
                raw_result = content.get("raw_result")
                if isinstance(raw_result, list) and raw_result:
                    st.dataframe(pd.DataFrame(raw_result))
                else:
                    st.write(raw_result)
        else:
            st.write(content)

if prompt := st.chat_input("Ask Sherlock AI..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})

    # To re-render the whole page with the new message
    st.rerun()

# This logic runs if the last message is from the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        with st.spinner("Sherlock is on the case..."):
            initial_state = {"messages": [{"role": "user", "content": user_prompt}]}
            config = {"configurable": {"thread_id": "user-session-1"}}
            
            # Call the backend graph
            # Add "# type: ignore" to suppress the linter's false positive error
            final_state = app.invoke(initial_state, config=config) # type: ignore
            
            # Bundle the results
            assistant_response = {
                "final_answer": final_state.get('final_answer', "I couldn't find an answer."),
                "chart_image": final_state.get('chart_image'),
                "sql_query": final_state.get('sql_query'),
                "raw_result": final_state.get('raw_result')
            }
            
            # Display the structured response
            st.write(assistant_response["final_answer"])
            if assistant_response["chart_image"]:
                st.image(assistant_response["chart_image"], caption="Generated Chart")
            with st.expander("Show the agent's work"):
                st.code(assistant_response["sql_query"], language="sql")
                if isinstance(assistant_response["raw_result"], list) and assistant_response["raw_result"]:
                    st.dataframe(pd.DataFrame(assistant_response["raw_result"]))
                else:
                    st.write(assistant_response["raw_result"])
            
            # Add the full assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
