# test\swap_api_test.py
import sys
import os 

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from swap_api import get_swap_route
from config import TOKENS
import time

def test_swap_route():
    # Par de tokens: RON → USDT
    from_token = "0x5555555555555555555555555555555555555555"  # RON
    to_token = TOKENS["USDC"]
    amount = "1000000000000000000"  # 1 RON (18 decimales)
    from_address = "0x44dd8E1597DE12636Bb286d06E6437a80031ccB6"

    print("🔍 Solicitando ruta de swap: RON → USDT")
    
    try:
        route = get_swap_route(from_token, to_token, amount, from_address)
        
        if route:
            print("✅ Ruta obtenida exitosamente")
            print(f"  To: {route['to']}")
            print(f"  TxData: {route['txData'][:40]}...")
            print(f"  To Amount: {route['toAmount']}")
            print(f"  Gas Cost: {route['gasCost']}")
            return True
        else:
            print("❌ No se pudo obtener ruta de swap")
            return False
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    if test_swap_route():
        print("✅ Swap API test: OK")
    else:
        print("❌ Swap API test: FALLÓ")