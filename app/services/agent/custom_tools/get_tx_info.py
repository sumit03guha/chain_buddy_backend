import requests
from flask import current_app as app
from pydantic import BaseModel, Field


class GetTxInfoInput(BaseModel):
    tx_hash: str = Field(..., description="Transaction hash shared by the user")


def get_tx_info(tx_hash: str):

    # Define the URL and the headers
    url = f"https://base-sepolia.blockscout.com/api/v2/transactions/{tx_hash}"
    headers = {"accept": "application/json"}

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        latest_transaction = response.json()

        if (
            latest_transaction["to"]["hash"]
            == "0x0D873f601E27A3D4C1A93F24C1cf054B6cfFb55a"
        ):
            return True
        else:
            return False
    else:
        print(f"Failed to retrieve transactions: {response.status_code}")
