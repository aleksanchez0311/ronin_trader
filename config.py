# config.py
CHAIN_ID = 2020
RONIN_RPC = "https://api.roninchain.com/rpc"

# Tokens comunes en Ronin (puedes agregar más)
TOKENS = {
    "USDT": "0xa863dbaf8a2c7b7998634c8c3d96d9c8a8d9909f",
    "WETH": "0xc99a6c30152917a785f5e3d6135387b27553b974",
    "RON": "0x5555555555555555555555555555555555555555",  # Native RON (usado como "token" en swaps)
    "AXS": "0x97a9107c1793bc407d69a8fa7f03b14671989c82",
    "SLP": "0xa4d5687e50a8a8abf81baa17a37859b964434808"
}

# Decimal de tokens (necesario para cálculos)
DECIMALS = {
    "USDT": 18,
    "WETH": 18,
    "AXS": 18,
    "SLP": 0,
    "RON": 18
}