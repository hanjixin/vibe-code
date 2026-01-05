from typing import List, Dict, Any, Optional
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock
from backend.claude_agent_sdk.core.state import AgentState
from backend.claude_agent_sdk.core.llm import ModelRouter

class BaseAgent:
    def __init__(self, name: str, mcp_servers: Dict[str, Any], allowed_tools: List[str], system_prompt: str):
        self.name = name
        self.mcp_servers = mcp_servers
        self.allowed_tools = allowed_tools
        self.system_prompt = system_prompt
        self.model_router = ModelRouter()

    async def run(self, state: AgentState) -> str:
        """
        Runs the agent using Claude Agent SDK.
        """
        # Get the last user message or relevant context
        messages = state.get("messages", [])
        if not messages:
            return "No messages to process."
        
        last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])

        # Determine model based on agent role
        if self.name == "Manager":
            model_name = self.model_router.get_model_name("reasoning")
        elif self.name == "Editor":
            model_name = self.model_router.get_model_name("coding")
        else:
            model_name = self.model_router.get_model_name("fast")

        options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            mcp_servers=self.mcp_servers,
            allowed_tools=self.allowed_tools,
            max_turns=10, # Limit turns for safety
            # model=model_name # Note: Claude Agent SDK might not support 'model' param in options yet, checking docs...
            # If SDK doesn't support model selection in options, it uses the CLI default.
            # Assuming for now we rely on CLI default or environment variables.
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
