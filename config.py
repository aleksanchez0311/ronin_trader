# config.py
CHAIN_ID = 2020
RONIN_RPC_URL = "https://api.roninchain.com/rpc"

# Tokens comunes en Ronin (puedes agregar más)
TOKENS = {
    "USDC": "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc",
    "RON": "0x5555555555555555555555555555555555555555",  # Native RON (usado como "token" en swaps)
    "WRON": "0xe514d9deb7966c8be0ca922de8a064264ea6bcd4",   
    "SLP": "0xa8754b9fa15fc18bb59458815510e40a12cd2014",
    "AXS": "0x97a9107c1793bc407d6f527b77e7fff4d812bece",
    "WETH": "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
}

# Decimal de tokens (necesario para cálculos)
DECIMALS = {
    "USDC": 6,
    "WETH": 18,
    "AXS": 18,
    "SLP": 18,
    "RON": 18,
    "WRON": 18
}

