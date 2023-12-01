import os
import json
import requests
from pyeoskit import eosapi, wallet
from math import pow
import argparse

def get_dogecoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['dogecoin']['usd']
    else:
        print("Error fetching Dogecoin price")
        return None


def main(order_side, amount_xmd):

    dogecoin_price = get_dogecoin_price()
    if dogecoin_price is None:
        print("Error fetching Dogecoin price. Exiting.")
        return
    

    # Import your account private key here
    wallet.import_key('mywallet', 'PVT_K1')

    #For testnet use https://protontestnet.greymass.com
    eosapi.set_node('https://proton.greymass.com')
    info = eosapi.get_info()
    print(info)

    # Replace with your account name
    USERNAME = 'trading.paul'
    permission = {USERNAME: 'active'}

    # Replace Trade Parameters
    BID_TOKEN_CONTRACT = 'xtokens'
    BID_TOKEN_SYMBOL = 'XDOGE'
    BID_TOKEN_PRECISION = 6
    BID_AMOUNT = amount_xmd / dogecoin_price * 1.05  # Amount of XDOGE to use for sell order
    

    ASK_TOKEN_CONTRACT = 'xmd.token'
    ASK_TOKEN_SYMBOL = 'XMD'
    ASK_TOKEN_PRECISION = 6
    ASK_AMOUNT = amount_xmd # Amount of XMD to use for buy order

    MARKET_ID = 12  # Unique ID of market
    PRICE = dogecoin_price  # Price of XDOGE/XMD to place order at
    print("The price of DOGECOIN is " + str(PRICE))
    if order_side.lower() == "buy":
        ORDER_SIDE = 1
    else:
        ORDER_SIDE = 2
    ASK_AMOUNT = amount_xmd
    ORDER_TYPE = 1  # Limit Order
    FILL_TYPE = 1  # Good Till Cancel

    if ORDER_SIDE == 1:
        token_contract = ASK_TOKEN_CONTRACT
        token_symbol = ASK_TOKEN_SYMBOL
        token_precision = ASK_TOKEN_PRECISION
        amount = ASK_AMOUNT
        market_price = 9223372036854775806
    else:
        token_contract = BID_TOKEN_CONTRACT
        token_symbol = BID_TOKEN_SYMBOL
        token_precision = BID_TOKEN_PRECISION
        amount = BID_AMOUNT
        market_price = int(1)

    args1 = {
        'from': USERNAME,
        'to': 'dex',
        'quantity': f'{amount:.{token_precision}f} {token_symbol}',
        'memo': ''
    }

    args2 = {
        'market_id': MARKET_ID,
        'account': USERNAME,
        'order_type': ORDER_TYPE,
        'order_side': ORDER_SIDE,
        'fill_type': FILL_TYPE,
        'bid_symbol': {
            'sym': f'{BID_TOKEN_PRECISION},{BID_TOKEN_SYMBOL}',
            'contract': BID_TOKEN_CONTRACT
        },
        'ask_symbol': {
            'sym': f'{ASK_TOKEN_PRECISION},{ASK_TOKEN_SYMBOL}',
            'contract': ASK_TOKEN_CONTRACT
        },
        'referrer': '',
        'quantity': int(amount * pow(10, token_precision)),
        'price': market_price,
        'trigger_price': 0
    }

    args3 = {
        'q_size': 20,
        'show_error_msg': 0
    }

    a1 = [token_contract, 'transfer', args1, permission]
    a2 = ['dex', 'placeorder', args2, permission]
    a3 = ['dex', 'process', args3, permission]

    if ORDER_SIDE == 1:
        print(f"Placing a buy order for {BID_AMOUNT:.8f} XDOGE (equivalent to {ASK_AMOUNT:.6f} XMD)")
    else:
        print(f"Placing a sell order for {BID_AMOUNT:.8f} XDOGE (equivalent to {ASK_AMOUNT:.6f} XMD)")

    eosapi.push_actions([a1, a2, a3])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trade XDOGE on SuchDEX.com")
    parser.add_argument("order_side", choices=["buy", "sell"], help="Choose between 'buy' and 'sell'")
    parser.add_argument("amount_xmd", type=float, help="Amount of XMD to use for the trade")

    args = parser.parse_args()
    main(args.order_side, args.amount_xmd)
