# test/query_wallet_test.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wallet import get_all_balances
from decouple import config

wallet_address = config("WALLET_ADDRESS")
print(f"🔍 Consultando balances para: {wallet_address}")

balances = get_all_balances(wallet_address)
print("✅ Balances obtenidos:")
for token, amount in balances.items():
    print(f"  {token}: {amount:.6f}")