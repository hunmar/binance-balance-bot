# Binance Balance Bot

This Python script balances USDT between your Spot and Futures wallets on Binance using the Binance API.

## Features

- Fetches the current USDT balance in both Spot and Futures wallets.
- Transfers USDT to balance the amount evenly between both wallets.
- Supports balancing BNB between Spot and Futures wallets.

## Requirements

- Python 3.7+
- Binance API key and secret

## Installation

1. **Clone the repository**:
    ```
    git clone https://github.com/hunmar/binance-balance-bot.git
    cd binance-balance-bot
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Copy `.env.example` to `.env` and fill in your Binance API key and secret**:
    ```
    cp .env.example .env
    ```

5. **Edit `.env` and add your Binance API key and secret**:
    ```
    BINANCE_API_KEY=your_api_key
    BINANCE_API_SECRET=your_api_secret
    ```

## Usage

Run the script to balance your USDT between Spot and Futures wallets:

    ```
    python balance_wallets.py
    ```

## Setting Up a Cron Job

To automate the process of balancing your wallets, you can set up a cron job that runs the script at regular intervals.

1. **Create a shell script to activate the virtual environment and run the Python script**:

   Create a file named `run_balance_bot.sh` with the following content:

   ```
   #!/bin/bash

   # Define log file
   LOGFILE="/path/to/your/binance-balance-bot/cron.log"

   # Log start time
   echo "Running script at $(date)" >> $LOGFILE

   # Activate virtual environment and run the script, capturing both stdout and stderr
   source /path/to/your/binance-balance-bot/venv/bin/activate && /path/to/your/binance-balance-bot/venv/bin/python /path/to/your/binance-balance-bot/balance_wallets.py >> $LOGFILE 2>&1

   # Log end time
   echo "Finished script at $(date)" >> $LOGFILE
   ```

   - Replace `/path/to/your/binance-balance-bot` with the actual path to your project directory.

2. **Make the shell script executable**:
    ```
    chmod +x /path/to/your/binance-balance-bot/run_balance_bot.sh
    ```

3. **Open your crontab file**:
    ```
    crontab -e
    ```

4. **Add the following line to run the script every day at midnight**:

    ```
    0 0 * * * /path/to/your/binance-balance-bot/run_balance_bot.sh
    ```

    This cron job will execute the script every day at midnight.

5. **Save and exit**. This will set up a cron job that runs the script at the specified interval and logs the output to `cron.log`.

### Example Paths

If your project is located at `/home/user/binance-balance-bot` and your virtual environment is in the same directory, the crontab line might look like this:

    ```
    0 0 * * * /home/user/binance-balance-bot/run_balance_bot.sh
    ```

### Log File

The output of the script, including any errors, will be logged in the `cron.log` file specified in the shell script. You can check this log file to troubleshoot and verify the execution of the cron job.

### Adjustable Wallet Balance Ratios

#### USDT Balance Configuration

The Binance Balance Bot supports an adjustable Spot/Futures wallet balance ratio for USDT. This allows you to specify the desired balance between your Spot and Futures wallets.

#### USDT Configuration

You can set the desired balance ratio for the Spot wallet using environment variables:

1. **`BALANCE_SPOT_RATIO`**:
   - This environment variable determines the percentage of the total USDT balance that should be allocated to the Spot wallet.
   - The value should be an integer between 0 and 100.
   - The Futures wallet will automatically receive the remaining percentage of the total balance.

   Example:
   - If you set `BALANCE_SPOT_RATIO=60`, the bot will ensure that 60% of the total USDT balance is in the Spot wallet and 40% is in the Futures wallet.

#### BNB Balance Configuration (New Feature)

The bot now also supports balancing BNB between your Spot and Futures wallets, with customizable configuration options.

To enable and configure BNB balancing, use the following environment variables:

1. **`BALANCE_BNB`**:
   - Set to `true` to enable BNB balancing, or `false` to disable it.
   - Default: `false`

2. **`BNB_SPOT_RATIO`**:
   - Percentage of total BNB balance to allocate to the Spot wallet.
   - Value should be between 0 and 100.
   - Default: `50`

3. **`BNB_FUTURES_RATIO`**:
   - Percentage of total BNB balance to allocate to the Futures wallet.
   - This is automatically calculated as `100 - BNB_SPOT_RATIO`.

4. **`BNB_MIN_DIFF_PERCENT`**:
   - Minimum percentage difference required to trigger a BNB transfer between wallets.
   - Default: `5`

#### Example `.env` Configuration:

```
# API credentials
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# USDT balance configuration
BALANCE_SPOT_RATIO=60

# BNB balance configuration
BALANCE_BNB=true
BNB_SPOT_RATIO=70
BNB_MIN_DIFF_PERCENT=5
```

With this configuration:
- 60% of your total USDT will be allocated to the Spot wallet.
- BNB balancing is enabled, with 70% of your total BNB allocated to the Spot wallet.
- The bot will only transfer BNB if the balance difference exceeds 5% of the total BNB balance.
