# config.py
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from contracts import FACTORY_ABI, POOL_ABI
from dotenv import load_dotenv
import os
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)

def to_checksum(addr):
    return Web3.to_checksum_address(addr.lower())

# Conexión a Ronin
W3_PROVIDER_URL = os.getenv("RONIN_NODE_URL", "https://api.roninchain.com/rpc")
W3 = Web3(Web3.HTTPProvider(W3_PROVIDER_URL))

# Verificar conexión
if not W3.is_connected():
    raise ConnectionError("❌ No se pudo conectar a Ronin. Revisa la URL del nodo.")
else:
    print("✅ Conectado a Ronin")

# Añadir middleware PoA
W3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Claves
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "").replace("ronin", "0x")

# Direcciones de contratos
ROUTER_ADDRESS = "0x2cCb8C89aBBDF3a366a39797C809c7957896c841"
FACTORY_ADDRESS = "0xb255d6a720bb7c39fee173ce22113397119cb930"

# Tokens
USDC = "0x0B7007c13325C48911F73A2daD5FA5dCBf808aDc"
WRON = "0xe514d9DEB7966c8BE0ca922de8a064264eA6bcd4"
AXS = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
WETH = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
SLP = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"

# --- Pares conocidos en Katana (token0, token1) ---
def get_pool_address(token_a, token_b):
    """Obtiene la dirección del pool para dos tokens"""
    try:
        # Dirección del Factory de Katana
        FACTORY_ADDRESS = "0x85a9C8f5478C8884b2Ea1F88d6a2B77fDa2E7900"
        
        # Crear contrato
        factory_contract = W3.eth.contract(
            address=to_checksum(FACTORY_ADDRESS), 
            abi=FACTORY_ABI
        )
        
        # Obtener dirección del pool
        pool_address = factory_contract.functions.getPair(
            to_checksum(token_a), 
            to_checksum(token_b)
        ).call()
        return to_checksum(pool_address)
    except Exception as e:
        logging.error(f"❌ Error al obtener dirección del pool: {e}")
        return None
    
# Puedes agregar más pares según necesites
PAIRS = {
    # AXS-USDC Pool
    "0x572bca391432053cded92926d429e02a079c914e": (USDC, AXS),
    # AXS-WETH Pool
    "0xc6344bc1604fcab1a5aad712d766796e2b7a70b9": (AXS, WETH),  # Agrega la dirección del pool si la conoces
    # SLP-USDC Pool
     "0xec087b4defcf76d5666ef366d7ae98cf926ae545": (USDC, SLP),
}

# Función para obtener los tokens de un pool
def get_tokens_from_pool(pool_address):
    try:
        pool_contract = W3.eth.contract(
            address=to_checksum(pool_address), 
            abi=POOL_ABI
        )
        token0 = pool_contract.functions.token0().call()
        token1 = pool_contract.functions.token1().call()
        return (to_checksum(token0), to_checksum(token1))
    except Exception as e:
        logging.error(f"❌ Error al obtener tokens del pool: {e}")
        return None


#TOKENS = {
    #"USDC": "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc",
    #"RON": "0x5555555555555555555555555555555555555555",
   # "WRON": "0xe514d9deb7966c8be0ca922de8a064264ea6bcd4",
    #"SLP": "0xa8754b9fa15fc18bb59458815510e40a12cd2014",
    #"AXS": "0x97a9107c1793bc407d6f527b77e7fff4d812bece",
    #"WETH": "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
#}