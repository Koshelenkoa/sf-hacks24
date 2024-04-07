import requests
import json
import aiohttp
import urllib

WEB_ADDRESS = '127.0.0.1' #local testing
WEB_PORT = 80

async def write_to_db(sender, recipient, amount, data, index):

    url = f"http://{WEB_ADDRESS}/{WEB_PORT}/record" 
    json_obj = json.dumps({'sender':sender, 'recipient':recipient, 'amount': amount, 'data': data, 'index': index})

    async with aiohttp.ClientSession() as session:
        async with session.postt(url, json_obj) as response:
            if response.status == 200:
                print(await response.text())  # Use await to get the response text
                return 0
            else:
                print("Error:", response.status)
                return -1


async def read_form_db(**kwargs):

    sender = kwargs.get('sender')
    recipient = kwargs.get('recipient')
    amount = kwargs.get('amount')
    data = kwargs.get('data')

    query_params = urllib.parse.urlencode({key: value for key, value in kwargs.items() if value is not None})
    # Example URL construction
    url = f"http://{WEB_ADDRESS}:{WEB_PORT}/record?{query_params}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status_code == 200:
                index = response.json()['index']
                return index
            elif response.status_code == 404:
                print('no such record')
                return -1
            else:
                print("Error:", response.status_code)
                return -1