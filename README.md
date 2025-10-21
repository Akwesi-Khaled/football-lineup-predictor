
# Football Lineup Predictor (API-Football pipeline)

This project is a modular Streamlit app that fetches live fixtures, lineups, and player stats from **API-Football**,
builds lineup-aware features, trains simple models (Poisson + XGBoost), and predicts match outcomes using the starting XI.

## How it works (high level)
- `src/data_loader.py` connects to API-Football to fetch fixtures, historical matches, lineups, and player stats.
- `src/features.py` computes rolling team stats, H2H aggregations, and lineup aggregates.
- `src/model.py` contains training helpers for Poisson and XGBoost models.
- `src/predict.py` runs inference and returns probabilities and expected scores.
- `app.py` is the Streamlit UI that ties everything together.

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Provide API key:
   - Locally: create `.env` with `API_FOOTBALL_KEY=your_key`
   - Streamlit Cloud: set secret `API_FOOTBALL_KEY`
3. Run: `streamlit run app.py`

The app has synthetic fallback data so you can test without an API key (feature-limited).
