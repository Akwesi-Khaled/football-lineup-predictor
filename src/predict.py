
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import poisson

def poisson_score_probs(home_model, away_model, input_features, max_goals=6):
    X = pd.DataFrame([input_features]).astype(float)
    Xc = sm.add_constant(X, has_constant='add').fillna(0)
    lam_home = float(home_model.predict(Xc)[0])
    lam_away = float(away_model.predict(Xc)[0])
    probs = np.zeros((max_goals+1, max_goals+1))
    for i in range(max_goals+1):
        for j in range(max_goals+1):
            probs[i,j] = poisson.pmf(i, lam_home) * poisson.pmf(j, lam_away)
    home_win = probs[np.triu_indices_from(probs, k=1)].sum()
    draw = np.trace(probs).sum()
    away_win = probs[np.tril_indices_from(probs, k=-1)].sum()
    exp_home = sum(i * probs[i,j] for i in range(max_goals+1) for j in range(max_goals+1))
    exp_away = sum(j * probs[i,j] for i in range(max_goals+1) for j in range(max_goals+1))
    return {'lam_home': lam_home, 'lam_away': lam_away, 'p_home': home_win, 'p_draw': draw, 'p_away': away_win, 'exp_home': exp_home, 'exp_away': exp_away}

def xgb_predict_proba(xgb_model, feature_vector):
    import pandas as pd
    probs = xgb_model.predict_proba(pd.DataFrame([feature_vector]))[0]
    return {'p_draw': probs[0], 'p_home': probs[1], 'p_away': probs[2]}
