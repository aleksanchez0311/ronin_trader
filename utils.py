# utils.py
from web3 import Web3
import logging
from contracts import POOL_ABI, ERC20_ABI
from config import PRIVATE_KEY, WALLET_ADDRESS, ROUTER_ADDRESS, FACTORY_ADDRESS, USDC, WETH, WRON, AXS, SLP
from config import W3


def get_token_balance(token_address, owner_address):
    """Obtiene el balance de un token ERC20 con decimales"""
    try:
        contract = W3.eth.contract(address=token_address, abi=ERC20_ABI)
        balance = contract.functions.balanceOf(owner_address).call()
        decimals = contract.functions.decimals().call()
        return balance / (10 ** decimals)
    except Exception as e:
        print(f"❌ Error al obtener balance: {e}")
        return 0

def get_token_symbol(token_address):
    """Obtiene el símbolo de un token"""
    try:
        contract = W3.eth.contract(address=token_address, abi=ERC20_ABI)
        return contract.functions.symbol().call()
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
    """Obtiene token0 y token1 de un pool con checksum aplicado"""
    try:
        contract = W3.eth.contract(address=pool_address, abi=POOL_ABI)
        token0 = to_checksum(contract.functions.token0().call())
        token1 = to_checksum(contract.functions.token1().call())
        print(f"✅ Obtenido del pool token 1: {token0}")
        print(f"✅ Obtenido del pool token 2: {token1}")
        return token0, token1
    except Exception as e:
        print(f"❌ Error al obtener tokens del pool: {e}")
        return None, None
    
# Función de checksum
def to_checksum(addr):
    return W3.to_checksum_address(addr.lower())

#Aplicando checksum a todas las direcciones
CHECKSUMED_PRIVATE_KEY = PRIVATE_KEY
CHECKSUMED_WALLET_ADDRESS = to_checksum(WALLET_ADDRESS)
CHECKSUMED_FACTORY_ADDRESS = to_checksum(FACTORY_ADDRESS)
CHECKSUMED_ROUTER_ADDRESS = to_checksum(ROUTER_ADDRESS)
CHECKSUMED_TOKENS = {to_checksum(USDC), to_checksum(WETH), to_checksum(WRON), to_checksum(AXS), to_checksum(SLP)}