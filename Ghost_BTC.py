import requests
import time
import sys
from colorama import init, Fore, Back, Style

init(autoreset=True)

ascii_art = f"""
{Fore.YELLOW}{Style.BRIGHT}
 ____ _____ ____    ____ _   _ _____ ____ _  _______ ____  
| __ )_   _/ ___|  / ___| | | | ____/ ___| |/ / ____|  _ \ 
|  _ \ | || |     | |   | |_| |  _|| |   | ' /|  _| | |_) |
| |_) || || |___  | |___|  _  | |__| |___| . \| |___|  _ < 
|____/ |_| \____|  \____|_| |_|_____\____|_|\_\_____|_| \_\

{Fore.CYAN}{Style.BRIGHT}Author: {Fore.GREEN}{Style.BRIGHT}Ghost sec [HELL YEAH 🔥🔥🔥]
"""

print(ascii_art)

ss = input(f'{Fore.MAGENTA}{Style.BRIGHT}Hey, give me the file name that contains the Bitcoin addresses: {Fore.YELLOW}{Style.BRIGHT}')
bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'

try:
    response = requests.get(bitcoin_api_url).json()
    bitcoin_price_usd = float(response['bpi']['USD']['rate_float'])
    print(f"{Fore.GREEN}{Style.BRIGHT}Bitcoin is flying high today! Current price: ${bitcoin_price_usd:.2f} USD")
except requests.exceptions.RequestException as e:
    print(f"{Fore.RED}{Style.BRIGHT}Oops! Something went wrong when fetching Bitcoin price. Error: {e}")
    sys.exit(1)

# Read the Bitcoin addresses from the file
try:
    with open(ss, 'r') as file:
        bitcoin_addresses = file.read().splitlines()
except FileNotFoundError:
    print(f"{Fore.RED}{Style.BRIGHT}Whoops, file {ss} not found. Check your file name, my friend.")
    sys.exit(1)

results = {}

for address in bitcoin_addresses:
    try:
        response = requests.get(f"https://api.blockchair.com/bitcoin/dashboards/address/{address}")
        
        if response.status_code != 200:
            print(f"{Fore.RED}{Style.BRIGHT}Oops! Failed to fetch data for address {address}. Status code: {response.status_code}. There's nothing here! skip buddy")
            continue

        data = response.json()
        
        if data and isinstance(data, dict) and 'data' in data:
            if address in data['data']:
                balance_satoshi = data['data'][address]['address']['balance']
                balance_btc = balance_satoshi / 100000000
                balance_usd = balance_btc * bitcoin_price_usd
                
                results[address] = {
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd
                }

                print(f"{Fore.GREEN}{Style.BRIGHT}🎉 Address: {Fore.CYAN}{Style.BRIGHT}{address} {Fore.GREEN}{Style.BRIGHT}| Balance: {Fore.YELLOW}{Style.BRIGHT}{balance_btc} BTC {Fore.GREEN}{Style.BRIGHT}| ${balance_usd:.2f} USD 🎉")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Hey, address {address} has no balance or wasn't found. Try again later.")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Oops! Data is either invalid or address {address} doesn’t exist. That's weird!")
    
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{Style.BRIGHT}Yikes! Something went wrong while fetching balance for {address}. Error: {e}")
    
    time.sleep(2)

with open('bitcoin_balances.txt', 'w') as file:
    for address, balances in results.items():
        file.write(f"{address}: {balances['balance_btc']} BTC, ${balances['balance_usd']:.2f}\n")

print(f"{Fore.GREEN}{Style.BRIGHT}All done! 🎉 Results have been saved to 'bitcoin_balances.txt'. Go check it out!")
