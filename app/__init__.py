from flask import Flask

from app.config.logger import setup_logger
from app.resources.agent.app import agent_blueprint


def create_app() -> Flask:
    app = Flask(__name__)

    # Initialize logger
    setup_logger(app)

    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(agent_blueprint, url_prefix="/api/agent")

    app.logger.info("Blueprints registered")
