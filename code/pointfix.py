# import pandas as pd
# import streamlit as st
# import altair as alt
# from pymongo.mongo_client import MongoClient


# def perform_point_fixture():

#     # Fetch data using cache
#     @st.cache_resource(show_spinner=False)
#     def init_connection():
#         # Read the secrets file
#         secrets = st.secrets["mongo"]
#         # Create the MongoDB client
#         client = MongoClient(secrets["host"], username=secrets["username"], password=secrets["password"])
#         return client

#     # Initialize the connection
#     client = init_connection()

#     # Access the 'Fplapp' database
#     db = client["Fplapp"]

#     # Access the collections
#     collection_details = db["details"]
#     collection_fixture = db["fixture"]

#     @st.cache_resource(show_spinner=False,ttl=10800)
#     def fetch_data_history(_collect):
#         # Fetch the data from the collection
#         return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

#     @st.cache_resource(show_spinner=False,ttl=10800)
#     def fetch_data_fixture(_collect):
#         # Fetch the data from the collection
#         return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

#     st.markdown('## Player Gameweek Points & Fixture Difficulty Ranking')
#     st.markdown('##### ***Select Multiple Players For Comparison***')
    
#     # Fetch history and fixtures data
#     df_history_2023 = fetch_data_history(collection_details)
#     df_fixtures_2023 = fetch_data_fixture(collection_fixture)
#     df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

#     # Sidebar filters
#     positions = list(df_history_2023['Position'].drop_duplicates())
#     positions.sort()
#     position_choice = st.sidebar.selectbox('Choose position:', positions)
#     teams_filter = list(df_history_2023['Team'].drop_duplicates())
    
#     # Initialize teams_choice with a default value if it's empty
#     teams_choice = st.sidebar.multiselect('Choose team:', teams_filter, default=[teams_filter[0]])

#     # Handle the scenario when no teams are selected
#     if not teams_choice:
#         teams_choice = [teams_filter[0]]  # Provide a default team

#     players_filter = df_history_2023.sort_values("Total Points", ascending=False)[(df_history_2023['Team'].isin(teams_choice)) & (df_history_2023['Position'] == position_choice)]
#     players_choice = st.sidebar.multiselect('Choose player:', players_filter['Player Name'].unique(), default=[players_filter['Player Name'].unique()[0]])

#     # Display player points and fixtures
#     for player in players_choice:
#         df_history_2023_player = df_history_2023[(df_history_2023['Player Name'] == player) & (df_history_2023['Position'] == position_choice) & (df_history_2023['Team'].isin(teams_choice))]

#         # Define custom colors for each position
#         position_colors = {
#             'Goalkeeper': '#60DB00',
#             'Defender': '#B141FF',
#             'Midfielder': '#00DADA',
#             'Forward': '#9DB600',
#         }
#         tab1, tab2 = st.columns(2)
        
#         with tab1:
#             st.markdown(f'### {player} Match Points')
#             c = alt.Chart(df_history_2023_player).mark_bar().encode(
#                 x=alt.X('Opponent', sort=alt.EncodingSortField('Gameweek')),
#                 y=alt.Y('Gameweek Points:Q', axis=alt.Axis(format='d')),
#                 color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['#B6006C', '#00B6A3'])),
#                 tooltip=['Player Name:N', 'Gameweek:N', 'Gameweek Points:Q', 'Goals Scored:Q', 'Assists:Q', 'Bonus:Q']
#             ).configure_axis(grid=True)
#             st.altair_chart(c, use_container_width=True, theme="streamlit")

#             df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) & (df_fixtures_2023['Team'].isin(teams_choice))]
#             df_fixtures_2023_player_next5 = df_fixtures_2023_player.head(5)      
#         with tab2:
            
#             st.markdown(f'### {player} Next Fixtures')
#             color_scale = alt.Scale(domain=[2, 3, 4, 5], range=['green', 'blue', 'yellow', 'red'])
#             y_limit = [0, 5]
#             d = alt.Chart(df_fixtures_2023_player_next5).mark_bar().encode(
#                 x=alt.X('Opponent:N', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
#                 y=alt.Y('Difficulty:Q', axis=alt.Axis(format='d'), scale=alt.Scale(domain=y_limit)),
#                 color=alt.Color('Difficulty:Q', scale=color_scale),
#                 tooltip=['Player Name:N', 'Venue:N','Gameweek:N', 'Opponent:N', 'Difficulty:Q']
#             ).configure_axis(grid=True)

#             st.altair_chart(d, use_container_width=True, theme="streamlit")


import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
import plotly.express as px


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
    
    
    df_history_2023["Venue"] = df_history_2023["Venue"].astype(str)
    df_history_2023["Venue"] = df_history_2023["Venue"].map({True: "Home", False: "Away"}).fillna(df_history_2023["Venue"])


    # Main Filter Section
    st.markdown("### Filter Players")

    # Create three columns for filters
    col1, col2, col3 = st.columns(3)

    # Place the filters in respective columns
    with col1:
        # Teams filter
        teams_filter = list(df_history_2023['Team'].unique())
        teams_choice = st.multiselect(
            "Select Teams:", 
            options=teams_filter, 
            default=[teams_filter[0]]
        )

    with col2:
        # Positions filter
        positions = list(df_history_2023['Position'].unique())
        position_choice = st.multiselect(
            "Select Positions:", 
            options=positions, 
            default=[positions[0]]
        )
    with col3:
        # Filter players dynamically based on team and position selection
        filtered_players = df_history_2023[
            (df_history_2023['Team'].isin(teams_choice)) & 
            (df_history_2023['Position'].isin(position_choice))
        ]

        players_filter = filtered_players['Player Name'].unique()

        # Determine the default player based on highest total points
        if not filtered_players.empty:
            highest_points_player = filtered_players.loc[
                filtered_players['Total Points'].idxmax(), 'Player Name'
            ]
        else:
            highest_points_player = None

        players_choice = st.multiselect(
            "Select Players:",
            options=players_filter,
            default=[highest_points_player] if highest_points_player else []  # Default to the player with the highest points
        )


    # Display player points and fixtures
    if players_choice:  # Check if any players are selected
        for player in players_choice:
            df_history_2023_player = df_history_2023[
                (df_history_2023['Player Name'] == player) & 
                (df_history_2023['Position'].isin(position_choice)) & 
                (df_history_2023['Team'].isin(teams_choice))
            ]

            # Define custom colors for each position
            position_colors = {
                'Goalkeeper': '#60DB00',
                'Defender': '#B141FF',
                'Midfielder': '#00DADA',
                'Forward': '#9DB600',
            }

            # Create tabs for player data
            tab1, tab2 = st.columns(2)

            # Tab 1: Player Match Points
            with tab1:
                st.markdown(f'### {player} Match Points')
                if not df_history_2023_player.empty:
                 

                    # Sort by Gameweek
                    df_history_2023_player = df_history_2023_player.sort_values('Gameweek')
                    df_history_2023_player["Venue"] = df_history_2023_player["Venue"].astype(str)
                    df_history_2023_player["Venue"] = df_history_2023_player["Venue"].map({True: "Home", False: "Away"}).fillna(df_history_2023_player["Venue"])




                    # Create a bar chart using Plotly Express
                    fig_points = px.bar(
                        df_history_2023_player,
                        x='Opponent',
                        y='Gameweek Points',
                        #color=alt.Color('Venue:N', scale=alt.Scale(domain=['Home', 'Away'], range=['#B6006C', '#00B6A3'])),
                        color='Venue',
                        color_discrete_map={'Home': '#B6006C', 'Away': '#00B6A3', 'unknown':'#CCCCCC'},
                        title=f"{player} Match Points",
                        hover_data=['Player Name', 'Gameweek', 'Goals Scored', 'Assists', 'Bonus'],
                        labels={'Gameweek Points': 'Points', 'Opponent': 'Opponent Team', 'Venue': 'Venue'}
                    )

                    # Update layout to ensure proper sorting and axis labeling
                    fig_points.update_layout(
                        xaxis=dict(categoryorder='array', categoryarray=df_history_2023_player['Opponent']),
                        xaxis_title="Opponent",
                        yaxis_title="Gameweek Points",
                        title_x=0.5,
                        legend_title="Venue"
                    )

                    # Display the chart
                    st.plotly_chart(fig_points, use_container_width=True)
                else:
                    st.warning(f"No match points data available for player: {player}")

            # Tab 2: Player Next Fixtures
            with tab2:
                df_fixtures_2023_player = df_fixtures_2023[
                    (df_fixtures_2023['Player Name'] == player) & 
                    (df_fixtures_2023['Team'].isin(teams_choice))
                ]
                df_fixtures_2023_player_next5 = df_fixtures_2023_player.head(5)
                st.markdown(f'### {player} Next Fixtures')

                if not df_fixtures_2023_player_next5.empty:
                    # Create a mapping of difficulty levels to colors
                    difficulty_colors = {
                        1: "green",
                        2: "blue",
                        3: "yellow",
                        4: "red",
                        5: "darkred"
                    }

                    # Add a column for color labels based on difficulty
                    df_fixtures_2023_player_next5['Difficulty Label'] = df_fixtures_2023_player_next5['Difficulty'].map(difficulty_colors)

                    # Create a bar chart using Plotly Express with discrete colors
                    fig_fixtures = px.bar(
                        df_fixtures_2023_player_next5,
                        x='Opponent',
                        y='Difficulty',
                        color='Difficulty',  # Use the mapped difficulty labels for color
                        title=f"{player} Next 5 Fixtures",
                        hover_data=['Player Name', 'Venue', 'Gameweek', 'Difficulty'],
                        labels={'Difficulty': 'Fixture Difficulty'},
                        color_discrete_map=difficulty_colors  # Use the custom color mapping
                    )

                    fig_fixtures.update_layout(
                        xaxis_title="Opponent",
                        yaxis_title="Difficulty",
                        title_x=0.5,
                        legend_title="Difficulty Level",
                        yaxis=dict(range=[0, 5])  # Ensure difficulty is between 0 and 5
                    )

                    # Display the chart
                    st.plotly_chart(fig_fixtures, use_container_width=True)
                else:
                    st.warning(f"No fixture data available for player: {player}")

    else:
        st.warning("No players selected. Please select at least one player to display data.")
            
            
    st.markdown('## Fixture Difficulty Matrix')
    st.markdown('##### ***Fixture difficulty for all teams and gameweeks***')
     

    st.markdown('<div style="text-align: center;">Gameweeks</div>', unsafe_allow_html=True)
    st.markdown("")
    # Ensure no duplicate entries exist for pivoting
    df_fixtures_2023 = df_fixtures_2023.drop_duplicates(subset=['Team', 'Gameweek'])
    df_fixtures_2023 = df_fixtures_2023[df_fixtures_2023['Gameweek'] >= 16]

    # Add Venue information to the Opponent column
    df_fixtures_2023['Opponent'] = df_fixtures_2023.apply(
        lambda x: f"{x['Opponent']} (H)" if x['Venue'] == 'Home' else f"{x['Opponent']} (A)", axis=1
    )
    # Pivot the dataframe to create a matrix format (Teams vs Gameweeks)
    fixture_matrix = df_fixtures_2023.pivot(index='Team', columns='Gameweek', values='Opponent')
# Rename the top level of the columns to "Gameweek"
    # fixture_matrix.columns = pd.MultiIndex.from_tuples([("Gameweek", col) for col in fixture_matrix.columns])
   
   
    # Define color scale for difficulty levels
    difficulty_colors = {
        2: "#5dff61 ",  # Light green for easy fixtures
        3: "#84b8ff ",  # Light blue for moderate fixtures
        4: "yellow",  # Light yellow for harder fixtures
        5: "#df0000 "   # Light red for tough fixtures
    }

        # Merge Opponent and Difficulty into a single display
    def style_matrix(row, difficulty_matrix):
        styled_row = []
        for gameweek, opponent in row.items():
            difficulty = difficulty_matrix.loc[row.name, gameweek]
            color = difficulty_colors.get(difficulty, "white")
            styled_row.append(f'background-color: {color}; color: black;')
        return styled_row

    # Create a difficulty matrix
    difficulty_matrix = df_fixtures_2023.pivot(index='Team', columns='Gameweek', values='Difficulty')

    # Apply styles to the Opponent matrix
    styled_fixture_matrix = fixture_matrix.style.apply(lambda row: style_matrix(row, difficulty_matrix), axis=1)

    # Display the styled matrix in Streamlit
    st.dataframe(styled_fixture_matrix, height=600, use_container_width=True)
        
