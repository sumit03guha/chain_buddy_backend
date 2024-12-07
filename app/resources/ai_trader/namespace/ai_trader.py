from flask_restx import Namespace

ai_trader_namespace = Namespace(
    "AI Trader", description="AI Trader related operations", path="/"
)
