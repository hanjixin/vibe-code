from typing import TypedDict, List, Optional, Dict, Any, Annotated
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Global state for the Multi-Agent System.
    """
    # Chat history
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Current plan/task breakdown
    plan: Optional[List[Dict[str, Any]]]
    
    # Current active agent
    next_agent: Optional[str]
    
    # Context (file snapshots, diffs, etc.)
    code_context: Dict[str, Any]
    
    # Verification results (test reports, screenshots)
    verification_results: Dict[str, Any]
    
    # System mode (Build, Plan, Fast, Autonomy)
    mode: str
    
    # Iteration count for autonomy limits
    iteration_count: int
