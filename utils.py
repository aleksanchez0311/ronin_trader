# utils.py
from web3 import Web3
import logging
from contracts import POOL_ABI, ERC20_ABI
from config import W3

def get_token_balance(token_address, wallet_address):
    """Obtiene el balance de un token ERC20 en una wallet"""
    try:
        contract = W3.eth.contract(address=token_address, abi=ERC20_ABI)
        return contract.functions.balanceOf(wallet_address).call()
    except Exception as e:
        logging.error(f"❌ Error al obtener balance de {token_address}: {e}")
        return 0

def get_token_symbol(token_address):
    """Obtiene el símbolo de un token"""
    try:
        contract = W3.eth.contract(address=token_address, abi=ERC20_ABI)
        return contract.functions.symbol().call()
    except Exception as e:
        print(f"❌ Error al obtener balance de {token_address}: {e}")
        return ""
    
def get_token_decimals(token_address):
    """Obtiene los decimales de un token"""
    try:
        contract = W3.eth.contract(address=token_address, abi=ERC20_ABI)
        return contract.functions.decimals0().call()
    except Exception as e:
        print(f"❌ Error al obtener balance de {token_address}: {e}")
        return ""

def get_pool_address(factory_contract, token_a, token_b):
    """Obtiene la dirección del pool"""
    try:
        return factory_contract.functions.getPair(token_a, token_b).call()
    except Exception as e:
        print(f"Error al obtener pool: {e}")
        return None
    
def get_tokens_from_pool(pool_address):
    """Obtiene token0 y token1 de un pool"""
    try:
        contract = W3.eth.contract(address=pool_address, abi=POOL_ABI)
        token0 = to_checksum(contract.functions.token0().call())
        token1 = to_checksum(contract.functions.token1().call())
        return token0, token1
        print(f"✅ Obtenido del pool token 1: {token0}")
        print(f"✅ Obtenido del pool token 2: {token1}")
    except Exception as e:
        print(f"❌ Error al obtener tokens del pool: {e}")
        return None, None
    
# Función de checksum
def to_checksum(addr):
    return W3.to_checksum_address(addr.lower())