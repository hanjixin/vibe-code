from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent_core.graph.workflow import app as graph_app
from agent_core.core.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import os
import json
import re

app = FastAPI(title="Claude Code Agent SDK API")

class ChatRequest(BaseModel):
    message: str
    mode: str = "autonomy"
    thread_id: str = str(uuid.uuid4())

class FileSaveRequest(BaseModel):
    path: str
    content: str

def extract_content_from_event(event_value):
    """从事件值中提取消息内容"""
    try:
        value_str = str(event_value)
        
        # 尝试直接提取 AIMessage content
        aimessage_match = re.search(r"AIMessage\(content='([^']*)'", value_str)
        if aimessage_match:
            content = aimessage_match.group(1)
            # 解码转义字符
            content = content.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
            return content
        
        # 尝试从 messages 数组中提取
        if 'messages' in event_value and isinstance(event_value['messages'], list):
            for msg in event_value['messages']:
                if hasattr(msg, 'content'):
                    return msg.content
        
        return value_str
    except Exception:
        return str(event_value)

async def generate_events(request, use_post=True):
    """生成 SSE 事件流"""
    try:
        async for event in graph_app.astream(request["inputs"], config=request["config"]):
            for key, value in event.items():
                content = extract_content_from_event(value)
                event_data = {
                    "node": key,
                    "content": content
                }
                yield f"data: {json.dumps(event_data)}\n\n"
        yield f"data: {json.dumps({'type': 'end'})}\n\n"
    except Exception as e:
        error_data = {
            "type": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint to interact with the Multi-Agent System.
    """
    config = {
        "configurable": {"thread_id": request.thread_id},
        "recursion_limit": 100
    }
    
    inputs = {
        "messages": [HumanMessage(content=request.message)],
        "mode": request.mode,
        "iteration_count": 0
    }
    
    request_data = {"inputs": inputs, "config": config}
    
    return StreamingResponse(
        generate_events(request_data),
        media_type="text/event-stream"
    )

@app.get("/chat")
async def chat_get(
    message: str = Query(..., description="The user message"),
    mode: str = Query("autonomy", description="The work mode"),
    thread_id: str = Query(str(uuid.uuid4()), description="Thread ID")
):
    """
    Endpoint to interact with the Multi-Agent System (GET for SSE).
    """
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 100
    }
    
    inputs = {
        "messages": [HumanMessage(content=message)],
        "mode": mode,
        "iteration_count": 0
    }
    
    request_data = {"inputs": inputs, "config": config}
    
    return StreamingResponse(
        generate_events(request_data),
        media_type="text/event-stream"
    )

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
