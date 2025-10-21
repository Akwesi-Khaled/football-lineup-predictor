import os
import requests
from src.config import API_FOOTBALL_KEY, BASE_URL

def get_fixtures(league_id, season=2024):
    headers = {
        "x-apisports-key": API_FOOTBALL_KEY
    }
    url = f"{BASE_URL}/fixtures"
    params = {"league": league_id, "season": season, "next": 10}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data
