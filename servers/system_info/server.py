from mcp.server.fastmcp import FastMCP
from datetime import datetime
import psutil


mcp = FastMCP("system_info")


@mcp.tool()
def get_current_datetime() -> str:
    """Get the current local date and time"""
    return datetime.now().isoformat()


@mcp.tool()
def list_running_processes(limit: int = 10) -> list[dict]:
    """
    List currently running processes on this machine.
    Args:
        limit: The maximum number of processes.
    """
    processes = []
    for proc in psutil.process_iter(["pid", "name"]):
        processes.append(proc.info)
        if len(processes) >= limit:
            break 
    return processes

if __name__ == "__main__":
    mcp.run()