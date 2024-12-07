from collections import namedtuple


class ChainList:
    # Define a namedtuple to hold the data
    Chain = namedtuple("Chain", ["key", "value"])

    # Assign namedtuple instances to class attributes
    ETHEREUM_MAINNET = Chain("ethereum", "https://rpc.flashbots.net")
    POLYGON_MAINNET = Chain("polygon", "https://polygon-bor-rpc.publicnode.com")
    BASE_MAINNET = Chain("base", "https://base.llamarpc.com")
    BASE_SEPOLIA = Chain("base-sepolia", "https://sepolia.base.org")
