# main.py
import os
import time
import requests
import logging
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)

# --- Importar desde config.py ---
from config import W3, PRIVATE_KEY, WALLET_ADDRESS, ROUTER_ADDRESS, WETH, USDC, AXS, SLP, to_checksum
from contracts import ROUTER_ABI, ERC20_ABI

# --- Validar billetera ---
if not W3.is_address(WALLET_ADDRESS):
    logging.error(f"❌ Dirección de billetera inválida: {WALLET_ADDRESS}")
    exit(1)

# --- Inicializar contrato del router ---
try:
    router_contract = W3.eth.contract(address=to_checksum(ROUTER_ADDRESS), abi=ROUTER_ABI)
    logging.info("✅ Contrato del router de Katana cargado.")
except Exception as e:
    logging.error(f"❌ Error al cargar contrato: {e}")
    exit(1)

# --- Utilidades ---
def get_token_balance(token_address):
    """Obtiene el balance de un token ERC20"""
    try:
        contract = W3.eth.contract(address=to_checksum(token_address), abi=ERC20_ABI)
        return contract.functions.balanceOf(WALLET_ADDRESS).call()
    except Exception as e:
        logging.error(f"❌ Error al obtener balance de {token_address}: {e}")
        return 0

def show_balances():
    """Muestra los balances actuales"""
    weth_bal = get_token_balance(WETH)
    usdc_bal = get_token_balance(USDC)
    axs_bal = get_token_balance(AXS)
    slp_bal = get_token_balance(SLP)
    eth_bal = W3.eth.get_balance(WALLET_ADDRESS)

    logging.info(
        f"💰 Balances: "
        f"{weth_bal / 10**18:.4f} WETH | "
        f"{usdc_bal / 10**6:.2f} USDC | "
        f"{axs_bal / 10**18:.4f} AXS | "
        f"{slp_bal / 10**18:.4f} SLP | "
        f"{W3.from_wei(eth_bal, 'ether'):.4f} RON"
    )

# --- Ejecutar Trade (simulado o real) ---
def execute_trade(token_in, token_out, amount_in_wei):
    """Ejecuta un swap en Katana"""
    if not PRIVATE_KEY:
        logging.warning(f"🟢 [SIMULADO] Swap: {amount_in_wei} {token_in} → {token_out}")
        return "simulated_tx_hash"

    try:
        # Estimar salida mínima (slippage 1%)
        amounts_out = router_contract.functions.getAmountsOut(
            amount_in_wei, [token_in, token_out]
        ).call()
        amount_out_min = int(amounts_out[1] * 0.99)

        # Construir transacción
        tx = router_contract.functions.swapExactTokensForTokens(
            amount_in_wei,
            amount_out_min,
            [token_in, token_out],
            WALLET_ADDRESS,
            int(time.time()) + 1000
        ).build_transaction({
            'from': WALLET_ADDRESS,
            'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS),
            'gas': 250000,
            'gasPrice': W3.to_wei('20', 'gwei'),
        })

        # Firmar y enviar
        signed_tx = W3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logging.info(f"✅ Trade enviado! Tx: {tx_hash.hex()}")
        return tx_hash.hex()

    except Exception as e:
        logging.error(f"❌ Error al ejecutar trade: {e}")
        return None

# --- Polling de eventos (Moralis) ---
def poll_moralis_events():
    """Consulta swaps recientes desde Moralis"""
    url = "https://deep-index.moralis.io/api/v2/erc20/transfers"
    params = {
        'chain': 'ronin',
        'address': ROUTER_ADDRESS,
        'limit': 5
    }
    headers = {
        'X-API-Key': os.getenv("MORALIS_API_KEY")
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            logging.warning(f"⚠️ Moralis: {r.status_code} - {r.text}")
            return

        data = r.json()
        for tx in data.get('result', []):
            # Detectar grandes transferencias de AXS
            token_addr = tx.get('token_address', '').lower()
            value = int(tx.get('value', '0'))

            if token_addr == AXS.lower() and value > 100 * 10**18:
                logging.warning("🚨 Gran venta de AXS detectada!")
                usdc_balance = get_token_balance(USDC)
                if usdc_balance > 5 * 10**6:  # >5 USDC
                    logging.info("Bot comprando AXS...")
                    execute_trade(USDC, AXS, 5 * 10**6)
                else:
                    logging.info("ℹ️  Sin suficiente USDC para comprar.")
                break  # Procesa solo uno por iteración

    except Exception as e:
        logging.error(f"❌ Error al consultar Moralis: {e}")

# --- Loop Principal ---
def main():
    logging.info(f"🚀 Bot de trading en Ronin iniciado | Wallet: {WALLET_ADDRESS[:10]}...")
    show_balances()

    while True:
        try:
            poll_moralis_events()
            time.sleep(30)  # Cada 30 segundos
        except KeyboardInterrupt:
            logging.info("🛑 Bot detenido por el usuario.")
            break
        except Exception as e:
            logging.error(f"🔁 Error en el loop principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()