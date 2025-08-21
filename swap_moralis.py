# swap_moralis.py
from moralis import evm_api
from decouple import config
from config import TOKENS, DECIMALS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def swap_token(token_in, token_out, amount_in, from_address):
    """
    Realiza un swap usando Moralis API
    """
    try:
        api_key = config("MORALIS_API_KEY")
        chain = "ronin"
        
        # Convertir la cantidad a la unidad correcta (con decimales)
        amount_in_wei = int(amount_in * (10 ** DECIMALS[token_in]))
        
        # Pasar tokens como objetos con propiedad "address"
        result = evm_api.token.approve_and_swap(
            api_key=api_key,
            chain=chain,
            amount_in=str(amount_in_wei),
            token_in={"address": token_in},
            token_out={"address": token_out},
            from_address=from_address,
            to_address=from_address
        )
        
        logger.info(f"✅ Swap realizado: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ Error al realizar swap: {e}")
        return None