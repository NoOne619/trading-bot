import os
from dotenv import load_dotenv

load_dotenv()

# Exchange Configuration (Binance Testnet Example)
API_KEY = os.getenv("API_KEY", "CO**********************")
API_SECRET = os.getenv("API_SECRET", "QC***********************")
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binanceusdm") # 'binance' for spot, 'binanceusdm' for futures
TESTNET = True

# Trading Settings
SYMBOL = "BTC/USDT"
ORDER_SIZE = 0.003  # Amount to buy/sell (0.003 * ~95k = ~285 USDT > 100)

# Webhook Settings
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE", "secret_passphrase")
