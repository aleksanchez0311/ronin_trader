# wallet.py
from web3 import Web3
from decouple import config
from config import RONIN_RPC_URL, TOKENS, DECIMALS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar a Ronin
w3 = Web3(Web3.HTTPProvider(
    RONIN_RPC_URL,
    request_kwargs={"timeout": 15}
))

if not w3.is_connected():
    raise Exception("❌ No se pudo conectar al nodo de Ronin")

logger.info("✅ Conectado a Ronin via ronin.drpc.org")

def get_balance(token_symbol, wallet_address):
    try:
        address = Web3.to_checksum_address(wallet_address)
        
        if token_symbol == "RON":
            balance = w3.eth.get_balance(address)
            return balance / 10**18
        
        token_address = Web3.to_checksum_address(TOKENS[token_symbol])
        contract = w3.eth.contract(
            address=token_address,
            abi=[{
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }]
        )
        balance = contract.functions.balanceOf(address).call()
        decimals = DECIMALS.get(token_symbol, 18)
        return balance / (10 ** decimals)

    except Exception as e:
        logger.error(f"❌ Error al obtener balance de {token_symbol}: {e}")
        return 0

def get_all_balances(wallet_address):
    balances = {}
    for symbol in TOKENS.keys():
        logger.info(f"🔍 Obteniendo balance de {symbol}...")
        bal = get_balance(symbol, wallet_address)
        balances[symbol] = round(bal, 6)
    return balances
