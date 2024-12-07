from flask import Response, current_app, jsonify, request, stream_with_context
from flask_restx import Resource

from app.services.agent.run_agent import run_agent

from ..namespace.agent import agent_namespace
from ..schema.agent import text_model


@agent_namespace.route("")
class Agent(Resource):
    """
    This endpoint allows for interaction with an agent through a conversational interface.
    It supports posting data to the agent and receiving a stream of responses as server-sent events.
    """

    @agent_namespace.expect(text_model, validate=True)
    def post(self):
        """
        Handles incoming requests to chat with the agent. It expects JSON data containing the chat input,
        processes it through the agent, and returns the agent's responses as a stream.

        The endpoint is designed to receive a 'conversation_id' for threading purposes and the 'input' text
        from the user to which the agent should respond.

        **Input Fields:**
        - `input`: Required. The textual input to the agent.
        - `conversation_id`: Optional. A unique identifier for the conversation thread.

        Returns:
        Response: A streamed response of the agent's output, formatted as server-sent events. In case of errors,
                  returns an appropriate JSON error message with HTTP status codes 400 (Bad Request) or 500 (Internal Server Error).

        Raises:
        - HTTP 400: If no input data is provided or the 'input' key is missing.
        - HTTP 500: If there is any internal error during the processing of the input.
        """
        try:
            data = request.get_json()
            user_name = request.headers.get("Authorization")

            if not data or "input" not in data:
                return jsonify({"error": "No data provided"}), 400

            if len(data["input"]) == 0:
                return jsonify({"error": "No data provided"}), 400

            config = {"configurable": {"thread_id": data.get("conversation_id", "")}}

            # Run the agent and stream its response
            return Response(
                stream_with_context(
                    run_agent(
                        data["input"] + "The name of the user is " + user_name + ".",
                        current_app.agent_executor,
                        config,
                    )
                ),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Content-Type": "text/event-stream",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
