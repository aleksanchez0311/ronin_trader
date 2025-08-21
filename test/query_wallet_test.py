from wallet import get_all_balances
from decouple import config

wallet_address = config("WALLET_ADDRESS")
print("Balances:", get_all_balances(wallet_address))