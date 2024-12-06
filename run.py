from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app import create_app
from app.config.env_vars import HOST, PORT
from app.services.agent.initialize_agent import initialize_agent

app: Flask = create_app()

# Allow all origins
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": "*"}})

# Flask-RESTX Application
api = Api(app)

agent_executor = initialize_agent()
app.agent_executor = agent_executor[0]
app.wallet = agent_executor[1]

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
