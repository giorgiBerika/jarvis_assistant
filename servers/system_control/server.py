from mcp.server.fastmcp import FastMCP
from pathlib import Path 
import subprocess


mcp = FastMCP("system-control")

ALLOWED_DIRS = [
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Desktop",
]


@mcp.tool()
def open_path(path: str) -> str:
    """
    Open a file or folder using the system's default application.
    Only works for paths inside allowed directories (Documents, Downloads, Desktop).
    Args:
        path: Absolute or ~-relative path to a file or folder.
    """

    resolved = Path(path).expanduser().resolve()

    if not resolved.exists():
        return f"Error: {resolved} does not exist."

    if not any(resolved.is_relative_to(allowed) for allowed in ALLOWED_DIRS):
        return f"Error: {resolved} is outside allowed directories."  

    # subprocess.run(["xdg-open", str(resolved)])
    subprocess.run(
        ["xdg-open", str(resolved)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return f"Opened {resolved}"


if __name__ == "__main__":
    mcp.run()