from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.claude_agent_sdk.graph.workflow import app as graph_app
from backend.claude_agent_sdk.core.state import AgentState
from langchain_core.messages import HumanMessage
import uuid

app = FastAPI(title="Claude Code Agent SDK API")

class ChatRequest(BaseModel):
    message: str
    mode: str = "autonomy"
    thread_id: str = str(uuid.uuid4())

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint to interact with the Multi-Agent System.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    inputs = {
        "messages": [HumanMessage(content=request.message)],
        "mode": request.mode,
        "iteration_count": 0
    }
    
    try:
        # Stream the output
        output = []
        async for event in graph_app.astream(inputs, config=config):
            for key, value in event.items():
                output.append({
                    "node": key,
                    "content": str(value) # Serialize for JSON
                })
        return {"status": "success", "thread_id": request.thread_id, "trace": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}
