from claude_agent_sdk import create_sdk_mcp_server
from backend.claude_agent_sdk.tools.filesystem import read_file, write_file, run_shell_command, list_directory, git_commit, git_reset
from backend.claude_agent_sdk.tools.browser import open_url, click_element, fill_form, take_screenshot, get_page_content
from backend.claude_agent_sdk.tools.planning import create_plan, delegate_task, search_web, report_status

def get_filesystem_server():
    return create_sdk_mcp_server(
        name="filesystem-tools",
        version="1.0.0",
        tools=[read_file, write_file, run_shell_command, list_directory, git_commit, git_reset]
    )

def get_browser_server():
    return create_sdk_mcp_server(
        name="browser-tools",
        version="1.0.0",
        tools=[open_url, click_element, fill_form, take_screenshot, get_page_content]
    )

def get_planning_server():
    return create_sdk_mcp_server(
        name="planning-tools",
        version="1.0.0",
        tools=[create_plan, delegate_task, search_web, report_status]
    )
