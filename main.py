# main.py
from web3 import Web3
from decouple import config
import time
from swap_api import get_swap_route
from wallet import get_all_balances
from notifier import alert
from config import TOKENS

web3 = Web3(Web3.HTTPProvider(config("RONIN_RPC_URL")))
private_key = config("PRIVATE_KEY")
wallet_address = config("WALLET_ADDRESS")

def execute_swap(route):
    tx = {
        'to': web3.to_checksum_address(route['to']),
        'value': 0,
        'gas': route['gasCost'],
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
        'data': route['txData'],
        'chainId': 2020
    }
    try:
        signed = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        alert(f"❌ Error al ejecutar swap: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Bot de trading en Ronin iniciado...")
    alert("Bot iniciado. Esperando señal...")

    while True:
        try:
            balances = get_all_balances(wallet_address)
            alert(f"📊 Balances actuales: {balances}")

            # Ejemplo: Swap de 1 RON → USDT
            from_token = "0x5555555555555555555555555555555555555555"  # RON
            to_token = TOKENS["USDT"]
            amount = int(1 * 10**18)  # 1 RON

            route = get_swap_route(from_token, to_token, amount, wallet_address)
            if not route:
                time.sleep(60)
                continue

            to_amount = int(route['toAmount']) / 10**18
            msg = f"""
🔔 *ALERTA DE SWAP*
De: 1 RON
A: {to_amount:.6f} USDT
¿Autorizas el swap? Responde en Telegram con:
✅ /ejecutar_swap
"""
            alert(msg)

            # Simulación de espera (30 seg)
            time.sleep(30)

            # Verificar si aún es rentable
            new_route = get_swap_route(from_token, to_token, amount, wallet_address)
            if new_route and int(new_route['toAmount']) >= int(route['toAmount']) * 0.98:
                hash = execute_swap(new_route)
                if hash:
                    alert(f"✅ Swap ejecutado! Hash: {hash}")
            else:
                alert("📉 Swap no rentable. Cancelado.")

            time.sleep(300)  # Esperar 5 minutos

        except Exception as e:
            alert(f"🚨 Error en el bot: {e}")
            time.sleep(60)