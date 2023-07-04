import pandas as pd
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import streamlit.components.v1 as components








def perform_point_fixture():
    st.markdown(f'### Match Fixture')

    components.iframe("https://www.premierleague.com/fixtures", width=1200, height=800, scrolling=True)

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
    df_fixtures_2023 = pd.read_csv('data/fixtures_update-20230526.csv')
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

        tab1, tab2 = st.columns(2)
        
        with tab1:
            st.markdown(f'### {player} Match Points')
            c = alt.Chart(df_history_2023_player).mark_bar().encode(
                x=alt.X('Opponent'),
                y=alt.Y('Gameweek Points'),
                color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['red', 'blue'])),
                tooltip=['Gameweek:N', 'Gameweek Points:Q', 'Goals Scored:Q', 'Assists:Q', 'Bonus:Q']
            ).configure_axis(grid=False)
            st.altair_chart(c, use_container_width=True, theme="streamlit")

            df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) & (df_fixtures_2023['Team'].isin(teams_choice))]
        with tab2:
            
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
