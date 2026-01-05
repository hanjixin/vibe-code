from langgraph.graph import StateGraph, END, MemorySaver
from backend.claude_agent_sdk.core.state import AgentState
from backend.claude_agent_sdk.agents.manager import ManagerAgent
from backend.claude_agent_sdk.agents.editor import EditorAgent
from backend.claude_agent_sdk.agents.verifier import VerifierAgent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize Agents
manager = ManagerAgent()
editor = EditorAgent()
verifier = VerifierAgent()

# Define Nodes
async def manager_node(state: AgentState):
    response = await manager.run(state)
    return {"messages": [AIMessage(content=response)], "next_agent": "Editor"}

async def editor_node(state: AgentState):
    response = await editor.run(state)
    return {"messages": [AIMessage(content=response)], "next_agent": "Verifier"}

async def verifier_node(state: AgentState):
    response = await verifier.run(state)
    # The response text might contain "STATUS_REPORT: success" or "STATUS_REPORT: failure"
    # We can parse this to decide the next step.
    # Note: In a real implementation, we might want to inspect tool calls directly,
    # but since BaseAgent.run returns text, we rely on the text output from the tool.
    
    if "STATUS_REPORT: success" in response:
        return {"messages": [AIMessage(content=response)], "verification_results": {"status": "success"}, "next_agent": "Manager"}
    elif "STATUS_REPORT: failure" in response:
        return {"messages": [AIMessage(content=response)], "verification_results": {"status": "failure"}, "next_agent": "Editor"}
    else:
        # Default fallback if no status reported
        return {"messages": [AIMessage(content=response)], "next_agent": "Manager"}

# Conditional Edge Logic
def should_continue(state: AgentState):
    """
    Determines the next node based on the verification results.
    """
    last_message = state["messages"][-1].content
    
    if "STATUS_REPORT: success" in last_message:
        return "Manager"
    elif "STATUS_REPORT: failure" in last_message:
        return "Editor"
    else:
        return "Manager" # Default

# Define Graph
workflow = StateGraph(AgentState)

workflow.add_node("Manager", manager_node)
workflow.add_node("Editor", editor_node)
workflow.add_node("Verifier", verifier_node)

workflow.set_entry_point("Manager")

# Define Edges
workflow.add_edge("Manager", "Editor")
workflow.add_edge("Editor", "Verifier")

# Conditional edge from Verifier
workflow.add_conditional_edges(
    "Verifier",
    should_continue,
    {
        "Manager": "Manager",
        "Editor": "Editor"
    }
)

# Checkpointer
memory = MemorySaver()

# Compile
app = workflow.compile(checkpointer=memory)
