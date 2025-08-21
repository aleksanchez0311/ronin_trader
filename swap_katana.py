# swap_katana.py
from web3 import Web3
from decouple import config
from config import RONIN_RPC_URL, TOKENS, DECIMALS
import json
import time

# Conectar a Ronin
w3 = Web3(Web3.HTTPProvider(RONIN_RPC_URL, request_kwargs={"timeout": 15}))

if not w3.is_connected():
    raise Exception("❌ No se pudo conectar al nodo de Ronin")

print("✅ Conectado a Ronin via api.roninchain.com/rpc")

# Cargar ABI del router de Katana
with open('katana_router_abi.json', 'r') as f:
    KATANA_ABI = json.load(f)

KATANA_ROUTER = "0x27861e29c73b689ad79a9743d9cbcf93151c4f04"

router_contract = w3.eth.contract(address=KATANA_ROUTER, abi=KATANA_ABI)

def get_amount_out(token_in, token_out, amount_in):
    try:
        amount_in_wei = int(amount_in * 10**DECIMALS[token_in])
        amounts = router_contract.functions.getAmountsOut(
            amount_in_wei,
            [token_in, token_out]
        ).call()
        return amounts[1] / 10**DECIMALS[token_out]
    except Exception as e:
        print(f"❌ Error al obtener cantidad de salida: {e}")
        return 0

def swap_exact_tokens_for_tokens(token_in, token_out, amount_in, min_amount_out, from_address, private_key):
    try:
        amount_in_wei = int(amount_in * 10**DECIMALS[token_in])
        deadline = int(time.time()) + 1000  # 1000 segundos

        tx = router_contract.functions.swapExactTokensForTokens(
            amount_in_wei,
            int(min_amount_out * 10**DECIMALS[token_out]),
            [token_in, token_out],
            from_address,
            deadline
        ).build_transaction({
            'from': from_address,
            'nonce': w3.eth.get_transaction_count(from_address),
            'gas': 250000,
            'gasPrice': w3.to_wei('20', 'gwei'),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ Swap ejecutado! Hash: {w3.to_hex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"❌ Error al ejecutar swap: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Par de tokens: USDC → RON
    token_in = TOKENS["USDC"]
    token_out = TOKENS["RON"]
    amount_in = 1.0  # 1 USDC
    min_amount_out = 0.001  # Mínimo de RON esperado
    from_address = config("WALLET_ADDRESS")
    private_key = config("PRIVATE_KEY")

    # Obtener precio estimado
    estimated_out = get_amount_out(token_in, token_out, amount_in)
    print(f"Estimación: {amount_in} USDC → {estimated_out:.6f} RON")

    # Ejecutar swap
    swap_exact_tokens_for_tokens(
        token_in=token_in,
        token_out=token_out,
        amount_in=amount_in,
        min_amount_out=min_amount_out,
        from_address=from_address,
        private_key=private_key
    )