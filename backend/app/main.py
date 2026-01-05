from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from claude_agent_sdk.graph.workflow import app as graph_app
from claude_agent_sdk.core.state import AgentState
from langchain_core.messages import HumanMessage
import uuid
import os

app = FastAPI(title="Claude Code Agent SDK API")

class ChatRequest(BaseModel):
    message: str
    mode: str = "autonomy"
    thread_id: str = str(uuid.uuid4())

class FileSaveRequest(BaseModel):
    path: str
    content: str

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

# --- File System APIs ---

@app.get("/files/tree")
def get_file_tree(path: str = "."):
    """
    Recursively gets the file tree of the current directory.
    """
    def build_tree(dir_path):
        tree = []
        try:
            items = sorted(os.listdir(dir_path))
            for item in items:
                if item.startswith(".") and item != ".gitignore": continue # Skip hidden files except gitignore
                if item == "__pycache__": continue
                if item == "node_modules": continue
                
                full_path = os.path.join(dir_path, item)
                is_dir = os.path.isdir(full_path)
                
                node = {
                    "name": item,
                    "path": full_path,
                    "type": "directory" if is_dir else "file",
                    "children": build_tree(full_path) if is_dir else None
                }
                tree.append(node)
        except PermissionError:
            pass
        return tree

    return build_tree(path)

@app.get("/files/content")
def get_file_content(path: str):
    """
    Reads the content of a file.
    """
    try:
        with open(path, 'r') as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/files/save")
def save_file(request: FileSaveRequest):
    """
    Saves content to a file.
    """
    try:
        with open(request.path, 'w') as f:
            f.write(request.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
