import requests

url = "https://api.twitter.com/1.1/search/tweets.json??max_id=1442855446860140549&q=snow&count=50&include_entities=1"

payload={}
headers = {
  'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAEw8UAEAAAAAZ5GWaDCwh9WZ77%2FWwtPhPiIH3xY%3Do6a3P2AJ3hhd8RdpNpT5RGJ6svyWgJyeP2j6noHmLPoaRbGXRW'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.status_code)
print(response.text)