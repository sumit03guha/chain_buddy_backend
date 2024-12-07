import requests
from ens import ENS
from web3 import Web3

from app.config.env_vars import COIN_GECKO_API_KEY
from app.constants.chain_list import ChainList


def get_rpc_url(chain: str) -> str:
    if chain == ChainList.BASE_MAINNET.key:
        return ChainList.BASE_MAINNET.value
    elif chain == ChainList.POLYGON_MAINNET.key:
        return ChainList.POLYGON_MAINNET.value
    elif chain == ChainList.BASE_SEPOLIA.key:
        return ChainList.BASE_SEPOLIA.value
    else:
        return ChainList.ETHEREUM_MAINNET.value


def resolve_ens_address(ens_name: str, chain: str = "ethereum") -> str:
    web3 = Web3(Web3.HTTPProvider(get_rpc_url(chain)))
    ns = ENS.from_web3(web3)
    return ns.address(ens_name)


def get_balance_of_eth(address: str, chain: str = "ethereum") -> str:
    web3 = Web3(Web3.HTTPProvider(get_rpc_url(chain)))
    try:
        balance = web3.eth.get_balance(Web3.to_checksum_address(address))
        eth_balance = web3.from_wei(balance, "ether")
        return str(eth_balance)
    except Exception as e:
        return f"Error fetching balance: {e}"


def get_token_balance(address: str, token_address: str, chain: str = "ethereum") -> str:
    web3 = Web3(Web3.HTTPProvider(get_rpc_url(chain)))
    tokenInst = web3.eth.contract(
        address=Web3.to_checksum_address(token_address),
        abi="""
        [
        {"constant": true,"inputs": [],"name": "decimals","outputs": [{"name": "","type": "uint8"}],"payable": false,"stateMutability": "view","type": "function"},
        {"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"}
        ]
        """,
    )
    decimals = tokenInst.functions.decimals().call()

    balance = tokenInst.functions.balanceOf(address).call()
    return str(balance / 10**decimals)


def get_token_address(token_symbol: str, chain: str) -> str:
    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": COIN_GECKO_API_KEY,
    }

    search_api_symbol_by_name_url = (
        f"https://api.coingecko.com/api/v3/search?query={token_symbol}"
    )

    api_symbol_response = requests.get(search_api_symbol_by_name_url, headers=headers)
    print("api_symbol", api_symbol_response.json()["coins"][0], flush=True)

    api_symbol = api_symbol_response.json()["coins"][0]["api_symbol"]
    coin_metadata_url = f"https://api.coingecko.com/api/v3/coins/{api_symbol}"

    coin_metadata_response = requests.get(coin_metadata_url, headers=headers)
    print(f"chain: {chain}")
    print("response", coin_metadata_response.json().get("platforms", {}).get(chain))

    return coin_metadata_response.json().get("platforms", {}).get(chain)


def get_coin_details_helper(token_symbol: str) -> str:
    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": COIN_GECKO_API_KEY,
    }

    search_api_symbol_by_name_url = (
        f"https://api.coingecko.com/api/v3/search?query={token_symbol}"
    )

    api_symbol_response = requests.get(search_api_symbol_by_name_url, headers=headers)
    print("api_symbol", api_symbol_response.json()["coins"][0], flush=True)

    api_symbol = api_symbol_response.json()["coins"][0]["api_symbol"]
    coin_metadata_url = f"https://api.coingecko.com/api/v3/coins/{api_symbol}"

    coin_metadata_response = requests.get(coin_metadata_url, headers=headers)

    return coin_metadata_response.json()
