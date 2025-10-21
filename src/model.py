
import joblib
import xgboost as xgb
import pandas as pd
import statsmodels.api as sm
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

def train_xgb_outcome(features_df, target_col='outcome'):
    X = features_df.drop(columns=[target_col]).astype(float)
    y = features_df[target_col].astype(int)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = xgb.XGBClassifier(n_estimators=200, learning_rate=0.05, use_label_encoder=False, eval_metric='mlogloss')
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    calib = CalibratedClassifierCV(model, cv='prefit', method='isotonic')
    calib.fit(X_val, y_val)
    return calib

def train_poisson_team_models(matches_df, predictor_cols=None):
    df = matches_df.copy().dropna(subset=['HomeGoals', 'AwayGoals'])
    predictor_cols = predictor_cols or [c for c in df.columns if c not in ['home_team','away_team','HomeGoals','AwayGoals']]
    X = df[predictor_cols].astype(float)
    Xc = sm.add_constant(X, has_constant='add').fillna(0)
    y_home = df['HomeGoals'].astype(float)
    y_away = df['AwayGoals'].astype(float)
    home_model = sm.GLM(y_home, Xc, family=sm.families.Poisson()).fit()
    away_model = sm.GLM(y_away, Xc, family=sm.families.Poisson()).fit()
    return home_model, away_model
