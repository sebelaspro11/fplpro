import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu

page_title = "Fantasy Football Analyzer"
page_icon = ":bar_chart:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Analysis", "Player Data", "Top Performer"],
    icons=["pencil-fill", "bar-chart-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title(f"Fantasy Football 2022/2023 Analysis")

if selected == "Analysis":
    
    df_player = pd.read_csv('data/fpl_data_update-20230518.csv')
    df_player.drop(['Unnamed: 0'], axis=1, inplace=True)



    df_player['90s'] = df_player['Minutes Played']/90
    calc_elements = ['Total Goals', 'Total Assists', 'Total Points']
    for each in calc_elements:
        df_player[f'{each} P90'] = df_player[each] / df_player['90s']
    df_player = df_player.drop('90s', axis=1)

    teams = list(df_player['Team'].drop_duplicates())
    teams_choice = st.sidebar.multiselect("Teams:", teams, default=teams)



    positions = list(df_player['Position'].drop_duplicates())
    position_choice = st.sidebar.multiselect(
    'Choose position:', positions, default=positions)

    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=.5, value=15.0)


    df_player = df_player[df_player['Position'].isin(position_choice)]
    df_player = df_player[df_player['Team'].isin(teams_choice)]
    df_player = df_player[df_player['Price'] < price_choice]


    st.markdown('### Player Overall Data', 
                unsafe_allow_html=True)
    st.dataframe(df_player.sort_values('Total Points',
                 ascending=False).reset_index(drop=True))

    st.markdown('### Cost vs 22/23 Points')
    st.vega_lite_chart(df_player, {
         'mark': {'type': 'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Price', 'type': 'quantitative'},
             'y': {'field': 'Total Points', 'type': 'quantitative'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 700,
         'height': 400,
     })

    #This is our header
    st.markdown('### Goals and Assists per 90')
    st.vega_lite_chart(df_player, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'Total Goals P90', 'type': 'quantitative'},
         'y': {'field': 'Total Assists P90', 'type': 'quantitative'},
         'color': {'field': 'Position', 'type': 'nominal'},
         'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
     },
     'width': 700,
     'height': 400,
     })

if selected == "Player Data":
    

    df_history_2023 = pd.read_csv('data/all_history_2023_merge_df-20230518.csv')
    df_fixtures_2023 = pd.read_csv('data/streamlit/fpl/all_fixtures_2023_merge_df-20230518.csv')
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

    players_fixtures = list(df_fixtures_2023['Player Name'].drop_duplicates())
    players_fixtures.sort()

    players = list(df_history_2023['Player Name'].drop_duplicates())
    players.sort()

    # Add filter column 'Position'
    positions = list(df_history_2023['Position'].drop_duplicates())
    positions.sort()
    position_choice = st.sidebar.selectbox('Choose position:', positions)

    # Filter players based on selected position
    # Define the desired order of positions
    position_order = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

    # Filter the position column based on the desired order
    position_filter = df_history_2023[df_history_2023['Position'] == position_choice]
    position_filter = position_filter.loc[position_filter['Position'].isin(position_order), 'Player Name'].unique()
    position_filter = df_history_2023[df_history_2023['Position'] == position_choice]['Player Name'].unique()

    # Select player from filtered players
    player_choice = st.sidebar.multiselect('Choose player:', position_filter)

    for i, player in enumerate(player_choice):
        df_history_2023_player = df_history_2023[(df_history_2023['Player Name'] == player) & (df_history_2023['Position'] == position_choice)]
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'## {player} Season Performance')
            c = alt.Chart(df_history_2023_player).mark_bar().encode(
                x='Opponent',
                y=alt.Y('Gameweek Points'),  
                color=alt.Color('Venue', scale=alt.Scale(domain=['Home', 'Away'], range=['red', 'blue'])),
                tooltip=['Gameweek','Gameweek Points','Goals Scored', 'Assists', 'Bonus']
            )
            st.altair_chart(c, use_container_width=True, theme="streamlit")

        df_fixtures_2023_player = df_fixtures_2023[df_fixtures_2023['Player Name'] == player]
        with col2:
            st.markdown(f'## {player} Season Fixtures')
            color_scale = alt.Scale(domain=[5, 4, 3, 2], range=['red', 'blue', 'yellow', 'green'])
            d = alt.Chart(df_fixtures_2023_player).mark_bar().encode(
                x=alt.X('Opponent', sort=alt.EncodingSortField('Gameweek')),
                y=alt.Y('Difficulty'),
                color=alt.Color('Difficulty', scale=color_scale),
                tooltip=['Gameweek','Player Name', 'Opponent', 'Difficulty']
            ).interactive()

            st.altair_chart(d, use_container_width=True, theme="streamlit")

    
if selected == "Top Performer":
    
    df_history_2023 = pd.read_csv('data/all_history_2023_merge_df-20230518.csv')


    df_history_2023['Last 3 Gameweek Goals'] = df_history_2023.groupby('Player Name')['Goals Scored'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Assists'] = df_history_2023.groupby('Player Name')['Assists'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Points'] = df_history_2023.groupby('Player Name')['Gameweek Points'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Clean Sheets'] = df_history_2023.groupby('Player Name')['Clean Sheets'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Conceded'] = df_history_2023.groupby('Player Name')['Goals Conceded'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Saves'] = df_history_2023.groupby('Player Name')['Saves'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek Bonus Points'] = df_history_2023.groupby('Player Name')['Bonus'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek xG'] = df_history_2023.groupby('Player Name')['xG'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek xA'] = df_history_2023.groupby('Player Name')['xA'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)
    df_history_2023['Last 3 Gameweek xG Conceded'] = df_history_2023.groupby('Player Name')['xG Conceded'].rolling(window=3, min_periods=1).sum().reset_index(0, drop=True)

    max_gw = df_history_2023['Gameweek'].max()
    df1 = df_history_2023[df_history_2023['Gameweek'] == max_gw]


    # Filter players based on position distribution
    goalkeepers = df1[df1['Position'] == 'Goalkeeper']
    defenders = df1[df1['Position'] == 'Defender']
    midfielders = df1[df1['Position'] == 'Midfielder']
    forwards = df1[df1['Position'] == 'Forward']

    # Sort players based on desired criteria
    goalkeepers = goalkeepers.sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded' ], ascending=False)
    defenders = defenders.sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA','Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek xG Conceded'], ascending=False)
    midfielders = midfielders.sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA'], ascending=False)
    forwards = forwards.sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA'], ascending=False)

    # Select top players for each position
    goalkeeper = goalkeepers.head(2).drop_duplicates(subset=['Player Name'])
    defenders = defenders.head(5).drop_duplicates(subset=['Player Name'])
    midfielders = midfielders.head(5).drop_duplicates(subset=['Player Name'])
    forwards = forwards.head(3).drop_duplicates(subset=['Player Name'])

    # Concatenate selected players into a final DataFrame
    selected_players = pd.concat([goalkeeper, defenders, midfielders, forwards])
    
    st.markdown(f'## Last 3 Gameweeks Performance')
    #color_scale = alt.Scale(domain=[5, 4, 3, 2], range=['red', 'blue', 'yellow', 'green'])
    d = alt.Chart(selected_players).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Position'),
        tooltip=['Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA']
    ).interactive()

    st.altair_chart(d, use_container_width=True, theme="streamlit")
