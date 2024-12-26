#!/bin/bash

# Define log file
LOGFILE="/home/hunmar/binance-balance-bot/cron.log"

# Log start time
echo "Running script at $(date)" >> $LOGFILE

source /home/hunmar/binance-balance-bot/venv/bin/activate
python3 /home/hunmar/binance-balance-bot/balance_wallets.py >> $LOGFILE 2>&1

# Log end time
echo "Finished script at $(date)" >> $LOGFILE
