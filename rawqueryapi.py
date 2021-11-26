import requests
import os
bear_token = os.environ['bearer_token']

url = "https://api.twitter.com/1.1/search/tweets.json??max_id=1442855446860140549&q=snow&count=50&include_entities=1"

payload={}
headers = {
  'authorization': f'Bearer {bear_token}'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.status_code)
print(response.text)