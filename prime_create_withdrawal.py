"""
Copyright 2022 Coinbase Global, Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json, hmac, hashlib, time, requests, base64, uuid, os
from urllib.parse import urlparse

####credentials
api_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SIGNING_KEY")
passphrase = os.environ.get("PASSPHRASE")
portfolio_id = os.environ.get("PORTFOLIO_ID")

####required variables
timestamp = str(int(time.time()))
idempotency_key = uuid.uuid4()
method = 'POST'

#user inputs
destination_type = 'DESTINATION_BLOCKCHAIN'
origin_wallet_id = os.environ.get('WALLET_ID')
amount = '0.01'
currency_symbol = 'eth'
destination_wallet_address = os.environ.get('BLOCKCHAIN_ADDRESS')
account_identifier = ''

url = 'https://api.prime.coinbase.com/v1/portfolios/'+portfolio_id+'/wallets/'+origin_wallet_id+'/withdrawals'
payload = {
    'portfolio_id': portfolio_id,
    'wallet_id': origin_wallet_id,
    'amount': amount,
    'destination_type': destination_type,
    'idempotency_key': str(idempotency_key),
    'currency_symbol': currency_symbol,
    'blockchain_address': {
        'address': '0xb9c9c43cb866a09e51aeb706007e43a45f4fbe44',
        'account_identifier': account_identifier
    }
}

####signature and request
url_path = urlparse(url).path
message = timestamp + method + url_path + json.dumps(payload)
signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
signature_b64 = base64.b64encode(signature).decode()

headers = {
   'X-CB-ACCESS-SIGNATURE': signature_b64,
   'X-CB-ACCESS-TIMESTAMP': timestamp,
   'X-CB-ACCESS-KEY': api_key,
   'X-CB-ACCESS-PASSPHRASE': passphrase,
   'Accept': 'application/json'
}
response = requests.post(url, json=payload, headers=headers)
parse = json.loads(response.text)
print(response.status_code)
print(json.dumps(parse, indent=3))