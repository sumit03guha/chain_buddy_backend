from flask_restx import fields

from ..namespace.agent import agent_namespace

text_model = agent_namespace.model(
    "TextData",
    {
        "input": fields.String(required=True, description="Input text to be processed"),
        "conversation_id": fields.String(
            required=True, description="Identifier for the conversation thread"
        ),
    },
)
