import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient

def perform_point_fixture():

    # Fetch data using cache
    @st.cache_resource(show_spinner=False)
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
    collection_fixture = db["fixture"]

    @st.cache_resource(show_spinner=False)
    def fetch_data_history(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    @st.cache_resource(show_spinner=False)
    def fetch_data_fixture(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    st.markdown('## Player Gameweek Points & Fixture Difficulty Ranking')
    st.markdown('##### ***Select Multiple Players For Comparison***')
    
    # Fetch history and fixtures data
    df_history_2023 = fetch_data_history(collection_details)
    df_fixtures_2023 = fetch_data_fixture(collection_fixture)
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

    # Sidebar filters
    positions = list(df_history_2023['Position'].drop_duplicates())
    positions.sort()
    position_choice = st.sidebar.selectbox('Choose position:', positions)
    teams_filter = list(df_history_2023['Team'].drop_duplicates())
    
    # Initialize teams_choice with a default value if it's empty
    teams_choice = st.sidebar.multiselect('Choose team:', teams_filter, default=[teams_filter[0]])

    # Handle the scenario when no teams are selected
    if not teams_choice:
        teams_choice = [teams_filter[0]]  # Provide a default team

    players_filter = df_history_2023.sort_values("Total Points", ascending=False)[(df_history_2023['Team'].isin(teams_choice)) & (df_history_2023['Position'] == position_choice)]
    players_choice = st.sidebar.multiselect('Choose player:', players_filter['Player Name'].unique(), default=[players_filter['Player Name'].unique()[0]])

    # Display player points and fixtures
    for player in players_choice:
        df_history_2023_player = df_history_2023[(df_history_2023['Player Name'] == player) & (df_history_2023['Position'] == position_choice) & (df_history_2023['Team'].isin(teams_choice))]

        # Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#60DB00',
            'Defender': '#B141FF',
            'Midfielder': '#00DADA',
            'Forward': '#9DB600',
        }
        tab1, tab2 = st.columns(2)
        
        with tab1:
            st.markdown(f'### {player} Match Points')
            c = alt.Chart(df_history_2023_player).mark_bar().encode(
                x=alt.X('Opponent', sort=alt.EncodingSortField('Gameweek')),
                y=alt.Y('Gameweek Points:Q', axis=alt.Axis(format='d')),
                color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['#B6006C', '#00B6A3'])),
                tooltip=['Player Name:N', 'Gameweek:N', 'Gameweek Points:Q', 'Goals Scored:Q', 'Assists:Q', 'Bonus:Q']
            ).configure_axis(grid=True)
            st.altair_chart(c, use_container_width=True, theme="streamlit")

            df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) & (df_fixtures_2023['Team'].isin(teams_choice))]
            df_fixtures_2023_player_next5 = df_fixtures_2023_player.head(5)      
        with tab2:
            
            st.markdown(f'### {player} Next Fixtures')
            color_scale = alt.Scale(domain=[2, 3, 4, 5], range=['green', 'blue', 'yellow', 'red'])
            y_limit = [0, 5]
            d = alt.Chart(df_fixtures_2023_player_next5).mark_bar().encode(
                x=alt.X('Opponent:N', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Difficulty:Q', axis=alt.Axis(format='d'), scale=alt.Scale(domain=y_limit)),
                color=alt.Color('Difficulty:Q', scale=color_scale),
                tooltip=['Player Name:N', 'Venue:N','Gameweek:N', 'Opponent:N', 'Difficulty:Q']
            ).configure_axis(grid=True)

            st.altair_chart(d, use_container_width=True, theme="streamlit")
