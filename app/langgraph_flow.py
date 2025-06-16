# sherlock-ai/app/langgraph_flow.py

from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, END

# Using relative imports as this is part of a package
from .state import AgentState
from .agents.sql_agent import sql_generator_agent
from .tools.query_executor import execute_sql_tool
from .agents.insight_explainer import generate_final_answer # <-- NEW: Import our new agent

# 1. Define the Nodes
def sql_executor_node(state: AgentState) -> dict:
    print("---EXECUTING SQL QUERY (CUSTOM NODE)---")
    query = state.get('sql_query')
    if query is None:
        error_message = "Error: No SQL query found in state."
        return { "messages": [ToolMessage(content=error_message, tool_call_id="")], "raw_result": error_message }
    result = execute_sql_tool.invoke({"query": query})
    tool_message = ToolMessage(content=result, name="execute_sql_tool", tool_call_id="sql_execution")
    return { "messages": [tool_message], "raw_result": result }

# 2. Define the Edges
def decide_next_step(state: AgentState) -> str:
    print("---DECIDING NEXT STEP---")
    last_message = state['messages'][-1]  # type: ignore
    if isinstance(last_message.content, str) and "Error" in last_message.content:
        print("SQL execution failed. Looping back for correction.")
        return "sql_generator"
    else:
        print("SQL execution successful. Proceeding to synthesize answer.")
        return "answer_synthesizer" # <-- CHANGED: Go to the new node instead of END

# 3. Assemble the Graph
workflow = StateGraph(AgentState)
workflow.add_node("sql_generator", sql_generator_agent)
workflow.add_node("sql_executor", sql_executor_node)
workflow.add_node("answer_synthesizer", generate_final_answer) # <-- NEW: Add the new node

workflow.set_entry_point("sql_generator")
workflow.add_edge("sql_generator", "sql_executor")

workflow.add_conditional_edges(
    source="sql_executor",
    path=decide_next_step,
    path_map={"sql_generator": "sql_generator", "answer_synthesizer": "answer_synthesizer"} # <-- CHANGED: Update path map
)

# NEW: Add a final edge from the synthesizer to the end of the graph
workflow.add_edge("answer_synthesizer", END)

app = workflow.compile()


if __name__ == '__main__':
    from dotenv import load_dotenv
    from langchain_core.messages import HumanMessage

    load_dotenv()
    print("--- Running Graph ---")

    question = "How many employees are there?"
    initial_state = { "messages": [HumanMessage(content=question)] }

    print("\n--- Invoking Graph ---")
    final_state = app.invoke(initial_state)

    print("\n--- Final Result ---")
    # CHANGED: Print the 'final_answer' instead of the raw result
    final_result = final_state.get('final_answer', 'No result found.')
    print(final_result)

    # final_state = None
    # for state_chunk in app.stream(initial_state):
    #     print("--- State Chunk ---")
    #     print(state_chunk)
    #     print("\n")
    #     final_state = state_chunk

    # print("--- Final Result ---")
    # if final_state:
    #     end_state = final_state.get('__end__', {})
    #     final_result = end_state.get('raw_result', 'No result found.')
    #     print(final_result)
    
