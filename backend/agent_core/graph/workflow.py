from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agent_core.core.state import AgentState
from agent_core.agents.manager import ManagerAgent
from agent_core.agents.editor import EditorAgent
from agent_core.agents.verifier import VerifierAgent
from langchain_core.messages import HumanMessage, AIMessage

manager = ManagerAgent()
editor = EditorAgent()
verifier = VerifierAgent()

async def manager_node(state: AgentState):
    response = await manager.run(state)
    return {"messages": [AIMessage(content=response)]}

async def editor_node(state: AgentState):
    response = await editor.run(state)
    return {"messages": [AIMessage(content=response)]}

async def verifier_node(state: AgentState):
    response = await verifier.run(state)
    return {"messages": [AIMessage(content=response)]}

def should_end(state: AgentState):
    messages = state.get("messages", [])
    for msg in reversed(messages[-3:]):
        content = msg.content if hasattr(msg, 'content') else str(msg)
        if "STATUS_REPORT: success" in content:
            return END
    return "continue"

workflow = StateGraph(AgentState)

workflow.add_node("Manager", manager_node)
workflow.add_node("Editor", editor_node)
workflow.add_node("Verifier", verifier_node)

workflow.set_entry_point("Manager")

workflow.add_edge("Manager", "Editor")
workflow.add_edge("Editor", "Verifier")

workflow.add_conditional_edges(
    "Verifier",
    should_end,
    {
        END: END,
        "continue": END
    }
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
