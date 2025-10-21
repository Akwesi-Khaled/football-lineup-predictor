import os

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

# Current season (for live data)
CURRENT_SEASON = 2024

# Historical season (used for training / model building)
HIST_SEASON = 2023

# Default season fallback
DEFAULT_SEASON = CURRENT_SEASON

# Number of upcoming fixtures to fetch per league
NEXT_FIXTURES = 10  # Adjust to your liking

# ============================================================
# ⚡ APP SETTINGS
# ============================================================

# Whether to use live API data (True) or cached local data (False)
USE_LIVE_API = True

# Refresh interval for auto-updating live matches (in seconds)
REFRESH_INTERVAL = 300  # 5 minutes

# Enable debug logging
DEBUG_MODE = True
