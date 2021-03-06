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

####By default, this code is set to market, however you can adjust order_type to LIMIT if you would like to place a limit order. There is no need to update the payload, but do note the differences.
import json, hmac, hashlib, time, requests, base64, uuid, os
from urllib.parse import urlparse

####credentials
api_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SIGNING_KEY")
passphrase = os.environ.get("PASSPHRASE")
portfolio_id = os.environ.get("PORTFOLIO_ID")

####required variables
timestamp = str(int(time.time()))
client_order_id = uuid.uuid4()
method = 'POST'

#get order preview
#url = 'https://api.prime.coinbase.com/v1/portfolios/'+portfolio_id+'/order_preview'

#create order
url = 'https://api.prime.coinbase.com/v1/portfolios/'+portfolio_id+'/order'

#user inputs
product_id = 'ETH-USD'
side = 'BUY' #or SELL
order_type = 'MARKET' #or LIMIT
limit_price = '1600'
base_quantity = '0.01'

payload = {
    'portfolio_id': portfolio_id,
    'product_id': product_id,
    'client_order_id': str(client_order_id),
    'side': side,
    'type': order_type,
    'base_quantity': base_quantity
}

if order_type == 'LIMIT':
    payload['limit_price'] = limit_price

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

if 'preview' in url:
    print(json.dumps(parse,indent=3))
else:
        parse_order = parse['order_id']
        print(parse_order)
