# trades.py
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://mainnet.api.protondex.com"

def get_trades_history(account, market, hours):
    url = f"{BASE_URL}/dex/v1/trades/history?account={account}&symbol={market}&offset=0&limit=100"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    trade_data = json.loads(response.text)

    past_time = datetime.utcnow() - timedelta(hours=hours)

    purchased = 0
    sold = 0

    for trade in trade_data['data']:
        trade_time = datetime.strptime(trade['block_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if trade_time > past_time:
            if trade['order_side'] == 1:  # Buy order (purchased)
                purchased += trade['bid_amount']
            elif trade['order_side'] == 0:  # Sell order (sold)
                sold += trade['ask_amount']

    return purchased, sold

def get_daily_stats(account):
    url = f"{BASE_URL}/dex/v1/trades/daily?account={account}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    daily_stats = response.json()

    return daily_stats

def get_recent_trades(market, offset, limit):
    url = f"{BASE_URL}/dex/v1/trades/recent?symbol={market}&offset={offset}&limit={limit}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    recent_trades = response.json()

    return recent_trades


def trades_history(args):
    purchased, sold = get_trades_history(args.account, args.market, args.hours)
    print(f"Purchased {args.market} in the last {args.hours} hours:", purchased)
    print(f"Sold {args.market} in the last {args.hours} hours:", sold)

def trades_daily(args):
    daily_stats = get_daily_stats(args.account)
    
    # Display daily stats (modify this part based on your requirements)
    for stat in daily_stats["data"]:
        print(f"{stat['symbol']}:")
        print(f"  High: {stat['high']}")
        print(f"  Low: {stat['low']}")
        print(f"  Open: {stat['open']}")
        print(f"  Close: {stat['close']}")
        print(f"  Volume Bid: {stat['volume_bid']}")
        print(f"  Volume Ask: {stat['volume_ask']}\n")

def trades_recent(args):
    recent_trades = get_recent_trades(args.market, args.offset, args.limit)
    
    # Display recent trades (modify this part based on your requirements)
    for trade in recent_trades["data"]:
        print(f"Trade ID: {trade['trade_id']}")
        print(f"  Market: {trade['market_id']}")
        print(f"  Price: {trade['price']}")
        print(f"  Block Time: {trade['block_time']}")
        print(f"  Bid User: {trade['bid_user']}")
        print(f"  Ask User: {trade['ask_user']}\n")
