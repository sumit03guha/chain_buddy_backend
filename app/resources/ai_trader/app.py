from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from app.exceptions import BaseExceptionClass
from app.exceptions.exception_handler import handle_error

# Import namespaces from the respective modules
from .endpoint.agent import agent_namespace

# Create a Flask Blueprint for the authentication module
agent_blueprint = Blueprint("agent", __name__)

# Initialize the Flask-RESTx API object, attaching it to the authentication Blueprint
# and configuring it with title, description, and authorization details
api = Api(
    agent_blueprint,
    title="Agents API",
    description="API endpoints for agent functionalities.",
)


# Register the agent namespaces with the API to include their endpoints
# in the Swagger UI documentation under the Authentication Management API
api.add_namespace(agent_namespace)  # Add agent-related endpoints

# Register the error handler for multiple exceptions
api.errorhandler(BaseExceptionClass)(handle_error)
api.errorhandler(BadRequest)(handle_error)
api.errorhandler(NotFound)(handle_error)
api.errorhandler(InternalServerError)(handle_error)
