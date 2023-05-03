import requests
import json
from datetime import datetime, timedelta

account = "trading.paul" #Put your own account here

url = f"https://mainnet.api.protondex.com/dex/v1/trades/history?account={account}&symbol=XDOGE_XMD&offset=0&limit=100"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
trade_data = json.loads(response.text)

# Get the timestamp 24 hours before the current time
past_24_hours = datetime.utcnow() - timedelta(hours=24)

purchased_xdoge = 0
sold_xdoge = 0

# Iterate through the trade data and filter trades within the past 24 hours
for trade in trade_data['data']:
    trade_time = datetime.strptime(trade['block_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

    if trade_time > past_24_hours:
        if trade['order_side'] == 1:  # Buy order (XDOGE purchased)
            purchased_xdoge += trade['bid_amount']
        elif trade['order_side'] == 0:  # Sell order (XDOGE sold)
            sold_xdoge += trade['ask_amount']

print("Purchased XDOGE in the last 24 hours:", purchased_xdoge)
print("Sold XDOGE in the last 24 hours:", sold_xdoge)
