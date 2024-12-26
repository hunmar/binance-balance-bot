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

#### New Feature: Adjustable Spot/Futures Balance Ratio

The Binance Balance Bot now supports an adjustable Spot/Futures wallet balance ratio. This allows you to specify the desired balance between your Spot and Futures wallets without needing to manually calculate percentages for each wallet.

#### Configuration

You can set the desired balance ratio for the Spot wallet using an environment variable. The bot will automatically adjust the balance to match the ratio you specify.

1. **`BALANCE_SPOT_RATIO`**:
   - This environment variable determines the percentage of the total balance that should be allocated to the Spot wallet.
   - The value should be an integer between 0 and 100.
   - The Futures wallet will automatically receive the remaining percentage of the total balance.

   Example:
   - If you set `BALANCE_SPOT_RATIO=50`, the bot will ensure that 50% of the total balance is in the Spot wallet and 50% is in the Futures wallet.

#### Example Usage:

1. **Set the Balance Ratio**:
   Set the `BALANCE_SPOT_RATIO` variable in your `.env` file or environment before running the bot.

   Example `.env`:
   ```
   BALANCE_SPOT_RATIO=60
   ```

2. **Running the Bot**:
   The bot will check the current balances in the Spot and Futures wallets and calculate the difference. If the balance difference exceeds 5% from the desired ratio, it will transfer funds between the wallets to achieve the target balance.

#### How It Works:

- The bot first checks the current balance of both the Spot and Futures wallets.
- It calculates the total balance (Spot + Futures).
- Using the `BALANCE_SPOT_RATIO`, the bot determines the amount of funds that should be in the Spot wallet.
- If the current Spot balance deviates by more than 5% from the target, it will automatically transfer funds between Spot and Futures to achieve the desired balance ratio.

#### Example Scenario:

- **Total Balance**: 1000 USDT (500 USDT in Spot and 500 USDT in Futures)
- **Desired Spot Ratio**: 60%
- The bot will calculate:
  - Desired Spot Balance: 60% of 1000 = 600 USDT
  - Current Spot Balance: 500 USDT
- Since the Spot balance is less than 600 USDT, the bot will transfer 100 USDT from the Futures wallet to the Spot wallet.
