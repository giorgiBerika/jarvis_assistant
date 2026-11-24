import json

from core.memory import recall_facts, recent_messages, log_message, remember_fact
from core.llm import LLMMessage


# Local Tool Schema for remember fact
REMEMBER_FACT_TOOL = {
    "type": "function",
    "function": {
        "name": "remember_fact",
        "description": "Save a fact about the user to long-term memory for future conversations.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Short label for the fact, e.g. 'name'"},
                "value": {"type": "string", "description": "The fact's value, e.g. 'Giorgi'"},
            },
            "required": ["key", "value"],
        },
    },
}

LOCAL_TOOLS = {
    'remember_fact': remember_fact
}

async def run_turn(hub, llm_client, user_message: str) -> str:
    facts = recall_facts()
    history = recent_messages(limit=10)

    system_prompt = f"You are a helpful personal assistant. Known facts about the user: {facts}"
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": user_message},
    ]

    log_message("user", user_message)

    tools = hub.get_tools_for_llm() + [REMEMBER_FACT_TOOL]

    while True:
        reply: LLMMessage = llm_client.chat(messages, tools)

        if not reply.tool_calls:
            log_message("assistant", reply.content)
            return reply.content

      
        messages.append({
            "role": "assistant",
            "content": reply.content,
            "tool_calls": [
                {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": tc.arguments}}
                for tc in reply.tool_calls
            ],
        })

        for tc in reply.tool_calls:
            args = json.loads(tc.arguments)

            if tc.name in LOCAL_TOOLS:
                result = LOCAL_TOOLS[tc.name](**args)  # Direct function calling, no MCP
            else:
                result = await hub.call_tool(tc.name, args)  # Otherwise - MCP

            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})