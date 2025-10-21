import requests
from src.config import BASE_URL, HEADERS

test_url = f"{BASE_URL}/status"
r = requests.get(test_url, headers=HEADERS)
print(r.json())
