import pandas as pd
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import streamlit.components.v1 as components
import plotly.express as px








def perform_point_fixture():

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
    df_fixtures_2023 = pd.read_csv('D:/streamlit/fpl/fixtures_update-20230526.csv')
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

    # Sidebar filters
    positions = list(df_history_2023['Position'].drop_duplicates())
    positions.sort()
    position_choice = st.sidebar.selectbox('Choose position:', positions)
    teams_filter = list(df_history_2023['Team'].drop_duplicates())
    teams_choice = st.sidebar.multiselect('Choose team:', teams_filter, default = [teams_filter[0]])
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
                x=alt.X('Opponent'),
                y=alt.Y('Gameweek Points:Q', axis=alt.Axis(format='d')),
                color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['#B6006C', '#00B6A3'])),
                tooltip=['Player Name:N', 'Gameweek:N', 'Gameweek Points:Q', 'Goals Scored:Q', 'Assists:Q', 'Bonus:Q']
            ).configure_axis(grid=True)
            st.altair_chart(c, use_container_width=True, theme="streamlit")

            df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) & (df_fixtures_2023['Team'].isin(teams_choice))]
        with tab2:
            
            st.markdown(f'### {player} Next Fixtures')
            color_scale = alt.Scale(domain=[2, 3, 4, 5], range=['green', 'blue', 'yellow', 'red'])
            y_limit = [0, 5]
            d = alt.Chart(df_fixtures_2023_player).mark_circle(stroke=None, size=200).encode(
                x=alt.X('Opponent:N', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Difficulty:Q', axis=alt.Axis(format='d'), scale=alt.Scale(domain=y_limit)),
                color=alt.Color('Difficulty:Q', scale=color_scale),
                tooltip=['Player Name:N', 'Venue:N','Gameweek:N', 'Opponent:N', 'Difficulty:Q']
            ).configure_axis(grid=True)

            st.altair_chart(d, use_container_width=True, theme="streamlit")
        
        # def record_fixture_chart(df_history_2023_player, category, tooltip):

        
        #     # Filter the data to include only the top 5 players
        #     df = df_history_2023_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
        #     # Create the bar chart
        #     fig = px.bar(
        #         df,
        #         y="Gameweek Points",
        #         x="Opponent",
        #         color="Position",
        #         color_discrete_map=position_colors,  # Set custom colors for each position
        #         text="Team",
        #         hover_data=tooltip.get(category, {})

        #     )
        #     custom_font_family = "Arial"
            
        #     # Set the custom font for the text
        #     fig.update_layout(
        #         font_family=custom_font_family,
        #         font_color="black",  # Optionally, set the font color
        #     )
            
        #     return fig


        # tooltip = {
        # "Total Points": {"Player Name": True, "Team": True, "Total Points": True}
        # }
 
        # fig_points = record_fixture_chart(df_history_2023_player, "Total Points", tooltip)
        # st.plotly_chart(fig_points, theme="streamlit", use_container_width=True)
    