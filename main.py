import asyncio
import os

from mcp import StdioServerParameters

from core.mcp_client import MCPToolHub
from core.llm import GroqLLMClient
from core.orchestrator import run_turn
from core.stt import get_user_input
from core.tts import speak, speak_gtts


# Necessary env variables
gui_env = {
    "DISPLAY": os.environ.get("DISPLAY", ""),
    "DBUS_SESSION_BUS_ADDRESS": os.environ.get("DBUS_SESSION_BUS_ADDRESS", ""),
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
}

async def main():
    hub = MCPToolHub()
    await hub.start([
        StdioServerParameters(command="python3", args=["servers/system_info/server.py"]),
        StdioServerParameters(command="python3", 
                            args=["servers/system_control/server.py"],
                            env=gui_env,),
        StdioServerParameters(command="python3", args=["servers/web_search/server.py"])
    ])

    llm_client = GroqLLMClient()

    try:
        while True:
            user_input = get_user_input()
            answer = await run_turn(hub, llm_client, user_input)
            speak_gtts(answer)
    finally:
        await hub.close()


if __name__ == "__main__":
    asyncio.run(main())