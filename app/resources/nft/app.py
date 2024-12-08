from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from app.exceptions import BaseExceptionClass
from app.exceptions.exception_handler import handle_error

# Import namespaces from the respective modules
from .endpoint.nft import nft_namespace

# Create a Flask Blueprint for the nft module
nft_blueprint = Blueprint("nft", __name__)

# Initialize the Flask-RESTx API object, attaching it to the nft Blueprint
# and configuring it with title, description, and authorization details
api = Api(
    nft_blueprint,
    title="NFT API",
    description="API endpoints for NFT functionalities.",
)


# Register the nft namespaces with the API to include their endpoints
# in the Swagger UI documentation under the Authentication Management API
api.add_namespace(nft_namespace)  # Add nft-related endpoints

# Register the error handler for multiple exceptions
api.errorhandler(BaseExceptionClass)(handle_error)
api.errorhandler(BadRequest)(handle_error)
api.errorhandler(NotFound)(handle_error)
api.errorhandler(InternalServerError)(handle_error)
