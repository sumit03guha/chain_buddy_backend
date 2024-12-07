from flask import current_app as app
from pydantic import BaseModel, Field
from web3 import Web3

from app.config.env_vars import NFT_CONTRACT_ADDRESS


class BookTicketInput(BaseModel):
    wallet_address: str = Field(
        ..., description="Wallet address of the user who wants to book a ticket"
    )


def book_ticket(wallet_address: str):
    abi = [
        {
            "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
            "name": "safeMint",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ]

    invocation = app.wallet.invoke_contract(
        contract_address=NFT_CONTRACT_ADDRESS,
        abi=abi,
        method="safeMint",
        args={"to": wallet_address},
    ).wait()

    print(invocation)

    return invocation
