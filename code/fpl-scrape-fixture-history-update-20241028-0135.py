import pandas as pd
import requests
import numpy as np
import datetime
from pymongo import MongoClient
import configparser

# Configure display options
pd.options.display.max_columns = None

# Get the current date and time in the desired format for file naming
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')

# Load configuration for MongoDB connection
config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('mongodb', 'username')
password = config.get('mongodb', 'password')
cluster_url = config.get('mongodb', 'cluster_url')
database = config.get('mongodb', 'database')

# Construct MongoDB URI and create client
mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster_url}?retryWrites=true&w=majority"
client = MongoClient(mongodb_uri)
db = client[database]
collection_fixture = db['fixture']
collection_details = db['details']

# Fetch general FPL data
base_url = 'https://fantasy.premierleague.com/api/'
bootstrap_url = f'{base_url}bootstrap-static/'
data = requests.get(bootstrap_url).json()

# Load key data tables from JSON response
elements_df = pd.DataFrame(data['elements'])
elements_types_df = pd.DataFrame(data['element_types'])
teams_df = pd.DataFrame(data['teams'])

# Initialize DataFrames for fixtures and history
all_fixtures_df = pd.DataFrame()
all_history_df = pd.DataFrame()

# Loop through each player to gather fixture and history data
for index, row in elements_df.iterrows():
    element_id = row['id']
    url = f'{base_url}element-summary/{element_id}/'
    element_data = requests.get(url).json()
    
    # Append player-specific data to aggregate DataFrames
    json_fixtures_df = pd.DataFrame(element_data['fixtures'])
    json_history_df = pd.DataFrame(element_data['history'])
    
    all_fixtures_df = pd.concat([all_fixtures_df, json_fixtures_df], ignore_index=True)
    all_history_df = pd.concat([all_history_df, json_history_df], ignore_index=True)
    
    all_fixtures_df.to_csv(f'all_fixtures_raw_{timestamp}.csv')
    all_history_df.to_csv(f'all_history_raw_{timestamp}.csv')
    


    print(f'Processed player index: {index}, ID: {element_id}')

# Prepare updated elements DataFrame with mapped team names
update_elements_df = elements_df[['web_name', 'team', 'element_type', 'selected_by_percent', 'now_cost', 
                                  'minutes', 'total_points', 'goals_scored', 'assists', 'clean_sheets', 'bonus']]
update_elements_df['team'] = update_elements_df['team'].map(teams_df.set_index('id').name)

# Map teams in fixture data and clean columns
all_fixtures_df['team_h'] = all_fixtures_df['team_h'].map(teams_df.set_index('id').name)
all_fixtures_df['team_a'] = all_fixtures_df['team_a'].map(teams_df.set_index('id').name)
all_fixtures_df['team'] = np.where(all_fixtures_df['is_home'], all_fixtures_df['team_h'], all_fixtures_df['team_a'])
all_fixtures_df['opponent'] = np.where(all_fixtures_df['is_home'], all_fixtures_df['team_a'], all_fixtures_df['team_h'])

# Merge fixtures with player names and clean unnecessary columns
all_fixtures_merged_df = pd.merge(all_fixtures_df, update_elements_df[['web_name', 'team']], on='team', how='left')
all_fixtures_merged_df.drop_duplicates(inplace=True)
all_fixtures_merged_df = all_fixtures_merged_df.drop(
    ['id', 'code', 'team_h_score', 'team_a_score', 'finished', 'minutes', 'provisional_start_time', 
     'event_name', 'team_h', 'team_a'], axis=1)

# Rename fields for clarity
fixture_rename = {
    "event": "Gameweek",
    "is_home": "Venue",
    "web_name": "Player Name",
    "kickoff_time": "Kickoff Time",
    "team": "Team",
    "opponent": "Opponent",
    "difficulty": "Difficulty"
}
all_fixtures_merged_df = all_fixtures_merged_df.rename(columns=fixture_rename)
all_fixtures_merged_df['Venue'] = all_fixtures_merged_df['Venue'].replace({True: 'Home', False: 'Away'})
all_fixtures_merged_df['Gameweek'] = all_fixtures_merged_df['Gameweek'].fillna(0).astype(int)
all_fixtures_merged_df.to_csv(f'all_fixtures_{timestamp}.csv', index=False)
# Prepare history data
all_history_merge_df = pd.merge(all_history_df, elements_df, left_on="element", right_on="id")
all_history_merge_df['opponent_team'] = all_history_merge_df.opponent_team.map(teams_df.set_index('id').name)
all_history_merge_df['team'] = all_history_merge_df.team.map(teams_df.set_index('id').name)
all_history_merge_df['element_type'] = all_history_merge_df.element_type.map(elements_types_df.set_index('id').singular_name)

# Renaming columns in history data for consistency
history_rename = {
    "web_name": "Player Name",
    "total_points_x": "Gameweek Points",
    "total_points_y": "Total Points",
    "minutes_x" : "Minutes Played",
    "goals_scored_x" : "Goals Scored",
    "assists_x" : "Assists",
    "clean_sheets_x" : "Clean Sheets",
    "goals_conceded_x" : "Goals Conceded",
    "expected_goals_conceded_x" : "xG Conceded",
    "own_goals_x" : "Own Goals",
    "penalties_saved_x" : "Penalties Saved",
    "penalties_missed_x" : "Penalties Missed",
    "yellow_cards_x" : "Yellow Cards",
    "red_cards_x" : "Red Cards",
    "saves_x" : "Saves",
    "bonus_x" : "Bonus",
    "expected_goals_x" : "xG",
    "expected_assists_x" : "xA",
    "selected_by_percent" : "Selected By(%)",
    "now_cost" : "Price",
    "goals_scored_y" : "Total GS",
    "assists_y" : "Total Assists",
    "clean_sheets_y" : "Total CS",
    "goals_conceded_y" : "Total GC",
    "expected_goals_conceded_y" : "Total xG Conceded",
    "own_goals_y" : "Total OG",
    "saves_y" : "Total Saves",
    "penalties_saved_y" : "Total Penalties Saved",
    "penalties_missed_y" : "Total Penalties Missed",
    "yellow_cards_y" : "Total YC",
    "red_cards_y" : "Total RC",
    "bonus_y" : "Total Bonus",
    "starts_y" : "Total Starts",
    "expected_goals_y" : "Total xG",
    "expected_assists_y" : "Total xA",
    "total_points_y" : "Total Points",
    "was_home" : "Venue",
    "round" : "Gameweek",
    "team_h_score" : "Home Team Score",
    "team_a_score" : "Away Team Score",
    "opponent_team" : "Opponent",
    "team" : "Team",
    "element_type" : "Position",
    "status": "Availability",
    "chance_of_playing_next_round" : "Next Round Playing Chance(%)",
    "dreamteam_count": "Dreamteam",
    "influence_x": "Influence",
    "influence_y": "Total Influence",
    "creativity_x": "Creativity",
    "creativity_y": "Total Creativity",
    "threat_x": "Threat",
    "threat_y": "Total Threat",
    "ict_index_x": "ICT Index",
    "ict_index_y": "Total ICT Index",
    "corners_and_indirect_freekicks_order": "Corners/Indirect Freekick Order",
    "direct_freekicks_order": "Direct Freekick Order",
    "penalties_order": "Penalties Order",
}
all_history_merge_df = all_history_merge_df.rename(columns=history_rename)
all_history_merge_df['Price'] = round(all_history_merge_df['Price'] / 10, 1)

# Define column dtypes for history data
column_dtypes = {'Venue': str, 'Opponent': str, 'Goals Scored': int}
all_history_merge_df = all_history_merge_df.astype(column_dtypes)

# Convert cleaned DataFrame to dictionary for MongoDB insertion
fixture_data_dict = all_fixtures_merged_df.to_dict('records')
history_data_dict = all_history_merge_df.to_dict('records')

# Clear existing data and insert updated data in MongoDB collection
collection_fixture.delete_many({})
collection_fixture.insert_many(fixture_data_dict)

collection_details.delete_many({})
collection_details.insert_many(history_data_dict)

print("Data updated successfully in MongoDB.")

# Save aggregated data to CSV files with timestamp
all_history_merge_df.to_csv(f'all_history_clean_{timestamp}.csv')
all_fixtures_merged_df.to_csv(f'all_fixtures_clean_{timestamp}.csv', index=False)