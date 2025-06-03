from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

app = Flask(__name__)

# Load saved models and encoders
try:
    clf = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/winner_model.joblib')
    reg_first = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/first_score_model.joblib')
    reg_second = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/second_score_model.joblib')
    team_encoder = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/team_encoder.joblib')
    venue_encoder = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/venue_encoder.joblib')
    team_stats = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/team_stats.joblib')
    venue_stats = joblib.load('/workspaces/codespaces-blank/IPL_2025_Predictions/venue_stats.joblib')
    print("Models and encoders loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    raise

# Prediction function
def predict_match(team1, team2, venue, match_date):
    """Predict match outcome based on teams, venue, and date."""
    try:
        match_date = pd.to_datetime(match_date)
        batting_first, batting_second = team1, team2
        
        # Validate inputs
        if team1 not in team_encoder.classes_ or team2 not in team_encoder.classes_:
            raise ValueError(f"Invalid team: {team1} or {team2}")
        if venue not in venue_encoder.classes_:
            raise ValueError(f"Invalid venue: {venue}")
        
        # Prepare features
        bf_encoded = team_encoder.transform([batting_first])[0]
        bs_encoded = team_encoder.transform([batting_second])[0]
        v_encoded = venue_encoder.transform([venue])[0]
        bf_wr = team_stats[batting_first]['wins'] / team_stats[batting_first]['matches'] if team_stats[batting_first]['matches'] > 0 else 0.5
        bs_wr = team_stats[batting_second]['wins'] / team_stats[batting_second]['matches'] if team_stats[batting_second]['matches'] > 0 else 0.5
        bf_as = team_stats[batting_first]['runs_scored'] / team_stats[batting_first]['matches'] if team_stats[batting_first]['matches'] > 0 else 150
        bs_as = team_stats[batting_second]['runs_scored'] / team_stats[batting_second]['matches'] if team_stats[batting_second]['matches'] > 0 else 150
        bf_rc = team_stats[batting_first]['runs_conceded'] / team_stats[batting_first]['matches'] if team_stats[batting_first]['matches'] > 0 else 150
        bs_rc = team_stats[batting_second]['runs_conceded'] / team_stats[batting_second]['matches'] if team_stats[batting_second]['matches'] > 0 else 150
        bf_rf = sum(team_stats[batting_first]['recent_wins']) / 5 if len(team_stats[batting_first]['recent_wins']) >= 5 else 0.5
        bs_rf = sum(team_stats[batting_second]['recent_wins']) / 5 if len(team_stats[batting_second]['recent_wins']) >= 5 else 0.5
        bf_vs_bs_wr = team_stats[batting_first]['vs_opponent_wins'][batting_second] / team_stats[batting_first]['vs_opponent_matches'][batting_second] if team_stats[batting_first]['vs_opponent_matches'][batting_second] > 0 else 0.5
        bf_vs_bs_as = sum(team_stats[batting_first]['vs_opponent_scores'][batting_second]) / len(team_stats[batting_first]['vs_opponent_scores'][batting_second]) if team_stats[batting_first]['vs_opponent_scores'][batting_second] else 150
        bf_vwr = team_stats[batting_first]['venue_wins'][venue] / team_stats[batting_first]['venue_matches'][venue] if team_stats[batting_first]['venue_matches'][venue] > 0 else 0.5
        bs_vwr = team_stats[batting_second]['venue_wins'][venue] / team_stats[batting_second]['venue_matches'][venue] if team_stats[batting_second]['venue_matches'][venue] > 0 else 0.5
        bf_rs = sum(team_stats[batting_first]['recent_scores']) / 5 if len(team_stats[batting_first]['recent_scores']) >= 5 else 150
        bs_rs = sum(team_stats[batting_second]['recent_scores']) / 5 if len(team_stats[batting_second]['recent_scores']) >= 5 else 150
        v_fa = venue_stats[venue]['first_innings_avg'] / venue_stats[venue]['matches'] if venue_stats[venue]['matches'] > 0 else 150
        v_sa = venue_stats[venue]['second_innings_avg'] / venue_stats[venue]['matches'] if venue_stats[venue]['matches'] > 0 else 140
        v_tbw = venue_stats[venue]['toss_bat_win_rate'] / venue_stats[venue]['matches'] if venue_stats[venue]['matches'] > 0 else 0.5
        ti = 0.5  # Neutral toss impact
        
        features = np.array([[bf_encoded, bs_encoded, v_encoded, bf_wr, bs_wr, bf_as, bs_as, bf_rc, bs_rc, 
                             bf_rf, bs_rf, bf_vs_bs_wr, bf_vs_bs_as, bf_vwr, bs_vwr, bf_rs, bs_rs, 
                             v_fa, v_sa, v_tbw, ti]])
        
        # Predict and convert NumPy types to Python types
        winner_prob = float(clf.predict_proba(features)[0][1])  # Probability batting_first wins
        first_score = float(max(50, min(300, reg_first.predict(features)[0])))
        second_score = float(max(50, min(300, reg_second.predict(features)[0])))
        
        # Determine winner based on scores
        if first_score > second_score:
            winner = batting_first
            winner_prob_display = winner_prob  # Probability for batting_first
        else:
            winner = batting_second
            winner_prob_display = 1.0 - winner_prob  # Probability for batting_second
        
        # Run rates
        first_run_rate = float(first_score / 20)
        second_run_rate = float(second_score / 20)
        
        # Head-to-head stats
        h2h_matches = team_stats[batting_first]['vs_opponent_matches'][batting_second]
        h2h_wins = team_stats[batting_first]['vs_opponent_wins'][batting_second]
        h2h_win_rate = float(h2h_wins / h2h_matches if h2h_matches > 0 else 0.5)
        h2h_avg_score = float(sum(team_stats[batting_first]['vs_opponent_scores'][batting_second]) / len(team_stats[batting_first]['vs_opponent_scores'][batting_second]) if team_stats[batting_first]['vs_opponent_scores'][batting_second] else 150)
        
        return {
            'batting_first': batting_first,
            'batting_second': batting_second,
            'venue': venue,
            'date': match_date.strftime('%Y-%m-%d'),
            'first_innings_score': round(first_score, 2),
            'second_innings_score': round(second_score, 2),
            'first_innings_run_rate': round(first_run_rate, 2),
            'second_innings_run_rate': round(second_run_rate, 2),
            'winner': winner,
            'winner_probability': round(winner_prob_display, 2),
            'head_to_head': {
                'matches': int(h2h_matches),
                'team1_wins': int(h2h_wins),
                'team1_win_rate': round(h2h_win_rate, 2),
                'team1_avg_score_vs_team2': round(h2h_avg_score, 2)
            },
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/')
def index():
    """Render the main page."""
    teams = team_encoder.classes_.tolist()
    venues = venue_encoder.classes_.tolist()
    return render_template('index.html', teams=teams, venues=venues)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict match outcome."""
    data = request.form
    team1 = data['team1']
    team2 = data['team2']
    venue = data['venue']
    match_date = data['date']
    
    result = predict_match(team1, team2, venue, match_date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)