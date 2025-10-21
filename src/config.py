import os

# ============================================================
# API CONFIGURATION
# ============================================================

# Load your API key securely (from Streamlit Secrets or .env)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Base URL for API-Football (direct endpoint)
BASE_URL = "https://v3.football.api-sports.io"

# Host name for headers (for RapidAPI or compatibility)
API_FOOTBALL_HOST = "v3.football.api-sports.io"

# ============================================================
# LEAGUE INFORMATION
# ============================================================

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

# For backward compatibility
LEAGUES = TOP_LEAGUES
