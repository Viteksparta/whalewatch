import requests
from datetime import datetime, timedelta

ETHERSCAN_API = "https://api.etherscan.io/api"
API_KEY = "YourApiKeyToken"  # <-- замените на свой ключ

class WhaleTracker:
    def __init__(self, addresses, min_value_usd=100_000):
        self.addresses = addresses
        self.min_value_usd = min_value_usd

    def fetch_transactions(self, address):
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": API_KEY
        }
        response = requests.get(ETHERSCAN_API, params=params)
        data = response.json()
        return data["result"] if data["status"] == "1" else []

    def filter_large_tx(self, tx_list):
        large_tx = []
        for tx in tx_list:
            eth_value = int(tx["value"]) / 1e18
            if eth_value * self._get_eth_price() > self.min_value_usd:
                large_tx.append({
                    "hash": tx["hash"],
                    "from": tx["from"],
                    "to": tx["to"],
                    "value_eth": eth_value,
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"]))
                })
        return large_tx

    def _get_eth_price(self):
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        return response.json()["ethereum"]["usd"]
