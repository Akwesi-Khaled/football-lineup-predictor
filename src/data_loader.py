
import requests
import pandas as pd
import streamlit as st
from .config import API_FOOTBALL_KEY, API_FOOTBALL_HOST, NEXT_FIXTURES, HIST_SEASON

headers = {
    "x-apisports-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": API_FOOTBALL_HOST
}
 if API_FOOTBALL_KEY else {}

def _safe_get(url, params=None, timeout=15):
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"API request failed: {e}")
        return None

@st.cache_data(ttl=600)
def fetch_fixtures(league_id, season=None, next_n=NEXT_FIXTURES):
    season = season or HIST_SEASON
    if not API_FOOTBALL_KEY:
        st.info('No API key provided: returning synthetic fixtures for demo.')
        df = pd.DataFrame([{
            'fixture.id': 1,
            'fixture.date': '2024-10-25 15:00:00',
            'teams.home.name': 'Team A',
            'teams.away.name': 'Team B',
            'league.name': 'Demo League'
        }, {
            'fixture.id': 2,
            'fixture.date': '2024-10-26 17:30:00',
            'teams.home.name': 'Team C',
            'teams.away.name': 'Team D',
            'league.name': 'Demo League'
        }])
        return df
    url = f'https://{API_FOOTBALL_HOST}/fixtures'
    params = {'league': league_id, 'season': season, 'next': next_n}
    data = _safe_get(url, params=params)
    if not data or 'response' not in data:
        return pd.DataFrame()
    df = pd.json_normalize(data['response'])
    return df

@st.cache_data(ttl=86400)
def fetch_historical_matches(league_id, season=HIST_SEASON):
    if not API_FOOTBALL_KEY:
        df = pd.DataFrame([{
            'fixture.date': '2024-09-01',
            'teams.home.name': 'Team A',
            'teams.away.name': 'Team B',
            'goals.home': 2,
            'goals.away': 1
        }, {
            'fixture.date': '2024-09-08',
            'teams.home.name': 'Team B',
            'teams.away.name': 'Team A',
            'goals.home': 0,
            'goals.away': 0
        }])
        return df

    url = f'https://{API_FOOTBALL_HOST}/fixtures'
    params = {'league': league_id, 'season': season, 'status': 'FT', 'limit': 1000}
    data = _safe_get(url, params=params)
    if not data or 'response' not in data:
        return pd.DataFrame()
    df = pd.json_normalize(data['response'])
    return df

@st.cache_data(ttl=3600)
def fetch_lineup(fixture_id):
    if not API_FOOTBALL_KEY:
        return None
    url = f'https://{API_FOOTBALL_HOST}/fixtures/lineups'
    params = {'fixture': fixture_id}
    data = _safe_get(url, params=params)
    if not data or 'response' not in data or len(data['response'])==0:
        return None
    return data['response']

@st.cache_data(ttl=3600)
def fetch_player_stats(player_id, season=HIST_SEASON):
    if not API_FOOTBALL_KEY:
        return None
    url = f'https://{API_FOOTBALL_HOST}/players'
    params = {'id': player_id, 'season': season}
    data = _safe_get(url, params=params)
    return data.get('response', None) if data else None
