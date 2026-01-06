from typing import List, Dict, Any, Optional
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock
from agent_core.core.state import AgentState
from agent_core.core.llm import ModelRouter
import shutil

class BaseAgent:
    def __init__(self, name: str, mcp_servers: Dict[str, Any], allowed_tools: List[str], system_prompt: str):
        self.name = name
        self.mcp_servers = mcp_servers
        self.allowed_tools = allowed_tools
        self.system_prompt = system_prompt
        self.model_router = ModelRouter()

    def _get_cli_path(self) -> str:
        cli_path = shutil.which("claude") or shutil.which("claude-code")
        if cli_path:
            return cli_path
        return "/usr/local/bin/claude"

    async def run(self, state: AgentState) -> str:
        messages = state.get("messages", [])
        if not messages:
            return "No messages to process."
        
        last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])

        cli_path = self._get_cli_path()
        
        options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            mcp_servers=self.mcp_servers,
            allowed_tools=self.allowed_tools,
            max_turns=10,
            cli_path=cli_path
        )

        response_text = ""
        
        try:
            async with ClaudeSDKClient(options=options) as client:
                await client.query(last_message)

                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                response_text += block.text
        except Exception as e:
            return f"Error running agent {self.name}: {str(e)}"

        return response_text
