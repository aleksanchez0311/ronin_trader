# config.py
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import requests

# Cargar variables
load_dotenv()

# Crear sesión con reintentos
session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Usar sesión en Web3
class RetryHTTPProvider(HTTPProvider):
    def __init__(self, endpoint_uri, session=None):
        self.endpoint_uri = endpoint_uri
        self.session = session or requests.Session()
        super().__init__(endpoint_uri, session=self.session)

# --- Conexión a Ronin ---
RONIN_NODE_URL="https://api.roninchain.com/rpc"
W3 = Web3(RetryHTTPProvider(RONIN_NODE_URL, session=session))

if not W3.is_connected():
    raise ConnectionError("❌ No se pudo conectar a Ronin")

W3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# --- Claves ---
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY no encontrada. Revise el archivo .env")

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
if not WALLET_ADDRESS:
    raise ValueError("WALLET_ADDRESS no encontrada. Revise el archivo .env")

# --- Direcciones ---
FACTORY_ADDRESS = "0xb255d6a720bb7c39fee173ce22113397119cb930"
ROUTER_ADDRESS = "0x2cCb8C89aBBDF3a366a39797C809c7957896c841"

# Tokens (agrega los que quieras aqui)
USDC = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
WETH = "0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5"
WRON = "0xe514d9DEB7966c8BE0ca922de8a064264eA6bcd4"
AXS = "0x97a9107C1793BC407d6F527b77e7fff4D812bece"
SLP = "0xa8754b9Fa15fc18BB59458815510E40a12cD2014"
#y luego aqui
TOKENS = [USDC,WETH,WRON,AXS,SLP]



SLIPPAGE=100