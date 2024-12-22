# Standard library
import time
import os

# 3rd party
import requests

# Dagster
from dagster import asset

@asset
def ledger_satoshis() -> int:
    api_key = os.environ['BLOCKONOMICS_API_KEY']
    zpub = os.environ['BITCOIN_ZPUB']

    url = "https://www.blockonomics.co/api/balance"

    # Define the request headers including your API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Create the request body
    body = {"addr": zpub}

    # Make the POST request
    response = requests.post(url, headers=headers, json=body)

    confirmed_balance = 0
    # Check if the request was successful (status code 200)
    if str(response.status_code).startswith('2'):
        while response.status_code == 202:
            print("Waiting on Blockonomics API...")
            time.sleep(5)
            response = requests.post(url, headers=headers, json=body)
        # Parse the JSON response
        data = response.json()
        # Access the balance data
        for entry in data["response"]:
            confirmed_balance += entry["confirmed"]
    else:
        raise ValueError("Error:", response.status_code)

    print(confirmed_balance)
    
    return confirmed_balance


assets = [ledger_satoshis]
