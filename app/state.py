# sherlock-ai/app/state.py

from typing import Any, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import MessagesState

class AgentState(TypedDict):
    """
    Represents the state of our Sherlock AI agent.
    This structure is passed between nodes in the graph.
    """
    user_query: str
    
    # The `MessagesState` type is a list of messages that is automatically
    # updated by LangGraph's tool-calling nodes.
    messages: MessagesState
    
    # These fields will be populated as the agent runs
    sql_query: Optional[str]
    sql_error: Optional[str]
    raw_result: Optional[Any]
    final_answer: Optional[str]
    chart_image: Optional[bytes]
    