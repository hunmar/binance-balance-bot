# Binance Balance Bot

This Python script balances USDT between your Spot and Futures wallets on Binance using the Binance API.

## Features

- Fetches the current USDT balance in both Spot and Futures wallets.
- Transfers USDT to balance the amount evenly between both wallets.

## Requirements

- Python 3.7+
- Binance API key and secret

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/binance-balance-bot.git
    cd binance-balance-bot
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Copy `.env.example` to `.env` and fill in your Binance API key and secret**:
    ```sh
    cp .env.example .env
    ```

5. **Edit `.env` and add your Binance API key and secret**:
    ```ini
    BINANCE_API_KEY=your_api_key
    BINANCE_API_SECRET=your_api_secret
    ```

## Usage

Run the script to balance your USDT between Spot and Futures wallets:

```sh
python balance_wallets.py
