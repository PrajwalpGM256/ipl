import pandas as pd
import numpy as np

def get_h2h_record(team1, team2, matches_df):
    """
    Get head-to-head record between two teams
    
    Parameters:
    -----------
    team1, team2: str - Team names
    matches_df: DataFrame - Matches data
    
    Returns:
    --------
    dict: Head-to-head statistics
    """
    # Find all matches between these two teams
    h2h_matches = matches_df[
        ((matches_df['team1'] == team1) & (matches_df['team2'] == team2)) |
        ((matches_df['team1'] == team2) & (matches_df['team2'] == team1))
    ]
    
    if len(h2h_matches) == 0:
        return None
    
    # Count wins for each team
    team1_wins = len(h2h_matches[h2h_matches['winner'] == team1])
    team2_wins = len(h2h_matches[h2h_matches['winner'] == team2])
    no_result = len(h2h_matches[h2h_matches['winner'].isna()])
    
    # Calculate percentages
    total_decided = team1_wins + team2_wins
    team1_win_pct = (team1_wins / total_decided * 100) if total_decided > 0 else 0
    team2_win_pct = (team2_wins / total_decided * 100) if total_decided > 0 else 0
    
    return {
        'total_matches': len(h2h_matches),
        f'{team1}_wins': team1_wins,
        f'{team2}_wins': team2_wins,
        'no_result': no_result,
        f'{team1}_win_pct': team1_win_pct,
        f'{team2}_win_pct': team2_win_pct,
        'matches': h2h_matches  # Return actual matches for deeper analysis
    }

def get_all_h2h_matrix(matches_df):
    """
    Create a matrix of head-to-head records for all teams
    """
    teams = sorted(list(set(matches_df['team1'].unique()) | set(matches_df['team2'].unique())))
    
    # Create empty matrix
    h2h_matrix = pd.DataFrame(index=teams, columns=teams)
    
    for team1 in teams:
        for team2 in teams:
            if team1 == team2:
                h2h_matrix.loc[team1, team2] = "-"
            else:
                record = get_h2h_record(team1, team2, matches_df)
                if record:
                    h2h_matrix.loc[team1, team2] = f"{record[f'{team1}_wins']}-{record[f'{team2}_wins']}"
                else:
                    h2h_matrix.loc[team1, team2] = "0-0"
    
    return h2h_matrix