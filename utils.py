# utils.py
from web3 import Web3
from contracts import POOL_ABI

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
    
def get_tokens_from_pool(pool_address, W3):
    """Obtiene token0 y token1 de un pool"""
    try:
        contract = W3.eth.contract(address=pool_address, abi=POOL_ABI)
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        return token0, token1
    except Exception as e:
        print(f"❌ Error al obtener tokens del pool: {e}")
        return None, None