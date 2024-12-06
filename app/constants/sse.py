from enum import Enum


class SSEType(Enum):
    AGENT = "agent"
    TOOLS = "tools"
    ERROR = "error"
    COMPLETED = "completed"
