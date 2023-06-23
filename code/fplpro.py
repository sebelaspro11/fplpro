import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from pymongo.mongo_client import MongoClient
import pymongo
import configparser
from pymongo import MongoClient
import requests



page_title = "Fantasy Football Analyzer"
page_icon = ":bar_chart:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Analysis", "Points & Fixture", "In-Form & Differential Player", "History", "Manager Details", "Match Prediction"],
    icons=["bi-magic", "bi-file-earmark-bar-graph-fill", "bi-capslock", "bi-bullseye", "bi-bullseye", "bi-bullseye"], # https://icons.getbootstrap.com/
    orientation="horizontal",
)


# @st.cache_resource
# def init_connection():
#     # Read the secrets file
#     secrets = st.secrets["mongo"]

#     # Create the MongoDB client
#     client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
#     return client





# # Initialize the connection
# client = init_connection()

# # Access the 'Fplapp' database
# db = client["Fplapp"]

# # Access the collections
# collection_player = db["player"]
# collection_details = db["details"]




if selected == "Analysis":
    # Fetch the data using cache
    @st.cache_resource
    def init_connection():
        # Read the secrets file
        secrets = st.secrets["mongo"]
        # Create the MongoDB client
        client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
        return client

    # Initialize the connection
    client = init_connection()

    # Access the 'Fplapp' database
    db = client["Fplapp"]

    # Access the collections
    collection_player = db["player"]


    @st.cache_resource
    def fetch_data_player(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    # Fetch the player data
    df_player = fetch_data_player(collection_player)
    
  


    st.markdown('### Player Points Across 2022/2023 Season & Next Fixture Difficulty')
    st.markdown('##### ***Select Multiple Players For Comparison***')


    # Calculate additional columns
    df_player['90s'] = df_player['Minutes Played'] / 90
    calc_elements = ['Total Goals', 'Total Assists', 'Total Points']
    for each in calc_elements:
        df_player[f'{each} P90'] = df_player[each] / df_player['90s']
    df_player = df_player.drop('90s', axis=1)

    # Sidebar filters
    teams = st.sidebar.multiselect("Teams:", list(df_player['Team'].drop_duplicates()), default=list(df_player['Team'].drop_duplicates()))
    positions = st.sidebar.multiselect("Choose position:", list(df_player['Position'].drop_duplicates()), default=list(df_player['Position'].drop_duplicates()))
    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=0.5, value=15.0)

    # Apply filters to the player data
    df_filtered_player = df_player[df_player['Position'].isin(positions) & df_player['Team'].isin(teams) & (df_player['Price'] < price_choice)]

    # Display player data
    st.markdown('### Player Overall Data', unsafe_allow_html=True)
    st.dataframe(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True))

    st.markdown('### Points')
    st.vega_lite_chart(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True).head(5), {
         'mark': {'type': 'bar', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Total Points', 'type': 'quantitative'},
             'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })
    
    
    #     # Filtered dataframe for Goals
    # df_goals = df_filtered_player.sort_values('Total Goals', ascending=False).reset_index(drop=True)
    # top_players_goals = df_goals.head(5)

    # # Check if there are fewer than 5 players with goals
    # num_players_goals = len(df_goals)
    # if num_players_goals < 5:
    #     top_players_goals = df_goals

    # # Goals chart
    # st.markdown('### Goals')
    # st.vega_lite_chart(top_players_goals, {
    #     'mark': {'type': 'bar', 'tooltip': True},
    #     'encoding': {
    #         'x': {'field': 'Total Goals', 'type': 'quantitative'},
    #         'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
    #         'color': {'field': 'Position', 'type': 'nominal'},
    #         'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    #     },
    #     'width': 800,
    #     'height': 400,
    # })    
    #Cost vs 22/23 Season Points chart
    st.markdown('### Goals')
    st.vega_lite_chart(df_filtered_player.sort_values('Total Goals', ascending=False).reset_index(drop=True).head(5), {
         'mark': {'type': 'bar', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Total Goals', 'type': 'quantitative'},
             'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })
    
    st.markdown('### Assists')
    st.vega_lite_chart(df_filtered_player.sort_values('Total Assists', ascending=False).reset_index(drop=True).head(5), {
         'mark': {'type': 'bar', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Total Assists', 'type': 'quantitative'},
             'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })
    
    st.markdown('### Bonus')
    st.vega_lite_chart(df_filtered_player.sort_values('Total Bonus', ascending=False).reset_index(drop=True).head(5), {
         'mark': {'type': 'bar', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Total Bonus', 'type': 'quantitative'},
             'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })
    

    
    # Cost vs 22/23 Season Points chart
    st.markdown('### Cost vs 22/23 Season Points')
    st.markdown('##### ***Identify Low Price Player With High Points Return***')
    st.vega_lite_chart(df_filtered_player, {
         'mark': {'type': 'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Price', 'type': 'quantitative'},
             'y': {'field': 'Total Points', 'type': 'quantitative'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })

    # Goals per 90 chart
    st.markdown('### Goals per 90')
    st.markdown('##### ***Player Total Goals, Assists and Points per 90 Minutes***')
    st.vega_lite_chart(df_filtered_player, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'Total Goals P90', 'type': 'quantitative'},
         'y': {'field': 'Total Assists P90', 'type': 'quantitative'},
         'color': {'field': 'Position', 'type': 'nominal'},
         'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Goals P90', 'type': 'quantitative'}, {'field': 'Total Assists P90', 'type': 'quantitative'}, {'field': 'Total Points P90', 'type': 'quantitative'}],
     },
     'width': 800,
     'height': 400,
    })
  
    

if selected == "Points & Fixture":
    

    # Fetch data using cache
    @st.cache_resource
    def init_connection():
        # Read the secrets file
        secrets = st.secrets["mongo"]
        # Create the MongoDB client
        client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
        return client

    # Initialize the connection
    client = init_connection()

    # Access the 'Fplapp' database
    db = client["Fplapp"]

    # Access the collections
    collection_details = db["details"]

    @st.cache_resource
    def fetch_data_history(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))


    st.markdown('### Player Points Across 2022/2023 Season & Next Fixture Difficulty')
    st.markdown('##### ***Select Multiple Players For Comparison***')
    # Fetch history and fixtures data
    df_history_2023 = fetch_data_history(collection_details)
    df_fixtures_2023 = pd.read_csv('./data/fixtures_update-20230526.csv')
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

    # Sidebar filters
    positions = list(df_history_2023['Position'].drop_duplicates())
    positions.sort()
    position_choice = st.sidebar.selectbox('Choose position:', positions)
    teams_filter = list(df_history_2023['Team'].drop_duplicates())
    teams_choice = st.sidebar.multiselect('Choose team:', teams_filter)
    players_filter = df_history_2023[(df_history_2023['Team'].isin(teams_choice)) & (df_history_2023['Position'] == position_choice)]
    players_choice = st.sidebar.multiselect('Choose player:', players_filter['Player Name'].unique())

    # Display player points and fixtures
    for player in players_choice:
        df_history_2023_player = df_history_2023[(df_history_2023['Player Name'] == player) & (df_history_2023['Position'] == position_choice) & (df_history_2023['Team'].isin(teams_choice))]

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'### {player} Match Points')
            c = alt.Chart(df_history_2023_player).mark_bar().encode(
                x=alt.X('Opponent'),
                y=alt.Y('Gameweek Points'),
                color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['red', 'blue'])),
                tooltip=['Gameweek:N', 'Gameweek Points:Q', 'Goals Scored:Q', 'Assists:Q', 'Bonus:Q']
            ).configure_axis(grid=False)
            st.altair_chart(c, use_container_width=True, theme="streamlit")

            df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) & (df_fixtures_2023['Team'].isin(teams_choice))]
        with col2:
            
            st.markdown(f'### {player} Next Fixtures')
            color_scale = alt.Scale(domain=[2, 3, 4, 5], range=['green', 'blue', 'yellow', 'red'])
            y_limit = [0, 5]
            d = alt.Chart(df_fixtures_2023_player).mark_square(stroke=None, size=200).encode(
                x=alt.X('Opponent:N', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Difficulty:Q', axis=alt.Axis(format='d'), scale=alt.Scale(domain=y_limit)),
                color=alt.Color('Difficulty:Q', scale=color_scale),
                tooltip=['Venue:N','Gameweek:N', 'Player Name:N', 'Opponent:N', 'Difficulty:Q']
            ).configure_axis(grid=False)

            st.altair_chart(d, use_container_width=True, theme="streamlit")




        
        
if selected == "In-Form & Differential Player":
    
    @st.cache_resource
    def init_connection():
        # Read the secrets file
        secrets = st.secrets["mongo"]

    # Create the MongoDB client
        client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
        return client

    # Initialize the connection
    client = init_connection()

    # Access the 'Fplapp' database
    db = client["Fplapp"]

    # Access the collections
    collection_details = db["details"]
    
    
    
    @st.cache_resource
    def fetch_data_history(_collect):
    # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    df_history_2023 = fetch_data_history(collection_details)

    st.markdown(f'### Top Performer Player Based On Last 3 Gameweeks')
 
    
    df_history_2023['Last 3 GW Goals'] = df_history_2023.groupby('Player Name')['Goals Scored'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Assists'] = df_history_2023.groupby('Player Name')['Assists'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Points'] = df_history_2023.groupby('Player Name')['Gameweek Points'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Clean Sheets'] = df_history_2023.groupby('Player Name')['Clean Sheets'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Conceded'] = df_history_2023.groupby('Player Name')['Goals Conceded'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Saves'] = df_history_2023.groupby('Player Name')['Saves'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW Bonus Points'] = df_history_2023.groupby('Player Name')['Bonus'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW xG'] = df_history_2023.groupby('Player Name')['xG'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW xA'] = df_history_2023.groupby('Player Name')['xA'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 GW xG Conceded'] = df_history_2023.groupby('Player Name')['xG Conceded'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)

    max_gw = df_history_2023['Gameweek'].max()
    df1 = df_history_2023[df_history_2023['Gameweek'] == max_gw]


    # Filter players based on position distribution
    goalkeepers = df1[df1['Position'] == 'Goalkeeper']
    defenders = df1[df1['Position'] == 'Defender']
    midfielders = df1[df1['Position'] == 'Midfielder']
    forwards = df1[df1['Position'] == 'Forward']
    
    # Convert 'Selected By(%)' column to numeric data type
    goalkeepers['Selected By(%)'] = pd.to_numeric(goalkeepers['Selected By(%)'], errors='coerce')
    defenders['Selected By(%)'] = pd.to_numeric(defenders['Selected By(%)'], errors='coerce')
    midfielders['Selected By(%)'] = pd.to_numeric(midfielders['Selected By(%)'], errors='coerce')
    forwards['Selected By(%)'] = pd.to_numeric(forwards['Selected By(%)'], errors='coerce')
    
    
    # Sort players based on desired criteria
    gk_top = goalkeepers[goalkeepers['Availability'] == 'a'].sort_values(['Last 3 GW Points', 'Last 3 GW Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    def_top = defenders[defenders['Availability'] == 'a'].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA','Last 3 GW Clean Sheets', 'Last 3 GW Conceded','Last 3 GW xG Conceded'], ascending=[False, False, False, False, False, False, False, True, True])
    mid_top = midfielders[midfielders['Availability'] == 'a'].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)
    fwd_top = forwards[forwards['Availability'] == 'a'].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)
    gk_diff = goalkeepers[(goalkeepers['Availability'] == 'a') & (goalkeepers['Selected By(%)'] < 10)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    def_diff = defenders[(defenders['Availability'] == 'a') & (defenders['Selected By(%)'] < 10)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    mid_diff = midfielders[(midfielders['Availability'] == 'a') & (midfielders['Selected By(%)'] < 10)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    fwd_diff = forwards[(forwards['Availability'] == 'a') & (forwards['Selected By(%)'] < 10)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])

    
    max_goalkeeper_price = 5.0
    max_defender_price = 5.0
    max_midfielder_price = 6.0
    max_forward_price = 6.5
    
    gk_price = goalkeepers[(goalkeepers['Availability'] == 'a') & (goalkeepers['Price'] < max_goalkeeper_price)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    def_price = defenders[(defenders['Availability'] == 'a') & (defenders['Price'] < max_defender_price)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    mid_price = midfielders[(midfielders['Availability'] == 'a') & (midfielders['Price'] < max_midfielder_price)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    fwd_price = forwards[(forwards['Availability'] == 'a') & (forwards['Price'] < max_forward_price)].sort_values(['Last 3 GW Points', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW Saves', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded'], ascending=[False, False, False, False, True, True])
    
    # Select top players for each position
    gk_top = gk_top.head(5).drop_duplicates(subset=['Player Name'])
    def_top = def_top.head(5).drop_duplicates(subset=['Player Name'])
    mid_top = mid_top.head(5).drop_duplicates(subset=['Player Name'])
    fwd_top = fwd_top.head(5).drop_duplicates(subset=['Player Name'])
    gk_diff = gk_diff.head(2).drop_duplicates(subset=['Player Name'])
    def_diff = def_diff.head(5).drop_duplicates(subset=['Player Name'])
    mid_diff = mid_diff.head(5).drop_duplicates(subset=['Player Name'])
    fwd_diff = fwd_diff.head(3).drop_duplicates(subset=['Player Name'])
    gk_price = gk_price.head(2).drop_duplicates(subset=['Player Name'])
    def_price = def_price.head(5).drop_duplicates(subset=['Player Name'])
    mid_price = mid_price.head(5).drop_duplicates(subset=['Player Name'])
    fwd_price = fwd_price.head(3).drop_duplicates(subset=['Player Name'])

    # Concatenate selected players into a final DataFrame
    selected_players = pd.concat([gk_top, def_top, mid_top, fwd_top])
    diff_players = pd.concat([gk_diff, def_diff, mid_diff, fwd_diff])
    price_players = pd.concat([gk_price, def_price, mid_price, fwd_price])

    
    st.markdown(f'##### ***Top 5 Player For Every Position***')
    

    # Define team colors
    team_colors = {
        'Arsenal': '#EF0107',
        'Aston Villa': '#C32148',
        'Bournemouth': '#DA291C',
        'Brentford': '#e30613',
        'Brighton': '#0057B8',
        'Chelsea': '#034694',
        'Crystal Palace': '#C4122E',
        'Everton': '#003399',
        'Fulham': '#CC0000',
        'Leeds': ' #FFCD00',
        'Leicester': '#003090',
        'Liverpool': '#C8102E',
        'Man City': '#6CABDD',
        'Man Utd': '#DA291C',
        'Newcastle': '#241F20',
        "Nott'm Forest": '#e53233',
        'Southampton': '#DD0000',
        'Spurs': '#132257',
        'West Ham': ' #7A263A',
        'Wolves': '#FDB913',
    }
    

    # Filter team_colors dictionary based on teams in the data
    color_gk_top = set(gk_top['Team'])  # Assuming 'Team' is the column name in the data
    color_def_top = set(def_top['Team'])  # Assuming 'Team' is the column name in the data
    color_mid_top = set(mid_top['Team'])  # Assuming 'Team' is the column name in the data
    color_fwd_top = set(fwd_top['Team'])  # Assuming 'Team' is the column name in the data
    team_colors_gk_top = {team: color for team, color in team_colors.items() if team in color_gk_top}
    team_colors_def_top  = {team: color for team, color in team_colors.items() if team in color_def_top}
    team_colors_mid_top  = {team: color for team, color in team_colors.items() if team in color_mid_top}
    team_colors_fwd_top  = {team: color for team, color in team_colors.items() if team in color_fwd_top}

    # Create the bar chart
    goalkeeper_chart = alt.Chart(gk_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        fill=alt.Fill('Team:N', scale=alt.Scale(domain=list(team_colors_gk_top.keys()), range=list(team_colors_gk_top.values()))),
        tooltip=[
            'Last 3 GW Points',
            'Last 3 GW Clean Sheets',
            'Last 3 GW Bonus Points',
            'Last 3 GW Saves',
            'Last 3 GW Conceded',
            'Last 3 GW xG Conceded',
            'Total Yellow Cards'
        ]
    ).configure_axis(grid=False)






    defender_chart = alt.Chart(def_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        #color=alt.Color('Team'),
        #color=alt.Color('Team:N', scale=color_scale, condition=alt.condition('datum.Total Yellow Cards == 4', alt.value('red'))),
        color=alt.Color('Team:N', scale=alt.Scale(domain=list(team_colors_def_top.keys()), range=list(team_colors_def_top.values()))),
        tooltip=['Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Bonus Points', 'Last 3 GW Clean Sheets', 'Last 3 GW xG', 'Last 3 GW xA', 'Last 3 GW Conceded', 'Last 3 GW xG Conceded', 'Total Yellow Cards']
    ).configure_axis(grid=False)

    color_scale = alt.Scale(domain=[4], range=['red'])

    midfielder_chart = alt.Chart(mid_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        fill=alt.Fill('Team:N', scale=alt.Scale(domain=list(team_colors_mid_top.keys()), range=list(team_colors_mid_top.values()))),
        tooltip=['Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Bonus Points', 'Last 3 GW xG', 'Last 3 GW xA', 'Total Yellow Cards']
    ).configure_axis(grid=False)


    forward_chart = alt.Chart(fwd_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        #color=alt.Color('Team'),
        fill=alt.Fill('Team:N', scale=alt.Scale(domain=list(team_colors_fwd_top.keys()), range=list(team_colors_fwd_top.values()))),
        tooltip=['Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Bonus Points', 'Last 3 GW xG', 'Last 3 GW xA', 'Total Yellow Cards']
    ).configure_axis(grid=False)
    
    diff_chart = alt.Chart(diff_players).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        color=alt.Color('Position'),
        tooltip=['Selected By(%)','Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Bonus Points', 'Last 3 GW xG', 'Last 3 GW xA', 'Total Yellow Cards']
    ).configure_axis(grid=False).configure_axis(grid=False)
    
    price_chart = alt.Chart(price_players).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Last 3 GW Points'),
        color=alt.Color('Position'),
        tooltip=['Price','Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Bonus Points', 'Last 3 GW xG', 'Last 3 GW xA', 'Total Yellow Cards']
    ).configure_axis(grid=False)
       
       
        # Filter the DataFrame to select the top 10 players with the most yellow cards
    top_10_yellow_cards = df_history_2023.sort_values('Total Yellow Cards', ascending=False)
    top_10_yellow_cards = top_10_yellow_cards.drop_duplicates(subset=['Player Name']).head(10)

    # Create the altair chart
    yc_chart = alt.Chart(top_10_yellow_cards).mark_bar().encode(
        y=alt.Y('Player Name', sort=alt.EncodingSortField('Total Yellow Cards:Q'), axis=alt.Axis(labelAngle=0)),
        x=alt.X('Total Yellow Cards'),
        color=alt.Color('Position'),
        tooltip=['Player Name', 'Total Yellow Cards']
    ).properties(
        width=500,
        height=300).configure_axis(grid=False)
    
    
    # Define the specific total yellow card values
    total_yellow_cards = [4, 9, 14, 19]

    # Filter the DataFrame to select players with the desired total yellow card values
    warn_yellow_cards = df_history_2023[df_history_2023['Total Yellow Cards'].isin(total_yellow_cards)]

    warn_yellow_cards = warn_yellow_cards.sort_values('Total Yellow Cards', ascending=False)
    warn_yellow_cards = warn_yellow_cards.drop_duplicates(subset=['Player Name']).head(10)
    
    
    yc_warn_chart = alt.Chart(warn_yellow_cards).mark_bar().encode(
        x=alt.X('Total Yellow Cards'),
        y=alt.Y('Player Name', sort=alt.EncodingSortField('Total Yellow Cards:Q'), axis=alt.Axis(labelAngle=0)),
        color=alt.Color('Position'),
        tooltip=['Player Name', 'Total Yellow Cards']
    ).properties(
        width=500,
        height=300).configure_axis(grid=False)

    
    top_10_red_cards = df_history_2023.sort_values('Total Red Cards', ascending=False)
    top_10_red_cards = top_10_red_cards.drop_duplicates(subset=['Player Name']).head(10)
    top_10_red_cards['Total Red Cards'] = pd.to_numeric(top_10_red_cards['Total Red Cards'])

    # Create the altair chart
    rc_chart = alt.Chart(top_10_red_cards).mark_bar().encode(
        x=alt.X('Total Red Cards:Q'),
        y=alt.Y('Player Name', sort=alt.EncodingSortField('Total Red Cards:Q'), axis=alt.Axis(labelAngle=0)),
        color=alt.Color('Position'),
        tooltip=['Player Name', 'Total Red Cards'],
        #order=alt.Order("Total Red Cards", sort="ascending"),
    ).properties(
        width=500,
    ).configure_axis(grid=False)

    

    
    # Display the bar chart figures
    st.markdown(f'##### ***Goalkeeper***')
    st.altair_chart(goalkeeper_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Defender***')
    st.altair_chart(defender_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Midfielder***')
    st.altair_chart(midfielder_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Forwards***')
    st.altair_chart(forward_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'### Top Eleven In-Form Differential Players')
    st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Selected By Lower Than 10%***')
    st.markdown(f'##### ***Value of Selected By Subject To Change***')
    
    
    st.altair_chart(diff_chart, use_container_width=True, theme="streamlit")
    
    st.markdown(f'### Top Eleven In-Form Budget Players')
    st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Budget Price***')
    st.markdown(f'##### ***:green[Goalkeeper < $5.0]***')
    st.markdown(f'##### ***:green[Defender < $5.0]***')
    st.markdown(f'##### ***:green[Midfielder < $6.0]***')
    st.markdown(f'##### ***:green[Forward < $6.5]***')
    st.altair_chart(price_chart, use_container_width=True, theme="streamlit")
    
    st.markdown(f'### Yellow Cards Record')
    st.altair_chart(yc_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'### Suspension Warning')
    st.altair_chart(yc_warn_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'### Red Cards Record')
    st.altair_chart(rc_chart, use_container_width=True, theme="streamlit")


    
if selected == "History":
    @st.cache_resource
    def init_connection():
        # Read the secrets file
        secrets = st.secrets["mongo"]

    # Create the MongoDB client
        client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
        return client

    # Initialize the connection
    client = init_connection()

    # Access the 'Fplapp' database
    db = client["Fplapp"]

    # Access the collections
    collection_history = db["history"]
    
    
    
    @st.cache_resource
    def fetch_data_past_history(_collect):
    # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    df_past_history_2023 = fetch_data_past_history(collection_history)
    
    
    
    # Sidebar filters
    season_hist = st.sidebar.multiselect("Seasons:", list(df_past_history_2023['Seasons'].drop_duplicates()), default=list(df_past_history_2023['Seasons'].drop_duplicates()))
    player_hist = st.sidebar.multiselect("Player Name:", df_past_history_2023[df_past_history_2023['Seasons'].isin(season_hist)]['Player Name'].drop_duplicates().tolist())
    # Apply filters to the player data
    df_hist_player_filter = df_past_history_2023[df_past_history_2023['Seasons'].isin(season_hist) & df_past_history_2023['Player Name'].isin(player_hist)]
    
    st.dataframe(df_hist_player_filter.sort_values('Seasons', ascending=False).reset_index(drop=True))
    st.data_editor(
    df_hist_player_filter,
    column_config={
        "Seasons": st.column_config.TextColumn(
            "Seasons",
            help="Seasons Played",
            default="st.",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
    },
    hide_index=True,
)

if selected == "Manager Details":

    manager_id = st.text_input("Enter manager ID:")
    if manager_id:
        url = 'https://fantasy.premierleague.com/api/entry//' + manager_id
        r = requests.get(url)
        json = r.json()
        manager_df = pd.DataFrame(json)
        manager_df = manager_df.iloc[[0, 3], :]
        manager_df['All Leagues'] = manager_df['leagues'].apply(lambda x: ', '.join([item['name'] for item in x]))
        manager_df = manager_df[['joined_time', 'player_first_name', 'player_last_name', 'player_region_iso_code_short', 'summary_overall_points', 'summary_overall_rank', 'summary_event_rank','summary_event_points', 'All Leagues', 'current_event' ]]

        # Rename the columns using the rename() method
        new_names = {
            "player_first_name" : "First Name",
            "player_last_name" : "Last Name",
            "player_region_iso_code_short" : "Country Code",
            "joined_time" : "Registered Time",
            "summary_event_points" : "Current Points",
            "summary_overall_points" : "Total Points",
            "summary_event_rank" : "Gameweek Rank",
            "summary_overall_rank" : "Last Rank",
            "All Leagues" : "League Entered",
            "current_event" : "Gameweek"
        }
        manager_df = manager_df.rename(columns=new_names)

        # Display First Name and Last Name
        st.write("First Name:", manager_df['First Name'].values[0])
        st.write("Last Name:", manager_df['Last Name'].values[0])
        st.write("Registered Time:", manager_df['Registered Time'].values[0])
        st.write("League Entered:", manager_df['League Entered'].values[0])
        st.write("Current Points:", manager_df['Current Points'].values[0])
        st.write("Total Points:", manager_df['Total Points'].values[0])
        st.write("Current Rank:", manager_df['Gameweek Rank'].values[0])
        st.write("Last Rank:", manager_df['Last Rank'].values[0])
        st.write("Gameweek:", manager_df['Gameweek'].values[0])
    
    
    
if selected == "Match Prediction":
    st.markdown(f'### Match Prediction from FiveThirtyEight.com')
    st.markdown(f'##### ***Prediction For League Standings & Upcoming Matches***')
    with st.echo():
        st.write(f"streamlit version: {st.__version__}")

    # embed streamlit docs in a streamlit app
    components.iframe("https://projects.fivethirtyeight.com/soccer-predictions/premier-league/", width=1500, height=2000, scrolling=True)
    
    
    
    

#client.close()
