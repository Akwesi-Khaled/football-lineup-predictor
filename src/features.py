
import pandas as pd

def build_team_long_form(matches_df):
    df = matches_df.copy()
    df = df.rename(columns={
        'fixture.date': 'date',
        'teams.home.name': 'home_team',
        'teams.away.name': 'away_team',
        'goals.home': 'home_goals',
        'goals.away': 'away_goals'
    })
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    home = df[['date', 'home_team', 'home_goals', 'away_goals']].copy()
    home.columns = ['date', 'team', 'team_goals', 'opp_goals']
    home['is_home'] = 1
    away = df[['date', 'away_team', 'away_goals', 'home_goals']].copy()
    away.columns = ['date', 'team', 'team_goals', 'opp_goals']
    away['is_home'] = 0
    long = pd.concat([home, away], ignore_index=True).sort_values('date')
    long['team_goals'] = pd.to_numeric(long['team_goals'], errors='coerce').fillna(0)
    long['opp_goals'] = pd.to_numeric(long['opp_goals'], errors='coerce').fillna(0)
    return long

def rolling_stats(long_df, window=5):
    features = []
    for team, g in long_df.groupby('team'):
        g = g.reset_index(drop=True)
        g['rolling_goals_for_5'] = g['team_goals'].rolling(window, min_periods=1).mean()
        g['rolling_goals_against_5'] = g['opp_goals'].rolling(window, min_periods=1).mean()
        g['rolling_winrate_5'] = (g['team_goals'] > g['opp_goals']).rolling(window, min_periods=1).mean()
        g['team'] = team
        features.append(g)
    return pd.concat(features, ignore_index=True)

def lineup_aggregate_from_api(lineup_home, lineup_away, player_stats_lookup):
    def agg_players(lineup):
        rows = []
        for p in lineup:
            player = p.get('player') or p.get('player_name') or p
            pid = player.get('id') if isinstance(player, dict) and 'id' in player else player.get('player_id', None)
            stats = player_stats_lookup.get(pid, {})
            rows.append({
                'player_id': pid,
                'rating': float(stats.get('rating', 6.5) or 6.5),
                'goals_5': int(stats.get('goals_last_5', 0) or 0),
                'assists_5': int(stats.get('assists_last_5', 0) or 0),
                'minutes_5': int(stats.get('minutes_last_5', 0) or 0)
            })
        if not rows:
            return {'avg_rating':6.5, 'sum_goals_5':0, 'sum_assists_5':0, 'avg_minutes':0}
        df = pd.DataFrame(rows)
        return {'avg_rating': df['rating'].mean(), 'sum_goals_5': df['goals_5'].sum(), 'sum_assists_5': df['assists_5'].sum(), 'avg_minutes': df['minutes_5'].mean()}
    h = agg_players(lineup_home or [])
    a = agg_players(lineup_away or [])
    feats = {
        'home_avg_rating': h['avg_rating'],
        'away_avg_rating': a['avg_rating'],
        'home_sum_goals5': h['sum_goals_5'],
        'away_sum_goals5': a['sum_goals_5'],
        'rating_diff': h['avg_rating'] - a['avg_rating'],
        'goals5_diff': h['sum_goals_5'] - a['sum_goals_5']
    }
    return feats
