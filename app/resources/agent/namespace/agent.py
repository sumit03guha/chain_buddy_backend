from flask_restx import Namespace

agent_namespace = Namespace("Agent", description="Agent related operations", path="/")
