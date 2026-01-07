import ccxt
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import logging
from datetime import datetime
import os
import config

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Setup Exchange ---
try:
    exchange_class = getattr(ccxt, config.EXCHANGE_ID)
    exchange = exchange_class({
        'apiKey': config.API_KEY,
        'secret': config.API_SECRET,
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}, # Adjust based on spot vs future
    })
    if config.TESTNET:
        exchange.set_sandbox_mode(True)
    logger.info(f"Initialized {config.EXCHANGE_ID} (Testnet: {config.TESTNET})")
except Exception as e:
    logger.error(f"Failed to initialize exchange: {e}")
    exchange = None

# --- Setup FastAPI ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Data Models ---
class WebhookPayload(BaseModel):
    action: str  # "buy" or "sell"
    ticker: str
    price: float
    passphrase: str = None # Optional security measure

# --- Helper: Log Trade ---
TRADE_FILE = "trades.csv"

def log_trade(action, symbol, price, amount, status, error_msg=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Action": action,
        "Symbol": symbol,
        "Price": price,
        "Amount": amount,
        "Status": status,
        "Error": error_msg
    }])
    
    if not os.path.isfile(TRADE_FILE):
        new_data.to_csv(TRADE_FILE, index=False)
    else:
        new_data.to_csv(TRADE_FILE, mode='a', header=False, index=False)

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    # Read trades
    trades = []
    if os.path.isfile(TRADE_FILE):
        try:
            df = pd.read_csv(TRADE_FILE)
            # Sort by Timestamp descending (newest first)
            trades = df.to_dict(orient="records")[::-1] 
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
    
    return templates.TemplateResponse("index.html", {"request": request, "trades": trades})

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    logger.info(f"Received webhook: {payload}")
    
    # Identify symbol (TradingView might send BTCUSDT, we need BTC/USDT)
    # Simple mapping or usage of config symbol generally preferred for safety
    symbol = config.SYMBOL 
    
    # 1. Validate Passphrase (Optional)
    # if payload.passphrase != config.WEBHOOK_PASSPHRASE:
    #     raise HTTPException(status_code=401, detail="Invalid Passphrase")

    if not exchange:
         return {"status": "error", "message": "Exchange not connected"}

    # 2. Execute Trade
    try:
        side = payload.action.lower()
        amount = config.ORDER_SIZE
        
        if side not in ['buy', 'sell']:
            return {"status": "error", "message": "Invalid action"}

        # Market Order
        logger.info(f"Placing {side} order for {symbol}")
        order = exchange.create_market_order(symbol, side, amount)
        
        logger.info(f"Order executed: {order['id']}")
        log_trade(side, symbol, payload.price, amount, "SUCCESS")
        
        return {"status": "success", "order_id": order['id'], "side": side}

    except Exception as e:
        logger.error(f"Trade failed: {e}")
        log_trade(payload.action, symbol, payload.price, config.ORDER_SIZE, "FAILED", str(e))
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
