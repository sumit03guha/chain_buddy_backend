from pydantic import BaseModel, Field

from app.services.agent.helper import get_coin_details_helper


class GetCoinPriceInput(BaseModel):
    token: str = Field(
        ..., description="The token symbol (e.g., 'ETH', 'BTC', 'DOGE', and so on)."
    )


def get_coin_price(token: str) -> str:
    """
    Get the current price of a coin in USD.

    Args:
        - token (str): The token symbol (e.g., 'ETH', 'BTC', 'DOGE', and so on).

    """

    coin_metadata = get_coin_details_helper(token)

    return coin_metadata.get("market_data", {}).get("current_price", {}).get("usd")
