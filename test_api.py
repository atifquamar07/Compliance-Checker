# Example request using Python requests library
import requests

url = "http://localhost:8050/check-compliance"
data = {
    "webpage_url": "https://mercury.com",
    "policy_url": "https://stripe.com/docs/treasury/marketing-treasury"
}

response = requests.post(url, json=data)
print(response.json())