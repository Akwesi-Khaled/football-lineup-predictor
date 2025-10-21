import os

# ============================================================
# API CONFIGURATION
# ============================================================

# Securely load your API key (from Streamlit Secrets or .env)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Base URL for API-Football (official direct endpoint)
BASE_URL = "https://v3.football.api-sports.io"

# Host (used in headers, especially with RapidAPI)
API_FOOTBALL_HOST = "v3.football.api-sports.io"

# Number of upcoming fixtures to fetch per league
NEXT_FIXTURES = 20  # You can change to 5, 15, 20 etc.

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

# For backward compatibility with modules using LEAGUES
LEAGUES = TOP_LEAGUES

# ============================================================
# APP SETTINGS
# ============================================================

# Default season to pull data for
DEFAULT_SEASON = 2024

# Whether to use cached or live API mode
USE_LIVE_API = True
