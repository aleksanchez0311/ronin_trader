# swap_api.py
import requests
from decouple import config
from config import CHAIN_ID, TOKENS

def get_swap_route_li_fi(from_token, to_token, amount, from_address):
    """Obtiene ruta de swap usando Li.Fi (primera opción)"""
    li_fi_api_key = config("LI_FI_API_KEY")
    if not li_fi_api_key:
        print("❌ No hay API Key de Li.Fi")
        return None
    
    url = "https://li.quest/v1/swap"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {li_fi_api_key}"
    }
    params = {
        "fromChain": "ronin",
        "toChain": "ronin",
        "fromToken": from_token,
        "toToken": to_token,
        "amount": str(amount),
        "fromAddress": from_address,
        "slippage": 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code in [401, 403, 404]:
            print(f"❌ Li.Fi falló con código {response.status_code}")
            return None
            
        response.raise_for_status()
        
        data = response.json()
        if "data" in data and "swap" in data["data"]:
            swap = data["data"]["swap"]
            return {
                'txData': swap['data'],
                'to': swap['to'],
                'gasCost': swap['gas'],
                'toAmount': swap['toAmount'],
                'fromAmount': amount
            }
        else:
            print(f"❌ Respuesta no esperada: {data}")
            return None
            
    except Exception as e:
        print(f"Li.Fi error: {e}")
        return None

def get_swap_route_socket(from_token, to_token, amount, from_address):
    """Obtiene ruta de swap usando Socket (respaldo)"""
    socket_api_key = config("SOCKET_API_KEY")
    if not socket_api_key:
        print("❌ No hay API Key de Socket")
        return None
    
    url = "https://api.socket.tech/v2/quote"
    headers = {
        "Accept": "application/json",
        "API-KEY": socket_api_key
    }
    params = {
        "fromChainId": CHAIN_ID,
        "toChainId": CHAIN_ID,
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "amount": str(amount),
        "fromAddress": from_address
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code in [401, 403, 404]:
            print(f"❌ Socket falló con código {response.status_code}")
            return None
            
        response.raise_for_status()
        
        data = response.json()
        if "result" in data and "route" in data["result"]:
            route = data["result"]["route"]
            return {
                'txData': route['txData'],
                'to': route['to'],
                'gasCost': int(route['gasCost']),
                'toAmount': route['toAmount'],
                'fromAmount': amount
            }
        else:
            print(f"❌ Respuesta no esperada: {data}")
            return None
            
    except Exception as e:
        print(f"Socket error: {e}")
        return None

def get_swap_route(from_token, to_token, amount, from_address):
    """Intenta Li.Fi primero, luego Socket si falla"""
    print("🔍 Intentando Li.Fi...")
    route = get_swap_route_li_fi(from_token, to_token, amount, from_address)
    if route:
        print("✅ Usando Li.Fi para ruta de swap")
        return route
    
    print("⚠️ Li.Fi falló, intentando Socket como respaldo...")
    return get_swap_route_socket(from_token, to_token, amount, from_address)