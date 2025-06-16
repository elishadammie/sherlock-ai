# sherlock-ai/app/agents/sql_agent.py

import os
import httpx  # <-- 1. IMPORT httpx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Imports from other project files remain the same
from app.state import AgentState
from app.agents.schema_retriever import get_enhanced_schema

# Load environment variables from .env file
load_dotenv()

# Ensure the OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def create_sql_generator_prompt() -> ChatPromptTemplate:
    """
    Creates the prompt template for the SQL generation agent.
    
    This prompt combines a fixed system message with our enhanced schema
    and a placeholder for the user's question and conversation history.
    """
    # Get the enhanced schema with business context
    enhanced_schema = get_enhanced_schema()
    
    # Define the system message template
    system_template = f"""
You are an expert SQL analyst. Your sole purpose is to write a single, valid SQLite SQL query to answer the user's question.

- You must use the following database schema to form your query.
- Do not use any tables or columns not listed in this schema.
- Pay close attention to the business descriptions for each table and column, as they contain critical hints about how the data is organized.

**DATABASE SCHEMA:**
{enhanced_schema}

**INSTRUCTIONS:**
1.  Analyze the user's question and the conversation history.
2.  Write a single, syntactically correct SQLite SQL query that directly answers the question.
3.  **IMPORTANT**: You must only respond with the SQL query itself. Do not include any other text, explanations, or markdown formatting (like ```sql).
"""
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        HumanMessagePromptTemplate.from_template("{messages}")
    ])
    
    return prompt

def sql_generator_agent(state: AgentState) -> dict:
    """
    This agent node generates the SQL query.

    Args:
        state: The current application state.

    Returns:
        A dictionary with the updated state.
    """
    print("---EXECUTING SQL GENERATOR AGENT---")
    
    # --- START: SSL VERIFICATION FIX ---
    # 2. Create a custom httpx client with SSL verification disabled.
    http_client = httpx.Client(verify=False)
    # --- END: SSL VERIFICATION FIX ---
    
    # Initialize the ChatOpenAI model
    # 3. Pass the custom http_client to the ChatOpenAI constructor.
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, http_client=http_client)
    
    # Create the prompt
    sql_prompt = create_sql_generator_prompt()
    
    # Create the chain
    sql_chain = sql_prompt | llm
    
    # The `MessagesState` is a list, so we pass it directly
    response = sql_chain.invoke({"messages": state['messages']})
    
    generated_sql = response.content
    print(f"Generated SQL:\n{generated_sql}")
    
    # Update the state with the generated SQL query
    return {"sql_query": generated_sql}

if __name__ == '__main__':
    # This block allows for independent testing of the agent
    from langchain_core.messages import HumanMessage
    from langgraph.graph.message import MessagesState
    
    # A sample state for testing. We now correctly initialize MessagesState.
    test_state = AgentState(
        user_query="How many employees are there?",
        # FIX: Explicitly create a MessagesState instance
        messages=MessagesState(messages=[HumanMessage(content="How many employees are there?")]),
        sql_query=None,
        sql_error=None,
        raw_result=None,
        final_answer=None,
        chart_image=None
    )
    
    # Run the agent
    result = sql_generator_agent(test_state)
    
    print("\n---Agent Output---")
    print(result)

    # Verify the output
    assert 'sql_query' in result, "Agent did not return a SQL query."
    assert result['sql_query'].strip().upper().startswith("SELECT COUNT"), "Generated SQL is not as expected."
    
    print("\nAgent test successful!")