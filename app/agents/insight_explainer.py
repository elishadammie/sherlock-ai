# insightgpt/app/agents/insight_explainer.py

import httpx
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.state import AgentState

def generate_final_answer(state: AgentState) -> dict:
    """
    Generates a final, human-readable answer based on the query result.
    This version is improved by including the SQL query in the prompt for context.
    """
    print("---GENERATING FINAL ANSWER---")
    
    # --- IMPROVED PROMPT ---
    # We now include the SQL query to give the LLM full context.
    prompt_template = """
Given the user's original question, the corresponding SQL query, and the data result from that query, formulate a friendly, natural language answer.

Original Question: {question}
SQL Query: {sql_query}
Data Result: {result}

Synthesize a final, conversational, and confident answer. Be direct and avoid generic phrases like "It looks like".
"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Using the same SSL fix for this LLM call
    http_client = httpx.Client(verify=False)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, http_client=http_client)
    
    chain = prompt | llm
    
    # Get all the necessary context from the state
    original_question = state['messages'][0].content  # type: ignore
    sql_query = state.get('sql_query')
    raw_result = state.get('raw_result')
    
    # Invoke the chain to get the final answer
    response = chain.invoke({
        "question": original_question,
        "sql_query": sql_query,
        "result": str(raw_result)
    })
    
    final_answer = response.content
    print(f"Synthesized Answer: {final_answer}")
    
    return {"final_answer": final_answer}