import os

from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.tools import CdpTool
from cdp_langchain.utils import CdpAgentkitWrapper
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.config.env_vars import AGENT_MODEL, OPENAI_API_KEY
from app.constants.prompt import AGENT_PROMPT
from app.services.agent.custom_tools.book_ticket import BookTicketInput, book_ticket
from app.services.agent.custom_tools.get_tx_info import (
    GetTxInfoInput,
    get_tx_info,
)
from app.services.agent.custom_tools.movie import (
    GetLatestMoviesInput,
    GetMovieByNameInput,
    GetUpcomingMoviesInput,
    get_latest_movies,
    get_movie_by_name,
    get_upcoming_movies,
)
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

    get_upcoming_movies_tool = CdpTool(
        name="get_upcoming_movies",
        description="Get the details of the upcoming movies. Use this function to show the upcoming movies to the user.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetUpcomingMoviesInput,
        func=get_upcoming_movies,
    )

    tools.append(get_upcoming_movies_tool)

    get_latest_movies_tool = CdpTool(
        name="get_latest_movies",
        description="Get the details of the latest movies. Use this function to show the latest movies to the user.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetLatestMoviesInput,
        func=get_latest_movies,
    )

    tools.append(get_latest_movies_tool)

    book_ticket_tool = CdpTool(
        name="book_ticket",
        description="Book a ticket for the movie.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=BookTicketInput,
        func=book_ticket,
    )

    tools.append(book_ticket_tool)

    get_tx_info_tool = CdpTool(
        name="get_tx_info",
        description="Get the details of the transaction hash shared by the user after making the payment for the ticket. Use this function to assert whether the user wallet address has paid the agent address. This should be called before booking the ticket or calling the book_ticket_tool.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetTxInfoInput,
        func=get_tx_info,
    )

    tools.append(get_tx_info_tool)

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
