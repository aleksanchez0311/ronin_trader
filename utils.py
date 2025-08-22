from config import W3

def get_token_price(token_in, token_out, amount_in):
    """Obtiene el precio estimado de swap usando Katana Router (view function)"""
    # Aquí deberías usar `getAmountsOut` del router
    # Pero necesitas el contrato cargado
    from web3.contract import Contract
    router = W3.eth.contract(address="0x2cCb8C89aBBDF3a366a39797C809c7957896c841", abi=[
        {
            "inputs": [{"type": "uint256", "name": "amountIn"}, {"type": "address[]", "name": "path"}],
            "name": "getAmountsOut",
            "outputs": [{"type": "uint256[]", "name": "amounts"}],
            "stateMutability": "view",
            "type": "function"
        }
    ])
    try:
        amounts = router.functions.getAmountsOut(amount_in, [token_in, token_out]).call()
        return amounts[1]
    except Exception as e:
        print("Error al obtener precio:", e)
        return 0