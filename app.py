
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from src.config import TOP_LEAGUES
from src.data_loader import fetch_fixtures, fetch_historical_matches, fetch_lineup, fetch_player_stats
from src.features import build_team_long_form, rolling_stats, lineup_aggregate_from_api
from src.model import train_poisson_team_models, train_xgb_outcome
from src.predict import poisson_score_probs, xgb_predict_proba
from src.utils import show_fixture_table, show_prob_metrics

st.set_page_config(page_title='Lineup-based Football Predictor', layout='wide')
st.title('Football Lineup Predictor (API-Football)')

league_choice = st.sidebar.selectbox('Choose league', list(TOP_LEAGUES.keys()))
league_id = TOP_LEAGUES[league_choice]

st.sidebar.markdown('**API key**: Provide API_FOOTBALL_KEY as env var or Streamlit secret.')
if not os.getenv('API_FOOTBALL_KEY'):
    st.sidebar.warning('No API key found. App will use synthetic fallback data for demo.')

with st.spinner('Fetching fixtures...'):
    fixtures = fetch_fixtures(league_id)

show_fixture_table(fixtures)

if fixtures is None or fixtures.empty:
    st.stop()

row_index = st.number_input('Fixture row index to analyze', min_value=0, max_value=max(0, len(fixtures)-1), value=0)
row = fixtures.iloc[int(row_index)]
fixture_id = row.get('fixture.id') if 'fixture.id' in row else None
home_name = row.get('teams.home.name') or 'Home'
away_name = row.get('teams.away.name') or 'Away'
st.header(f"{home_name} vs {away_name}")

with st.spinner('Fetching historical matches...'):
    hist = fetch_historical_matches(league_id)

long = build_team_long_form(hist)
rolling = rolling_stats(long)

# get lineup if available
lineups = fetch_lineup(fixture_id) if fixture_id else None
home_lineup = None; away_lineup = None
if lineups:
    try:
        entry = lineups[0] if isinstance(lineups, list) and len(lineups)>0 else lineups
        if isinstance(entry, dict) and 'lineups' in entry:
            l = entry['lineups']
            if len(l)>=2:
                home_lineup = l[0].get('startXI', [])
                away_lineup = l[1].get('startXI', [])
    except Exception as e:
        st.warning('Lineup parse error: ' + str(e))

st.subheader('Starting XI (fetched or editable)')
if home_lineup:
    st.write('Home lineup fetched, first 5 players:')
    st.write(home_lineup[:5])
else:
    st.info('No home lineup available (you can enter manually in future).')

player_stats_lookup = {}
for p in (home_lineup or []) + (away_lineup or []):
    pid = None
    try:
        player = p.get('player') if isinstance(p, dict) else p
        pid = player.get('id') if isinstance(player, dict) else None
    except Exception:
        pid = None
    if pid:
        player_stats_lookup[pid] = fetch_player_stats(pid) or {}

lineup_feats = lineup_aggregate_from_api(home_lineup, away_lineup, player_stats_lookup)
st.write('Lineup aggregate features:', lineup_feats)

st.markdown('---')
st.subheader('Train simple models (demo)')
if st.button('Train models (Poisson + XGB)'):
    matches_df = hist.rename(columns={
        'teams.home.name': 'home_team',
        'teams.away.name': 'away_team',
        'goals.home': 'HomeGoals',
        'goals.away': 'AwayGoals'
    }).copy()
    matches_df['rating_diff'] = 0
    matches_df['goals5_diff'] = 0
    try:
        home_model, away_model = train_poisson_team_models(matches_df, predictor_cols=['rating_diff','goals5_diff'])
        st.success('Poisson models trained (in-memory).')
    except Exception as e:
        st.error('Poisson training failed: ' + str(e))
    try:
        matches_df['outcome'] = matches_df.apply(lambda r: 1 if r['HomeGoals']>r['AwayGoals'] else (2 if r['HomeGoals']<r['AwayGoals'] else 0), axis=1)
        xgb_model = train_xgb_outcome(matches_df[['rating_diff','goals5_diff','outcome']])
        st.success('XGB outcome model trained (in-memory).')
    except Exception as e:
        st.error('XGB training failed: ' + str(e))

st.subheader('Predict using current lineup features')
if st.button('Predict now'):
    try:
        input_features = {'rating_diff': lineup_feats.get('rating_diff',0), 'goals5_diff': lineup_feats.get('goals5_diff',0)}
        p = poisson_score_probs(home_model, away_model, input_features)
        show_prob_metrics(p)
    except Exception as e:
        st.error('Prediction failed: ' + str(e))
