# trading_strategy.py
from config import TOKENS

def rsi_strategy(balances, prices):
    """
    Estrategia basada en el RSI (Relative Strength Index)
    """
    # En este ejemplo, usamos un enfoque simple: comprar si el precio de USDC está por debajo de 0.99 y vender si está por encima de 1.01
    # En la práctica, necesitarías obtener los precios de los tokens y calcular el RSI
    
    usdc_price = prices["USDC"]
    
    if usdc_price < 0.99:
        return "BUY"
    elif usdc_price > 1.01:
        return "SELL"
    else:
        return "HOLD"

def get_prices():
    """
    Obtiene los precios actuales de los tokens
    """
    # En la práctica, necesitarías usar una API para obtener los precios
    # Este es un ejemplo de precios ficticios
    return {
        "USDC": 1.00,
        "RON": 0.001,
        "WRON": 0.001,
        "SLP": 0.0005,
        "AXS": 0.5,
        "WETH": 0.0005
    }