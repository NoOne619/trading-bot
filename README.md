# Crypto Trading Bot (Assignment #4)

## Overview
A fully automated trading bot using TradingView (Pine Script) for signals and Python (FastAPI + CCXT) for execution on a Testnet Exchange.

## Components
1. **TradingView Strategy**: `trading_strategy.pine` - Generates Buy/Sell signals via Webhooks.
2. **Python Server**: `bot_server.py` - Receives webhooks and executes trades.
3. **Configuration**: `config.py` - API keys and settings.
4. **Testing**: `test_webhook.py` - Script to simulate TradingView alerts.

## Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
1.  Go to [Binance Futures Testnet](https://testnet.binancefuture.com/en/futures/BTCUSDT).
2.  Login/Register and get your **API Key** and **Secret Key**.
3.  Open `config.py` in your code editor.
4.  Replace `YOUR_TESTNET_API_KEY` and `YOUR_TESTNET_API_SECRET` with your actual keys.
    *(Alternatively, create a `.env` file with `API_KEY=...` and `API_SECRET=...`)*.

### 3. Local Testing (Verify Exchange Connection)
Before connecting TradingView, verify your code can talk to Binance Testnet.

1.  **Start the Server**:
    Open a terminal and run:
    ```bash
    python bot_server.py
    ```
    *Keep this terminal open.*

2.  **Send Mock Alerts**:
    Open a **second** terminal window and run:
    ```bash
    python test_webhook.py
    ```

3.  **Check Results**:
    - **Terminal 1**: Should show "Received webhook/Placing buy order...".
    - **Terminal 2**: Should show "Response: {'status': 'success', ...}".
    - **trades.csv**: A new file will appear with the trade details.
    - **Binance UI**: Check "Open Orders" or "Order History" on the testnet website.

### 4. Setup TradingView Alert
- Create an Alert in TradingView.
- URL: `http://<YOUR_PUBLIC_IP>:5000/webhook` (Use ngrok for local testing: `ngrok http 5000`).
- Message (JSON):
  ```json
  {"action": "{{strategy.order.action}}", "ticker": "{{ticker}}", "price": {{close}}}
  ```

### 5. Verify
Run the test script to simulate an alert:
```bash
python test_webhook.py
```
Check `trades.csv` for trade logs.
