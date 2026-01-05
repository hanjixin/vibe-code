from claude_agent_sdk import tool
import os
import subprocess

@tool("read_file", "Reads a file from the filesystem", {"file_path": str})
async def read_file(args) -> dict:
    """Reads a file from the filesystem."""
    file_path = args["file_path"]
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": [{"type": "text", "text": content}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error reading file: {str(e)}"}]}

@tool("write_file", "Writes content to a file", {"file_path": str, "content": str})
async def write_file(args) -> dict:
    """Writes content to a file."""
    file_path = args["file_path"]
    content = args["content"]
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return {"content": [{"type": "text", "text": f"Successfully wrote to {file_path}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error writing file: {str(e)}"}]}

@tool("run_shell_command", "Runs a shell command", {"command": str})
async def run_shell_command(args) -> dict:
    """Runs a shell command in the sandbox environment."""
    command = args["command"]
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return {"content": [{"type": "text", "text": output}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error executing command: {str(e)}"}]}

@tool("list_directory", "Lists files in a directory", {"path": str})
async def list_directory(args) -> dict:
    """Lists files in a directory."""
    path = args.get("path", ".")
    try:
        files = str(os.listdir(path))
        return {"content": [{"type": "text", "text": files}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error listing directory: {str(e)}"}]}

@tool("git_commit", "Commits changes to git", {"message": str})
async def git_commit(args) -> dict:
    """Commits changes to git."""
    message = args["message"]
    try:
        subprocess.run("git add .", shell=True, check=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, check=True)
        return {"content": [{"type": "text", "text": f"Successfully committed with message: {message}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error committing: {str(e)}"}]}

@tool("git_reset", "Resets git to previous commit", {"hard": bool})
async def git_reset(args) -> dict:
    """Resets git to previous commit."""
    hard = args.get("hard", False)
    try:
        cmd = "git reset --hard HEAD~1" if hard else "git reset HEAD~1"
        subprocess.run(cmd, shell=True, check=True)
        return {"content": [{"type": "text", "text": "Successfully reset to previous commit."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error resetting: {str(e)}"}]}
