from eth_utils import is_address
from pydantic import BaseModel, Field

from app.services.agent.helper import (
    get_balance_of_eth,
    get_token_address,
    get_token_balance,
    resolve_ens_address,
)


class GetETHBalanceInput(BaseModel):

    ens_name_or_address: str = Field(
        ...,
        description="The ens name or address of the account to get the balance for",
    )
    token: str = Field(..., description="The token to get the balance for")
    chain: str = Field(
        ...,
        description="The chain to get the balance for",
        examples=["ethereum", "polygon", "base", "base-sepolia"],
    )


def get_balance(ens_name_or_address: str, token: str, chain: str) -> str:
    """
    Gets the current balance of ETH or tokens for an ENS address on the specified chain.
    If you are not sure about the chain to use, just use Ethereum Mainnet for this specific action.

    Args:
        - ens_name_or_address (str): The ENS name (e.g., 'vitalik.eth'). If it starts with 0x... then it's an address.
            If it doesnt end with .eth and its not an address, ask if the user wants to replace the ending with .eth.
            Only accept .eth endings.

        - token (str): The token symbol (e.g., 'ETH', 'USDC', 'USDT', and so on).
        - chain (str): The chain to get the balance for. The supported chains are:
            - ethereum
            - polygon
            - base
            - base-sepolia

    Returns:
        str: The balance information for the address.
    """

    try:
        address = None
        if not ens_name_or_address.endswith(".eth"):
            address = ens_name_or_address
        else:
            address = resolve_ens_address(ens_name_or_address)
        print(f"Address: {address}")
        if not address or not is_address(address):
            return f"Could not resolve ENS name: {ens_name_or_address}"

        if token.lower() == "eth":
            print("ETH")
            eth_balance = get_balance_of_eth(address, chain)
            return f"The balance for {ens_name_or_address} ({address}) is {float(eth_balance):.4f} ETH."
        else:
            token_address = get_token_address(token, chain)
            token_balance = float(get_token_balance(address, token_address, chain))
            return f"The balance for {ens_name_or_address} ({address}) is {token_balance:.4f} {token}."
    except Exception as e:
        return f"Error fetching balance: {e}"
