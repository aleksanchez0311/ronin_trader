# config.py
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv
import os

# Cargar variables
load_dotenv()

# --- Conexión a Ronin ---
RONIN_NODE_URL = os.getenv("RONIN_NODE_URL", "https://api.roninchain.com/rpc")
w3 = Web3(Web3.HTTPProvider(RONIN_NODE_URL))

if not w3.is_connected():
    raise ConnectionError("❌ No se pudo conectar a Ronin")

w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# --- Claves ---
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS_RAW = os.getenv("WALLET_ADDRESS")
if not WALLET_ADDRESS_RAW:
    raise ValueError("WALLET_ADDRESS no encontrada")

WALLET_ADDRESS = w3.to_checksum_address(WALLET_ADDRESS_RAW.replace("ronin", "0x"))

# --- Direcciones ---
FACTORY_ADDRESS = "0xb255d6a720bb7c39fee173ce22113397119cb930"
ROUTER_ADDRESS = "0x2cCb8C89aBBDF3a366a39797C809c7957896c841"

# Tokens
USDC = "0xa8C7852237F27EeE51234e8D3f9C17a377631249"
AXS = "0x97a9107c1793bc407d69a15566cf58a69ff36c02"
WETH = "0xc748673057861a797275CD8A068AbB95A902e8de"
SLP = "0xa5d410f29bb76871725b53edd43eba2c574cce58"

# Lista de tokens
TOKENS = {"USDC": USDC, "AXS": AXS, "WETH": WETH, "SLP": SLP}

# Función de checksum
def to_checksum(addr):
    return w3.to_checksum_address(addr.lower())