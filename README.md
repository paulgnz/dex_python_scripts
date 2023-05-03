# dex_python_scripts
various python scripts for protondex

https://api-docs.protondex.com/

## Trades

### Get Trades History

To get the trades history for a specific account, market and number of hours in the past to look for, use the following command:

```python dex.py trades history <account> <market> <hours>```

For Example

```python dex.py trades history paul XDOGE_XMD 24```

### Get Daily Stats

To get the daily stats for a specific market, use the following command:

```python dex.py trades daily <market>```

For Example

```python dex.py trades daily XDOGE_XMD```



### Why Proton DEX?
Proton DEX allows users to trade all available cryptos on the exchange and offers what most of the CEX's offer nowadays - Orderbook, different types of orders (Limit order, Market order, Stop loss order, Take profit order,) and trading view chart integration. The DEX also allows users to manage their orders - view or cancel active orders as well as view order history.

Proton Blockchains offers no gas fees to users, this combined with the secure DeFi wallet Webauth, offers the best decentralized trading experience!

Learn more about the Proton blockchain and ecosystem in this overview.

https://docs.protondex.com/dex/what-is-proton-dex/proton-dex-faq

