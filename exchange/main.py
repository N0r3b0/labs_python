from wallet_generator import generate_wallets, show_wallets
from exchange_api import fetch_exchange_rates
import argparse

def main():
    parser = argparse.ArgumentParser(description="Currency Wallet Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate wallets command
    gen_parser = subparsers.add_parser("generate", help="Generate random wallets for available currencies")
    gen_parser.add_argument("--show", action="store_true", help="Display generated wallets")

    # Show rates command
    rates_parser = subparsers.add_parser("rates", help="Show current exchange rates")

    # Calculate value command
    calc_parser = subparsers.add_parser("calculate", help="Calculate total value in specified currency")
    calc_parser.add_argument("currency", help="Target currency code (e.g., USD, EUR)")
    calc_parser.add_argument("values", nargs="+", help="Currency values in format CODE:AMOUNT (e.g., USD:100 EUR:50)")

    args = parser.parse_args()

    if args.command == "generate":
        wallets = generate_wallets()
        if args.show:
            print("\nGenerated Wallets:")
            show_wallets(wallets)
        return wallets

    elif args.command == "rates":
        rates = fetch_exchange_rates()
        print("\nCurrent Exchange Rates (to PLN):")
        for code, rate in rates.items():
            print(f"{code}: {rate:.4f}")

    elif args.command == "calculate":
        rates = fetch_exchange_rates()
        if args.currency not in rates:
            print(f"Error: Currency {args.currency} not found in exchange rates")
            return

        total = 0
        for value_str in args.values:
            try:
                code, amount = value_str.split(":")
                amount = float(amount)
                if code not in rates:
                    print(f"Warning: Currency {code} not found - skipping")
                    continue
                total += amount * rates[code]
            except ValueError:
                print(f"Warning: Invalid format for '{value_str}' - skipping")

        # Convert total to target currency
        target_rate = rates[args.currency]
        result = total / target_rate

        print(f"\nTotal value in {args.currency}: {result:.2f}")

if __name__ == "__main__":
    main()