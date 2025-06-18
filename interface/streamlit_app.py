# insightgpt/interface/streamlit_app.py

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the project root to the Python path to allow for absolute imports
# This is a robust way to handle imports in a Streamlit app
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.langgraph_flow import app

# --- Page Configuration ---
st.set_page_config(
    page_title="Sherlock AI",
    page_icon="🧠",
    layout="wide"
)

# --- Application Title and Description ---
st.title("🧠 Sherlock AI")
st.markdown("""
Welcome to Sherlock AI, your conversational business intelligence partner. 
Ask a question about the Chinook database, and Sherlock will find the answer, generate insights, and visualize the data for you.
""")

# --- Session State Initialization ---
# This is crucial for maintaining the conversation history.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you analyze the Chinook database today?"}
    ]

# --- Display Chat History ---
# Loop through the session state to display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Check if the content is a dictionary (our special format) or just text
        if isinstance(message["content"], dict):
            # Display all the artifacts from the agent's response
            st.write(message["content"]["final_answer"])
            if message["content"]["chart_image"]:
                st.image(message["content"]["chart_image"], caption="Generated Chart")
            
            with st.expander("Show the agent's work"):
                st.code(message["content"]["sql_query"], language="sql")
                st.dataframe(pd.DataFrame(message["content"]["raw_result"]))
        else:
            st.write(message["content"])


# --- User Input Handling ---
# Use st.chat_input for a clean, persistent input box at the bottom
if prompt := st.chat_input("Ask a question, e.g., 'What are the top 5 selling artists?'"):
    # Add user's message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # --- Invoke the Backend Graph ---
    # Display a spinner while the agent is working
    with st.chat_message("assistant"):
        with st.spinner("Sherlock is on the case..."):
            
            # Prepare the input for the LangGraph app
            # We pass the entire message history for conversational context
            initial_state = {"messages": st.session_state.messages}
            
            # A unique thread ID for each user session could be used here.
            # For simplicity, we'll use a single thread ID.
            config = {"configurable": {"thread_id": "user-session-1"}}

            # Invoke the graph
            final_state = app.invoke(initial_state, config=config)

            # --- Extract and Display the Results ---
            # We bundle all results into a single dictionary to store in the session state
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
                st.dataframe(pd.DataFrame(assistant_response["raw_result"]))
            
            # Add the full assistant response to the session state
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})