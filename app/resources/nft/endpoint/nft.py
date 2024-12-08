import json
import os

from flask_restx import Resource

from app.config.env_vars import STORAGE_FOLDER

from ..namespace.nft import nft_namespace


@nft_namespace.route("/<int:token_id>")
class Ticket(Resource):
    def get(self, token_id):
        """
        Get the ticket details by token_id.
        """
        # Path to the JSON file for the specific ticket
        file_path = os.path.join(STORAGE_FOLDER, f"{token_id}.json")

        # Check if the file exists
        if not os.path.isfile(file_path):
            return {"status": "error", "message": "Ticket not found"}, 404

        # Read the JSON file and return its contents
        with open(file_path, "r") as file:
            ticket_details = json.load(file)

        return {"status": "success", "data": ticket_details}, 200
