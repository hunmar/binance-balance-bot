import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def get_balance(wallet_type, asset='USDT'):
    if wallet_type == 'spot':
        account_info = client.get_account()
        for balance in account_info['balances']:
            if balance['asset'] == asset:
                return float(balance['free'])
    elif wallet_type == 'futures':
        account_info = client.futures_account()
        for asset_info in account_info['assets']:
            if asset_info['asset'] == asset:
                return float(asset_info['availableBalance'])
    return 0.0

def transfer_funds(from_wallet, to_wallet, amount, asset='USDT'):
    try:
        if from_wallet == 'spot' and to_wallet == 'futures':
            result = client.futures_account_transfer(asset=asset, amount=amount, type=1)
        elif from_wallet == 'futures' and to_wallet == 'spot':
            result = client.futures_account_transfer(asset=asset, amount=amount, type=2)
        else:
            raise ValueError("Invalid wallet types for transfer.")
        return result
    except BinanceAPIException as e:
        print(f"Error transferring funds: {e}")
        return None

def balance_wallets():
    spot_balance = get_balance('spot')
    futures_balance = get_balance('futures')

    print(f"Spot Wallet Balance: {spot_balance} USDT")
    print(f"Futures Wallet Balance: {futures_balance} USDT")

    total_balance = spot_balance + futures_balance
    desired_balance = total_balance / 2

    # Calculate the percentage difference between the Spot and Futures balances
    balance_diff_percentage = abs(spot_balance - futures_balance) / total_balance * 100

    if balance_diff_percentage > 5:  # If the difference is more than 5%
        if spot_balance > desired_balance:
            amount_to_transfer = spot_balance - desired_balance
            print(f"Transferring {amount_to_transfer} USDT from Spot to Futures...")
            transfer_funds('spot', 'futures', amount_to_transfer)
        elif futures_balance > desired_balance:
            amount_to_transfer = futures_balance - desired_balance
            print(f"Transferring {amount_to_transfer} USDT from Futures to Spot...")
            transfer_funds('futures', 'spot', amount_to_transfer)
    else:
        print("The balance difference is less than 5%. No transfer required.")

    # Show updated balances
    spot_balance = get_balance('spot')
    futures_balance = get_balance('futures')
    print(f"Updated Spot Wallet Balance: {spot_balance} USDT")
    print(f"Updated Futures Wallet Balance: {futures_balance} USDT")

if __name__ == "__main__":
    balance_wallets()
