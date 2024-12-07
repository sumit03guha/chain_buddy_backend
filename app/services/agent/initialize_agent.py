import os

from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.tools import CdpTool
from cdp_langchain.utils import CdpAgentkitWrapper
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.config.env_vars import AGENT_MODEL, OPENAI_API_KEY
from app.constants.prompt import AGENT_PROMPT
from app.services.agent.custom_tools.get_balance import GetETHBalanceInput, get_balance
from app.services.agent.custom_tools.get_coin_price import (
    GetCoinPriceInput,
    get_coin_price,
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

    get_balance_tool = CdpTool(
        name="get_balance",
        description="""Get the current balance of ETH or tokens for an ENS address on the specified chain.The chain to get the balance for. The supported chains are:
            - ethereum
            - polygon
            - base
            - base-sepolia""",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetETHBalanceInput,
        func=get_balance,
    )

    tools.append(get_balance_tool)

    get_coin_details_tool = CdpTool(
        name="get_coin_details",
        description="Get the current details of a coin, such as price, volume, market cap, etc.",
        cdp_agentkit_wrapper=agentkit,
        args_schema=GetCoinPriceInput,
        func=get_coin_price,
    )

    tools.append(get_coin_details_tool)

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
