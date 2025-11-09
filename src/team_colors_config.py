"""
IPL Team Colors Configuration
Professional color palette for consistent visualization across the project
"""

TEAM_COLORS = {
    # Active Teams
    'Mumbai Indians': '#004BA0',           # Blue
    'Chennai Super Kings': '#FFFF3C',      # Yellow
    'Royal Challengers Bengaluru': '#EC1C24',  # Red
    'Kolkata Knight Riders': '#3A225D',    # Purple
    'Delhi Capitals': '#282968',           # Navy Blue
    'Punjab Kings': '#ED1B24',             # Red
    'Rajasthan Royals': '#254AA5',         # Royal Blue
    'Sunrisers Hyderabad': '#FF822A',      # Orange
    'Gujarat Titans': '#1C2C3E',           # Dark Blue/Grey
    'Lucknow Super Giants': '#4ED973',     # Cyan/Turquoise
    
    # Defunct Teams
    'Deccan Chargers': '#0066B3',          # Blue
    'Pune Warriors': '#2F9BE3',            # Light Blue
    'Gujarat Lions': '#FF6600',            # Orange
    'Kochi Tuskers Kerala': '#9354A5',     # Purple
    'Rising Pune Supergiants': '#D11D9B',  # Pink/Magenta
    
    # Default for Unknown
    'Unknown': '#808080',                  # Grey
    'Not Awarded': '#808080'               # Grey
}

# Team abbreviations for compact displays
TEAM_ABBREVIATIONS = {
    'Mumbai Indians': 'MI',
    'Chennai Super Kings': 'CSK',
    'Royal Challengers Bengaluru': 'RCB',
    'Kolkata Knight Riders': 'KKR',
    'Delhi Capitals': 'DC',
    'Punjab Kings': 'PBKS',
    'Rajasthan Royals': 'RR',
    'Sunrisers Hyderabad': 'SRH',
    'Gujarat Titans': 'GT',
    'Lucknow Super Giants': 'LSG',
    'Deccan Chargers': 'DC',
    'Pune Warriors': 'PW',
    'Gujarat Lions': 'GL',
    'Kochi Tuskers Kerala': 'KTK',
    'Rising Pune Supergiants': 'RPS',
    'Unknown': 'UNK'
}

def get_team_color(team_name):
    """
    Get color for a team name
    
    Parameters:
    -----------
    team_name : str
        Name of the team
        
    Returns:
    --------
    str : Hex color code
    """
    return TEAM_COLORS.get(team_name, '#808080')

def get_team_abbr(team_name):
    """
    Get abbreviation for a team name
    
    Parameters:
    -----------
    team_name : str
        Name of the team
        
    Returns:
    --------
    str : Team abbreviation
    """
    return TEAM_ABBREVIATIONS.get(team_name, team_name[:3].upper())