import requests
import json
import time

url = "http://127.0.0.1:5000/webhook"
headers = {"Content-Type": "application/json"}

# 1. Test Buy Signal
payload_buy = {
    "action": "buy",
    "ticker": "BTC/USDT",
    "price": 45000.50
}

print(f"Sending BUY request to {url}...")
try:
    response = requests.post(url, data=json.dumps(payload_buy), headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Failed to connect:", e)
    print("Make sure bot_server.py is running!")

print("-" * 30)
time.sleep(1)

# 2. Test Sell Signal
payload_sell = {
    "action": "sell",
    "ticker": "BTC/USDT",
    "price": 46000.00
}

print(f"Sending SELL request to {url}...")
try:
    response = requests.post(url, data=json.dumps(payload_sell), headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Failed to connect:", e)
