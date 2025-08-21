# socket_api.py
import requests
from decouple import config
from config import CHAIN_ID

SOCKET_API_KEY = config("SOCKET_API_KEY")
SOCKET_URL = "https://api.socket.tech/v2/quote"

headers = {
    "Accept": "application/json",
    "API-KEY": SOCKET_API_KEY
}

def get_swap_route(from_token, to_token, amount, from_address):
    params = {
        "fromChainId": CHAIN_ID,
        "toChainId": CHAIN_ID,
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "amount": str(amount),
        "fromAddress": from_address
    }
    try:
        response = requests.get(SOCKET_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            route = data['result']['route']
            return {
                'txData': route['txData'],
                'to': route['to'],
                'gasCost': int(route['gasCost']),
                'toAmount': route['toAmount'],
                'fromAmount': amount
            }
        else:
            print(f"Socket error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error en Socket API: {e}")
        return None