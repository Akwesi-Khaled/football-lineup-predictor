import os

# Load your API key from environment (Streamlit Secrets or .env)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Base URL for API-Football
BASE_URL = "https://v3.football.api-sports.io"

# League IDs (from API-Football)
LEAGUES = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue 1": 61,
}


HIST_SEASON = 2023
NEXT_FIXTURES = 50
