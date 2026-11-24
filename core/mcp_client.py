import json 
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPToolHub:
    def __init__(self):
        self._stack = AsyncExitStack()
        self._sessions: dict[str, ClientSession] = {}  # tool name -> owning session
        self._tools_for_llm: list[dict] = []

    async def start(self, server_commands: list[StdioServerParameters]) -> None:
        for params in server_commands:
            read, write = await self._stack.enter_async_context(stdio_client(params))
            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                self._sessions[tool.name] = session
                self._tools_for_llm.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                })

    def get_tools_for_llm(self) -> list[dict]:
        return self._tools_for_llm

    async def call_tool(self, name: str, arguments: dict) -> str:
        session = self._sessions[name]
        result = await session.call_tool(name, arguments)
        return json.dumps(result.structuredContent)

    async def close(self) -> None:
        await self._stack.aclose()