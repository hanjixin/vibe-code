from claude_agent_sdk import tool
from typing import List
from duckduckgo_search import DDGS

@tool("create_plan", "Creates a structured plan of tasks", {"tasks": list})
async def create_plan(args) -> dict:
    """Creates a structured plan of tasks."""
    tasks = args["tasks"]
    return {"content": [{"type": "text", "text": f"Plan created with {len(tasks)} tasks."}]}

@tool("delegate_task", "Delegates a specific task to a sub-agent", {"agent_name": str, "task_description": str})
async def delegate_task(args) -> dict:
    """Delegates a specific task to a sub-agent (Editor or Verifier)."""
    agent_name = args["agent_name"]
    task_description = args["task_description"]
    return {"content": [{"type": "text", "text": f"Delegated to {agent_name}: {task_description}"}]}

@tool("search_web", "Searches the web for documentation or information", {"query": str})
async def search_web(args) -> dict:
    """Searches the web for documentation or information using DuckDuckGo."""
    query = args["query"]
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        formatted_results = "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
        return {"content": [{"type": "text", "text": f"Search results for '{query}':\n{formatted_results}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error searching web: {str(e)}"}]}

@tool("report_status", "Reports the status of the current task", {"status": str, "details": str})
async def report_status(args) -> dict:
    """
    Reports the status of the current task.
    status: 'success' or 'failure'
    details: Description of the outcome or error.
    """
    status = args["status"]
    details = args["details"]
    # This tool's output will be used by the graph to decide the next step
    return {"content": [{"type": "text", "text": f"STATUS_REPORT: {status} - {details}"}]}
