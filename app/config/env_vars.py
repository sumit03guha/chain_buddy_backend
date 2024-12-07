import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

# Define configuration variables
FLASK_ENV: str = os.environ["FLASK_ENV"]
HOST: str = os.environ["HOST"]
PORT = int(os.environ["PORT"])
SECRET_KEY: str = os.environ["SECRET_KEY"]

# Logging setup
LOG_DIR: str = os.path.join(BASE_DIR, "logs")
LOG_FILE: str = os.path.join(LOG_DIR, "agent-ai.log")

# CORS HEADER
CORS_HEADER: str = os.environ["CORS_HEADER"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
AGENT_MODEL = os.environ["AGENT_MODEL"]

COIN_GECKO_API_KEY = os.environ["COIN_GECKO_API_KEY"]
