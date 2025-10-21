
import os

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_HOST = os.getenv("API_FOOTBALL_HOST", "v3.football.api-sports.io")

TOP_LEAGUES = {
    "EPL": 39,
    "LaLiga": 140,
    "Bundesliga": 78,
    "SerieA": 135
}

HIST_SEASON = 2023
NEXT_FIXTURES = 50
