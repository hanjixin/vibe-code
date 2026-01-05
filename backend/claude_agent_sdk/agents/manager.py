from backend.claude_agent_sdk.agents.base import BaseAgent
from backend.claude_agent_sdk.tools.server import get_planning_server

MANAGER_PROMPT = """You are the Manager Agent, responsible for the overall coordination and planning of the software development task.
Your goal is to understand the user's request, break it down into actionable steps, and delegate them to the Editor and Verifier agents.

You have access to the following tools:
- create_plan: To structure the workflow.
- delegate_task: To assign work to Editor or Verifier.
- search_web: To find information if needed.
- report_status: To report final completion.

Do not write code yourself. Focus on architecture and management.
When the entire task is done, use `report_status(status="success", details="All tasks completed")`.
"""

class ManagerAgent(BaseAgent):
    def __init__(self):
        planning_server = get_planning_server()
        super().__init__(
            name="Manager",
            mcp_servers={"planning": planning_server},
            allowed_tools=[
                "mcp__planning__create_plan", 
                "mcp__planning__delegate_task", 
                "mcp__planning__search_web",
                "mcp__planning__report_status"
            ],
            system_prompt=MANAGER_PROMPT
        )
