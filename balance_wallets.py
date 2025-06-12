import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys and balance ratio from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
BALANCE_SPOT_RATIO = float(os.getenv('BALANCE_SPOT_RATIO', 50))  # Default to 50 if not set
BALANCE_FUTURES_RATIO = float(os.getenv('BALANCE_FUTURES_RATIO', 50))  # Default to 50 if not set

# BNB balance configuration
BALANCE_BNB = os.getenv('BALANCE_BNB', 'false').lower() == 'true'  # Default to false
BNB_SPOT_RATIO = float(os.getenv('BNB_SPOT_RATIO', 50))  # Default to 50 if not set
BNB_FUTURES_RATIO = float(os.getenv('BNB_FUTURES_RATIO', 50))  # Default to 50 if not set
BNB_MIN_DIFF_PERCENT = float(os.getenv('BNB_MIN_DIFF_PERCENT', 5))  # Minimum difference to trigger a transfer

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def get_balance(wallet_type, asset='USDT'):
    """Retrieve the balance for a specific wallet (Spot or Futures)"""
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
    """Transfer funds between Spot and Futures wallets"""
    try:
        if from_wallet == 'spot' and to_wallet == 'futures':
            result = client.futures_account_transfer(asset=asset, amount=amount, type=1)
        elif from_wallet == 'futures' and to_wallet == 'spot':
            result = client.futures_account_transfer(asset=asset, amount=amount, type=2)
        else:
            raise ValueError("Invalid wallet types for transfer.")
        print(f"Transfer successful: {amount} {asset} from {from_wallet} to {to_wallet}")
        return result
    except BinanceAPIException as e:
        print(f"Error transferring funds: {e}")
        return None

def balance_wallets_for_asset(asset='USDT', spot_ratio=None, futures_ratio=None, min_diff_percent=5):
    """Balance the Spot and Futures wallets for a specific asset"""
    spot_balance = get_balance('spot', asset)
    futures_balance = get_balance('futures', asset)

    print(f"\n--- Balancing {asset} ---")
    print(f"Spot Wallet Balance: {spot_balance} {asset}")
    print(f"Futures Wallet Balance: {futures_balance} {asset}")

    total_balance = spot_balance + futures_balance
    if total_balance == 0:
        print(f"No {asset} balance found in either wallet.")
        return

    print(f"Total Balance (Spot + Futures): {total_balance} {asset}")

    # Adjust based on Spot ratio or Futures ratio
    if spot_ratio is not None:  # If Spot ratio is provided
        spot_target = total_balance * (spot_ratio / 100)
        futures_target = total_balance - spot_target
        print(f"Target Spot Wallet Balance: {spot_target} {asset} ({spot_ratio}% of total balance)")
        print(f"Target Futures Wallet Balance: {futures_target} {asset} ({100 - spot_ratio}% of total balance)")
    elif futures_ratio is not None:  # If Futures ratio is provided
        futures_target = total_balance * (futures_ratio / 100)
        spot_target = total_balance - futures_target
        print(f"Target Futures Wallet Balance: {futures_target} {asset} ({futures_ratio}% of total balance)")
        print(f"Target Spot Wallet Balance: {spot_target} {asset} ({100 - futures_ratio}% of total balance)")
    else:
        # Default to 50/50 if neither ratio is provided
        spot_target = total_balance * 0.5
        futures_target = total_balance * 0.5
        print(f"Target Spot Wallet Balance: {spot_target} {asset} (50% of total balance)")
        print(f"Target Futures Wallet Balance: {futures_target} {asset} (50% of total balance)")

    # Calculate the percentage difference
    if total_balance > 0:
        balance_diff_percentage = abs(spot_balance - spot_target) / total_balance * 100
        print(f"Balance Difference: {balance_diff_percentage:.2f}%")

        if balance_diff_percentage > min_diff_percent:  # If the difference is more than the minimum percentage
            if spot_balance > spot_target:
                amount_to_transfer = spot_balance - spot_target
                print(f"Transferring {amount_to_transfer:.8f} {asset} from Spot to Futures...")
                transfer_funds('spot', 'futures', amount_to_transfer, asset)
            elif futures_balance > futures_target:
                amount_to_transfer = futures_balance - futures_target
                print(f"Transferring {amount_to_transfer:.8f} {asset} from Futures to Spot...")
                transfer_funds('futures', 'spot', amount_to_transfer, asset)
        else:
            print(f"The balance difference is less than {min_diff_percent}%. No transfer required.")

        # Show updated balances
        spot_balance = get_balance('spot', asset)
        futures_balance = get_balance('futures', asset)
        print(f"Updated Spot Wallet Balance: {spot_balance} {asset}")
        print(f"Updated Futures Wallet Balance: {futures_balance} {asset}")

def balance_wallets():
    """Balance the Spot and Futures wallets for all configured assets"""
    # Balance USDT
    balance_wallets_for_asset(
        asset='USDT',
        spot_ratio=BALANCE_SPOT_RATIO if BALANCE_SPOT_RATIO != 50 else None,
        futures_ratio=BALANCE_FUTURES_RATIO if BALANCE_SPOT_RATIO == 50 else None,
        min_diff_percent=5
    )
    
    # Balance BNB if enabled
    if BALANCE_BNB:
        balance_wallets_for_asset(
            asset='BNB',
            spot_ratio=BNB_SPOT_RATIO if BNB_SPOT_RATIO != 50 else None,
            futures_ratio=BNB_FUTURES_RATIO if BNB_SPOT_RATIO == 50 else None,
            min_diff_percent=BNB_MIN_DIFF_PERCENT
        )

if __name__ == "__main__":
    balance_wallets()
