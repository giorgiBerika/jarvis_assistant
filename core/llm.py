from abc import ABC, abstractmethod
from dataclasses import dataclass, field 

from groq import Groq
from ..config import GROQ_API_KEY

@dataclass
class ToolCall:
    id: str 
    name: str 
    arguements: str # raw JSON string , same as MCP server expects


@dataclass
class LLMMessage:
    content: str | None 
    tool_calls: list[ToolCall] = field(default_factory=list)


class LLMClient(ABC):

    @abstractmethod
    def chat(self, messages: list[dict], tools: list[dict]) -> LLMMessage:
        """Send conversation history + available tools, get back a normalized reply."""
        ...


class GroqLLMClient(LLMClient):
    def __init__(self, model: str = "openai/gpt-oss-120b"):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = model 

    def chat(self, messages: list[dict], tools: list[dict]) -> LLMMessage:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools
        )

        raw = response.choices[0].message 

        tool_calls = [
            ToolCall(id=tc.id, name=tc.function.name, arguements=tc.function.arguments)
            for tc in (raw.tool_calls or [])
        ]

        return LLMMessage(content=raw.content, tool_calls=tool_calls)