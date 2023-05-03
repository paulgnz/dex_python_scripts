# dex.py

import argparse
import requests
import json
from datetime import datetime, timedelta
from functions.trades import trades_history, trades_daily, trades_recent

def main():
    parser = argparse.ArgumentParser(description="CLI tool for managing various functions")
    
    subparsers = parser.add_subparsers()

    # Trades subparser
    trades_parser = subparsers.add_parser("trades", help="Trades related functions")
    trades_subparsers = trades_parser.add_subparsers()

    # Trades history subparser
    trades_history_parser = trades_subparsers.add_parser("history", help="Get trades history")
    trades_history_parser.add_argument("account", help="The account to fetch the trades history for")
    trades_history_parser.add_argument("market", help="The market symbol (e.g., XDOGE_XMD)")
    trades_history_parser.add_argument("hours", type=int, help="The number of hours to look back")
    trades_history_parser.set_defaults(func=trades_history)

    # Trades daily subparser
    trades_daily_parser = trades_subparsers.add_parser("daily", help="Get daily stats")
    trades_daily_parser.add_argument("account", help="The account to fetch the daily stats for")
    trades_daily_parser.set_defaults(func=trades_daily)

    # Trades recent subparser
    trades_recent_parser = trades_subparsers.add_parser("recent", help="Get recent trades")
    trades_recent_parser.add_argument("market", help="The market symbol (e.g., XDOGE_XMD)")
    trades_recent_parser.add_argument("offset", type=int, help="The offset for recent trades")
    trades_recent_parser.add_argument("limit", type=int, help="The number of recent trades to fetch")
    trades_recent_parser.set_defaults(func=trades_recent)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
