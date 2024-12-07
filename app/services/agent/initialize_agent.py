import os

from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.tools import CdpTool
from cdp_langchain.utils import CdpAgentkitWrapper
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.config.env_vars import AGENT_MODEL, OPENAI_API_KEY
from app.constants.prompt import AGENT_PROMPT
from app.services.agent.custom_tools.movie import GetMovieByNameInput, get_movie_by_name
from app.services.agent.custom_tools.nook import (
    GetNookProfileInput,
    get_movies_from_nook_profile,
)

wallet_data_file = "wallet_data.txt"


def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    # Initialize LLM.
    llm = ChatOpenAI(model=AGENT_MODEL, api_key=OPENAI_API_KEY)

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    # Configure CDP Agentkit Langchain Extension.
    values = {}
    if wallet_data is not None:
        # If there is a persisted agentic wallet, load it and pass to the CDP Agentkit Wrapper.
        values = {"cdp_wallet_data": wallet_data}

    agentkit = CdpAgentkitWrapper(**values)

    # Initialize CDP Agentkit Toolkit and get tools.
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools()

    get_movie_by_name_tool = CdpTool(
        name="get_movie_by_name",
        description="Get the details of a movie by its name.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetMovieByNameInput,
        func=get_movie_by_name,
    )

    tools.append(get_movie_by_name_tool)

    get_movies_from_nook_profile_tool = CdpTool(
        name="get_movies_from_nook_profile",
        description="Get the details of a movie from the social Nook profile of a user, where they have shared their review of the movie. These details reflect the user's movie preferences. Use this function to get the movie reviews of the user and use it to recommend movies to the user.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetNookProfileInput,
        func=get_movies_from_nook_profile,
    )

    tools.append(get_movies_from_nook_profile_tool)

    # persist the agent's CDP MPC Wallet Data.
    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Store buffered conversation history in memory.
    memory = MemorySaver()

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return (
        create_react_agent(
            llm,
            tools=tools,
            checkpointer=memory,
            state_modifier=AGENT_PROMPT,
        ),
        agentkit.wallet,
    )
