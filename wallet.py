# wallet.py
from web3 import Web3
from decouple import config
from config import RONIN_RPC, TOKENS, DECIMALS

web3 = Web3(Web3.HTTPProvider(config("RONIN_RPC_URL")))

def get_balance(token_symbol, wallet_address):
    address = web3.to_checksum_address(wallet_address)
    if token_symbol == "RON":
        balance = web3.eth.get_balance(address)
        return balance / 10**18
    else:
        token_address = web3.to_checksum_address(TOKENS[token_symbol])
        contract = web3.eth.contract(
            address=token_address,
            abi=[{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]
        )
        balance = contract.functions.balanceOf(address).call()
        decimals = DECIMALS.get(token_symbol, 18)
        return balance / (10 ** decimals)

def get_all_balances(wallet_address):
    balances = {}
    for symbol in TOKENS.keys():
        try:
            bal = get_balance(symbol, wallet_address)
            if bal > 0:
                balances[symbol] = round(bal, 6)
        except:
            balances[symbol] = 0
    return balances