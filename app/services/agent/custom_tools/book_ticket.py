import json
import os
import random
from datetime import datetime

from flask import current_app as app
from pydantic import BaseModel, Field

from app.config.env_vars import NFT_CONTRACT_ADDRESS


class BookTicketInput(BaseModel):
    wallet_address: str = Field(
        ..., description="Wallet address of the user who wants to book a ticket"
    )
    movie_name: str = Field(..., description="Name of the movie")
    show_time: str = Field(..., description="Show time of the movie")
    show_date: str = Field(..., description="Show date of the movie")
    seat_number: str = Field(..., description="Seat number of the user")
    theater_name: str = Field(..., description="Name of the theater")


def book_ticket(
    wallet_address: str,
    movie_name: str,
    show_time: str,
    show_date: str,
    seat_number: str,
    theater_name: str,
):
    # ABI for smart contract invocation
    abi = [
        {
            "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
            "name": "safeMint",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ]

    token_id = random.randint(0, 99999)

    # Invoke the smart contract to mint the ticket as an NFT
    invocation = app.wallet.invoke_contract(
        contract_address=NFT_CONTRACT_ADDRESS,
        abi=abi,
        method="safeMint",
        args={"to": wallet_address, "tokenId": token_id},
    ).wait()

    print(invocation)

    # Create the ticket details dictionary
    ticket_details = {
        "wallet_address": wallet_address,
        "movie_name": movie_name,
        "show_time": show_time,
        "show_date": show_date,
        "seat_number": seat_number,
        "theater_name": theater_name,
        "transaction_hash": invocation.get("transactionHash", "N/A"),
        "block_number": invocation.get("blockNumber", "N/A"),
        "status": invocation.get("status", "N/A"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Ensure the ticket storage directory exists
    storage_folder = "ticket_storage"
    os.makedirs(storage_folder, exist_ok=True)

    # Create a unique filename for the ticket
    filename = f"{storage_folder}/ticket_{wallet_address}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    # Save the ticket details to a JSON file
    with open(filename, "w") as file:
        json.dump(ticket_details, file, indent=4)

    print(f"Ticket details saved at: {filename}")

    return invocation
