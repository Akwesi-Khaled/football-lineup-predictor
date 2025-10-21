import os
import datetime

# ============================================================
# ⚙️ API CONFIGURATION
# ============================================================

# Securely load your API key (from Streamlit Secrets or .env)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Base URL for API-Football (official direct endpoint)
BASE_URL = "https://v3.football.api-sports.io"

# Host (used in headers, especially with RapidAPI)
API_FOOTBALL_HOST = "v3.football.api-sports.io"

# ============================================================
# 🏆 LEAGUE INFORMATION
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

# ============================================================
# 📅 SEASON SETTINGS
# ============================================================

CURRENT_SEASON = datetime.datetime.now().year
HIST_SEASON = CURRENT_SEASON - 1
DEFAULT_SEASON = CURRENT_SEASON
NEXT_FIXTURES = 10  # Number of upcoming fixtures per league

# ============================================================
# ⚡ APP SETTINGS
# ============================================================

USE_LIVE_API = True
REFRESH_INTERVAL = 300  # 5 minutes
DEBUG_MODE = True

# ============================================================
# 🔐 HEADERS FOR API REQUESTS
# ============================================================

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": API_FOOTBALL_HOST,
}
