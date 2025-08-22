# config.py
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

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
FACTORY_ADDRESS = "0x85a9C8f5478C8884b2Ea1F88d6a2B77fDa2E7900"

# Tokens
USDC = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
AXS = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
WETH = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
SLP = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"

def to_checksum(addr):
    return Web3.to_checksum_address(addr.lower())

#TOKENS = {
    #"USDC": "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc",
    #"RON": "0x5555555555555555555555555555555555555555",
   # "WRON": "0xe514d9deb7966c8be0ca922de8a064264ea6bcd4",
    #"SLP": "0xa8754b9fa15fc18bb59458815510e40a12cd2014",
    #"AXS": "0x97a9107c1793bc407d6f527b77e7fff4d812bece",
    #"WETH": "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
#}