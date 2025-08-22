# main.py
import os
import time
import logging
from dotenv import load_dotenv
from web3 import Web3

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
from utils import get_tokens_from_pool

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

def get_token_symbol(token_address):
    """Obtiene el símbolo de un token (simplificado para tokens conocidos)"""
    SYMBOLS = {
        WETH.lower(): "WETH",
        USDC.lower(): "USDC",
        AXS.lower(): "AXS",
        SLP.lower(): "SLP"
    }
    return SYMBOLS.get(token_address.lower(), token_address[:8])

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

# --- Ejecutar Trade ---
def execute_trade(token_in, token_out, amount_in_wei):
    """Ejecuta un swap en Katana"""
    if not PRIVATE_KEY:
        in_sym = get_token_symbol(token_in)
        out_sym = get_token_symbol(token_out)
        logging.warning(f"🟢 [SIMULADO] Swap: {amount_in_wei} {in_sym} → {out_sym}")
        return "simulated_tx_hash"

    try:
        amounts_out = router_contract.functions.getAmountsOut(
            amount_in_wei, [token_in, token_out]
        ).call()
        amount_out_min = int(amounts_out[1] * 0.99)

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

        signed_tx = W3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logging.info(f"✅ Trade enviado! Tx: {tx_hash.hex()}")
        return tx_hash.hex()

    except Exception as e:
        logging.error(f"❌ Error al ejecutar trade: {e}")
        return None

# --- Monitorear eventos de Swap en Katana (versión avanzada) ---
def poll_katana_swaps():
    """Consulta eventos de Swap en Katana y detecta oportunidades en cualquier par"""
    try:
        # Topic del evento Swap
        SWAP_TOPIC = "0xdff52c99c1dbe141c749727819e755918be7b86541a05d408426704d16017d4c"

        latest_block = W3.eth.block_number
        from_block = max(latest_block - 100, 0)

        logs = W3.eth.get_logs({
            "fromBlock": from_block,
            "toBlock": latest_block,
            "address": to_checksum(ROUTER_ADDRESS),
            "topics": [SWAP_TOPIC]
        })

        if not logs:
            return

        logging.info(f"🔍 {len(logs)} swaps detectados en los últimos 100 bloques")

        for log in logs:
            try:
                # Decodificar evento Swap
                event = router_contract.events.Swap()
                decoded = event.process_log(log)

                # Obtener tokens del pool
                pool_address = log["address"]
                tokens = get_tokens_from_pool(pool_address)
                
                if not tokens:
                    continue

                token0, token1 = tokens
                token0_sym = get_token_symbol(token0)
                token1_sym = get_token_symbol(token1)

                # Determinar qué token se vendió
                if decoded.args.amount0In > 0:
                    token_sold = token0
                    token_bought = token1
                    amount_sold = decoded.args.amount0In
                    amount_bought = decoded.args.amount1Out
                    sym_sold = token0_sym
                    sym_bought = token1_sym
                elif decoded.args.amount1In > 0:
                    token_sold = token1
                    token_bought = token0
                    amount_sold = decoded.args.amount1In
                    amount_bought = decoded.args.amount0Out
                    sym_sold = token1_sym
                    sym_bought = token0_sym
                else:
                    continue

                # Mostrar swap detectado
                logging.info(f"🔁 Swap detectado: {amount_sold / 10**18:.4f} {sym_sold} → {amount_bought / 10**18:.4f} {sym_bought} | Pool: {sym_sold}-{sym_bought}")

                # Estrategia: seguir grandes swaps
                if amount_sold > 100 * 10**18 and sym_sold in ["AXS", "SLP"]:
                    logging.warning(f"🚨 Gran venta de {sym_sold} detectada: {amount_sold / 10**18:.2f} {sym_sold}")
                    # Aquí tu lógica de trading
                    
                elif amount_bought > 100 * 10**18 and sym_bought in ["AXS", "SLP"]:
                    logging.warning(f"🟢 Gran compra de {sym_bought} detectada: {amount_bought / 10**18:.2f} {sym_bought}")
                    # Aquí tu lógica de trading

            except Exception as e:
                logging.error(f"❌ Error al procesar evento: {e}")
                continue

    except Exception as e:
        logging.error(f"❌ Error al consultar eventos de Katana: {e}")

# --- Loop Principal ---
def main():
    logging.info(f"🚀 Bot de trading en Ronin iniciado | Wallet: {WALLET_ADDRESS[:10]}...")
    show_balances()

    while True:
        try:
            poll_katana_swaps()
            time.sleep(30)  # Cada 30 segundos
        except KeyboardInterrupt:
            logging.info("🛑 Bot detenido por el usuario.")
            break
        except Exception as e:
            logging.error(f"🔁 Error en el loop principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()