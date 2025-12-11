# src/feature_engineering.py
"""
Feature Engineering Helper Functions for IPL Analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_team_form(matches_df, team, date, n_matches=5):
    """
    Calculate recent form of a team (last n matches win rate)
    """
    team_matches = matches_df[
        ((matches_df['team1'] == team) | (matches_df['team2'] == team)) &
        (matches_df['date'] < date)
    ].tail(n_matches)
    
    if len(team_matches) == 0:
        return 0.5  # Default for new teams
    
    wins = len(team_matches[team_matches['winner'] == team])
    return wins / len(team_matches)

def get_h2h_stats(matches_df, team1, team2, date):
    """
    Get head-to-head statistics between two teams before a given date
    """
    h2h = matches_df[
        (((matches_df['team1'] == team1) & (matches_df['team2'] == team2)) |
         ((matches_df['team1'] == team2) & (matches_df['team2'] == team1))) &
        (matches_df['date'] < date)
    ]
    
    if len(h2h) == 0:
        return {'h2h_matches': 0, 'team1_h2h_win_rate': 0.5}
    
    team1_wins = len(h2h[h2h['winner'] == team1])
    return {
        'h2h_matches': len(h2h),
        'team1_h2h_win_rate': team1_wins / len(h2h)
    }

def calculate_venue_stats(matches_df, team, venue, date):
    """
    Calculate team's historical performance at a specific venue
    """
    venue_matches = matches_df[
        ((matches_df['team1'] == team) | (matches_df['team2'] == team)) &
        (matches_df['venue'] == venue) &
        (matches_df['date'] < date)
    ]
    
    if len(venue_matches) == 0:
        return {'venue_matches': 0, 'venue_win_rate': 0.5}
    
    wins = len(venue_matches[venue_matches['winner'] == team])
    return {
        'venue_matches': len(venue_matches),
        'venue_win_rate': wins / len(venue_matches)
    }

def calculate_toss_impact(matches_df, team, date, n_matches=20):
    """
    Calculate toss win to match win conversion rate
    """
    recent_matches = matches_df[
        (matches_df['toss_winner'] == team) &
        (matches_df['date'] < date)
    ].tail(n_matches)
    
    if len(recent_matches) == 0:
        return 0.5
    
    wins = len(recent_matches[recent_matches['winner'] == team])
    return wins / len(recent_matches)

def get_season_stats(matches_df, team, season):
    """
    Get team's performance in the current season before the match
    """
    season_matches = matches_df[
        ((matches_df['team1'] == team) | (matches_df['team2'] == team)) &
        (matches_df['season'] == season)
    ]
    
    if len(season_matches) == 0:
        return {
            'season_matches': 0,
            'season_win_rate': 0.5,
            'season_avg_win_margin': 0
        }
    
    wins = season_matches[season_matches['winner'] == team]
    win_margins = []
    
    for _, match in wins.iterrows():
        if match['result'] == 'runs':
            win_margins.append(match['result_margin'])
        else:  # wickets
            win_margins.append(match['result_margin'] * 3)  # Approximate conversion
    
    return {
        'season_matches': len(season_matches),
        'season_win_rate': len(wins) / len(season_matches),
        'season_avg_win_margin': np.mean(win_margins) if win_margins else 0
    }

def calculate_player_impact(deliveries_df, matches_df, player_name, date, role='batsman'):
    """
    Calculate player's recent performance metrics
    """
    # Get recent matches before the date
    recent_match_ids = matches_df[matches_df['date'] < date].tail(20)['id'].values
    
    if role == 'batsman':
        player_data = deliveries_df[
            (deliveries_df['batsman'] == player_name) &
            (deliveries_df['match_id'].isin(recent_match_ids))
        ]
        
        if len(player_data) == 0:
            return {'avg_runs': 0, 'strike_rate': 100}
        
        total_runs = player_data['batsman_runs'].sum()
        balls_faced = len(player_data[player_data['extras_type'] != 'wides'])
        
        return {
            'avg_runs': total_runs / len(player_data['match_id'].unique()),
            'strike_rate': (total_runs / balls_faced * 100) if balls_faced > 0 else 100
        }
    
    else:  # bowler
        player_data = deliveries_df[
            (deliveries_df['bowler'] == player_name) &
            (deliveries_df['match_id'].isin(recent_match_ids))
        ]
        
        if len(player_data) == 0:
            return {'economy': 8, 'wickets_per_match': 0}
        
        total_runs = player_data['total_runs'].sum()
        total_balls = len(player_data[player_data['extras_type'] != 'noballs'])
        wickets = len(player_data[player_data['player_dismissed'].notna()])
        
        return {
            'economy': (total_runs / (total_balls / 6)) if total_balls > 0 else 8,
            'wickets_per_match': wickets / len(player_data['match_id'].unique())
        }

def create_match_context_features(row, matches_df):
    """
    Create contextual features for a match
    """
    features = {}
    
    # Day/Night match
    features['is_day_match'] = 1 if pd.to_datetime(row['date']).hour < 16 else 0
    
    # Playoff match
    features['is_playoff'] = 1 if 'Qualifier' in str(row.get('match_type', '')) or \
                                  'Eliminator' in str(row.get('match_type', '')) or \
                                  'Final' in str(row.get('match_type', '')) else 0
    
    # Season phase (early/mid/late)
    season_matches = matches_df[matches_df['season'] == row['season']]
    match_position = len(season_matches[season_matches['date'] <= row['date']])
    total_matches = len(season_matches)
    
    if total_matches > 0:
        position_ratio = match_position / total_matches
        if position_ratio <= 0.33:
            features['season_phase'] = 'early'
        elif position_ratio <= 0.67:
            features['season_phase'] = 'mid'
        else:
            features['season_phase'] = 'late'
    else:
        features['season_phase'] = 'mid'
    
    return features

def aggregate_bowling_innings(deliveries_df, match_id, innings):
    """
    Aggregate bowling statistics for an innings
    """
    innings_data = deliveries_df[
        (deliveries_df['match_id'] == match_id) &
        (deliveries_df['inning'] == innings)
    ]
    
    if len(innings_data) == 0:
        return {}
    
    # Powerplay (1-6 overs)
    powerplay = innings_data[innings_data['over'] <= 6]
    powerplay_runs = powerplay['total_runs'].sum()
    powerplay_wickets = powerplay['is_wicket'].sum()  # FIXED: use is_wicket
    
    # Middle overs (7-15)
    middle = innings_data[(innings_data['over'] > 6) & (innings_data['over'] <= 15)]
    middle_runs = middle['total_runs'].sum()
    middle_wickets = middle['is_wicket'].sum()  # FIXED: use is_wicket
    
    # Death overs (16-20)
    death = innings_data[innings_data['over'] > 15]
    death_runs = death['total_runs'].sum()
    death_wickets = death['is_wicket'].sum()  # FIXED: use is_wicket
    
    # Extras
    extras = innings_data['extra_runs'].sum()
    
    return {
        'powerplay_runs': powerplay_runs,
        'powerplay_wickets': int(powerplay_wickets),
        'middle_runs': middle_runs,
        'middle_wickets': int(middle_wickets),
        'death_runs': death_runs,
        'death_wickets': int(death_wickets),
        'total_extras': extras,
        'total_runs': innings_data['total_runs'].sum(),
        'total_wickets': int(innings_data['is_wicket'].sum())  # FIXED: use is_wicket
    }

def calculate_momentum(deliveries_df, match_id, over_number):
    """
    Calculate momentum based on recent scoring rate
    """
    match_data = deliveries_df[deliveries_df['match_id'] == match_id]
    
    if over_number <= 3:
        return 0  # No momentum in early overs
    
    recent_overs = match_data[
        (match_data['over'] > over_number - 3) & 
        (match_data['over'] <= over_number)
    ]
    previous_overs = match_data[
        (match_data['over'] > over_number - 6) & 
        (match_data['over'] <= over_number - 3)
    ]
    
    if len(recent_overs) == 0 or len(previous_overs) == 0:
        return 0
    
    recent_rate = recent_overs['total_runs'].sum() / 3
    previous_rate = previous_overs['total_runs'].sum() / 3
    
    return recent_rate - previous_rate