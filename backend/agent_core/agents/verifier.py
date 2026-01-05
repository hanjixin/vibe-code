from agent_core.agents.base import BaseAgent
from agent_core.tools.server import get_browser_server, get_planning_server

VERIFIER_PROMPT = """You are the Verifier Agent, responsible for quality assurance and testing.
You are the "Eyes" of the system.

Your capabilities:
- Perform REAL browser automation using Playwright (open URLs, click, fill forms, get content).
- Take screenshots to verify UI.
- Report task status using `report_status`.

Verify the work done by the Editor. 
1. If the verification passes, call `report_status(status="success", details="Verification passed...")`.
2. If the verification fails, call `report_status(status="failure", details="Verification failed because...")`.

Use `get_page_content` to verify text on the page.
"""

class VerifierAgent(BaseAgent):
    def __init__(self):
        browser_server = get_browser_server()
        planning_server = get_planning_server() # For report_status
        
        # Merge servers
        servers = {"browser": browser_server, "planning": planning_server}
        
        super().__init__(
            name="Verifier",
            mcp_servers=servers,
            allowed_tools=[
                "mcp__browser__open_url", 
                "mcp__browser__click_element", 
                "mcp__browser__fill_form", 
                "mcp__browser__take_screenshot", 
                "mcp__browser__get_page_content",
                "mcp__planning__report_status"
            ],
            system_prompt=VERIFIER_PROMPT
        )
