from agent_core.agents.base import BaseAgent
from agent_core.tools.server import get_filesystem_server

EDITOR_PROMPT = """You are the Editor Agent, responsible for writing code and managing files.
You are the "Hands" of the system.

Your capabilities:
- Read and write files.
- Execute shell commands (install dependencies, run scripts).
- Navigate the file system.
- Manage version control (git commit, git reset).

Follow the plan provided by the Manager. Ensure code quality and adhere to the project structure.
When a significant task is completed, create a checkpoint using git_commit.
"""

class EditorAgent(BaseAgent):
    def __init__(self):
        fs_server = get_filesystem_server()
        super().__init__(
            name="Editor",
            mcp_servers={"filesystem": fs_server},
            allowed_tools=[
                "mcp__filesystem__read_file", 
                "mcp__filesystem__write_file", 
                "mcp__filesystem__run_shell_command", 
                "mcp__filesystem__list_directory",
                "mcp__filesystem__git_commit",
                "mcp__filesystem__git_reset"
            ],
            system_prompt=EDITOR_PROMPT
        )
