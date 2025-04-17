from exchange_api import fetch_exchange_rates
from wallet import Wallet

def generate_wallets():
    currency_data = fetch_exchange_rates()
    return [Wallet(code, rate) for code, rate in currency_data.items()]


def show_wallets(wallets):
    for wallet in wallets:
        print(wallet)