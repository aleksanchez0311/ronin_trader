# test/swap_test.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from swap_moralis import swap_token
from decouple import config
from config import TOKENS

# Par de tokens: USDC → RON
token_in = TOKENS["USDC"]
token_out = TOKENS["RON"]
amount_in = 0.1  # 0.1 USDC
from_address = config("WALLET_ADDRESS")

# Ejecutar swap
result = swap_token(
    token_in=token_in,
    token_out=token_out,
    amount_in=amount_in,
    from_address=from_address
)

if result:
    print("✅ Swap realizado con éxito")
else:
    print("❌ Error al realizar el swap")