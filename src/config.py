import os

# ============================================================
# API CONFIGURATION
# ============================================================

# Load your API key securely (from Streamlit Secrets or .env)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Base URL for the API-Football endpoints
BASE_URL = "https://v3.football.api-sports.io"

# ============================================================
# LEAGUE INFORMATION
# ============================================================

# Common league IDs (from API-Football docs)
TOP_LEAGUES = {
    "Premier League (England)": 39,
    "La Liga (Spain)": 140,
    "Serie A (Italy)": 135,
    "Bundesliga (Germany)": 78,
    "Ligue 1 (France)": 61,
    "Eredivisie (Netherlands)": 88,
    "Primeira Liga (Portugal)": 94,
    "Champions League (Europe)": 2,
}

# For backward compatibility with older imports
LEAGUES = TOP_LEAGUES

