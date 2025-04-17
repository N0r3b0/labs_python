import requests

def fetch_exchange_rates():
    url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {entry["code"]: entry["mid"] for entry in data[0]["rates"]}
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return {}
