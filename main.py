# main.py
from decouple import config
import time
from swap_moralis import swap_token
from wallet import get_all_balances
from notifier import alert
from trading_strategy import rsi_strategy, get_prices
from config import TOKENS

# Configuración de la billetera
wallet_address = config("WALLET_ADDRESS")

def execute_swap(token_in, token_out, amount_in):
    """
    Ejecuta un swap con la cantidad especificada
    """
    try:
        # Obtener el precio actual
        prices = get_prices()
        usdc_price = prices["USDC"]
        
        # Calcular la cantidad de salida estimada
        amount_out = amount_in * usdc_price
        
        # Mostrar información del swap
        alert(f"🔍 Señal de swap detectada: {amount_in} {token_in} → {amount_out:.6f} {token_out}")
        
        # Ejecutar el swap
        result = swap_token(
            token_in=token_in,
            token_out=token_out,
            amount_in=amount_in,
            from_address=wallet_address
        )
        
        if result:
            alert(f"✅ Swap ejecutado con éxito: {result}")
            return True
        else:
            alert("❌ Error al ejecutar el swap")
            return False
    except Exception as e:
        alert(f"🚨 Error en el swap: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Bot de trading en Ronin iniciado...")
    alert("Bot iniciado. Esperando señales...")

    while True:
        try:
            # Obtener balances
            balances = get_all_balances(wallet_address)
            alert(f"📊 Balances actuales: {balances}")
            
            # Obtener precios
            prices = get_prices()
            
            # Estrategia de trading
            signal = rsi_strategy(balances, prices)
            
            if signal == "BUY" and balances["USDC"] > 0.1:
                # Comprar USDC a RON
                amount_in = 0.1  # 0.1 USDC
                token_in = TOKENS["USDC"]
                token_out = TOKENS["RON"]
                
                # Ejecutar el swap
                execute_swap(token_in, token_out, amount_in)
                
            elif signal == "SELL" and balances["RON"] > 0.1:
                # Vender RON por USDC
                amount_in = 0.1  # 0.1 RON
                token_in = TOKENS["RON"]
                token_out = TOKENS["USDC"]
                
                # Ejecutar el swap
                execute_swap(token_in, token_out, amount_in)
                
            else:
                alert("🟨 Sin acción: Esperando señal...")
            
            time.sleep(300)  # Esperar 5 minutos
            
        except Exception as e:
            alert(f"🚨 Error en el bot: {e}")
            time.sleep(60)