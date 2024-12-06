from tkinter import S
from typing import Iterator

from langchain_core.messages import HumanMessage

from app.adapter.sse_formatter import format_server_sent_event
from app.constants.sse import SSEType


def run_agent(input, agent_executor, config) -> Iterator[str]:
    """Run the agent and yield formatted SSE messages"""
    print("RUNNING AGENT", flush=True)
    try:
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=input)]}, config
        ):
            if "agent" in chunk:
                content = chunk["agent"]["messages"][0].content
                if content:
                    yield format_server_sent_event(content, SSEType.AGENT.value)
            elif "tools" in chunk:
                name = chunk["tools"]["messages"][0].name
                content = chunk["tools"]["messages"][0].content
                if content:
                    yield format_server_sent_event(
                        content, SSEType.TOOLS.value, functions=[name]
                    )

    except Exception as e:
        yield format_server_sent_event(f"Error: {str(e)}", SSEType.ERROR.value)
