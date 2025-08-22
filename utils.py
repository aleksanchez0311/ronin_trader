# utils.py
from web3 import Web3

def get_token_symbol(token_address, tokens_dict):
    """Devuelve el símbolo del token si es conocido"""
    for name, addr in tokens_dict.items():
        if addr.lower() == token_address.lower():
            return name
    return token_address[:8]

def get_pool_address(factory_contract, token_a, token_b):
    """Obtiene la dirección del pool"""
    try:
        return factory_contract.functions.getPair(token_a, token_b).call()
    except Exception as e:
        print(f"Error al obtener pool: {e}")
        return None