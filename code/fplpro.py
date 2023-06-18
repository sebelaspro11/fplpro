import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components




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
    options=["Analysis", "Points & Fixtures", "In-Form & Differential Player", "Match Prediction"],
    icons=["bi-magic", "bi-file-earmark-bar-graph-fill", "bi-capslock", "bi-bullseye"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if selected == "Analysis":
    
    df_player = pd.read_csv('data/player_update-20230526.csv')
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

    st.markdown('### Cost vs 22/23 Season Points')
    st.markdown('##### ***Identify Low Price Player With High Points Return***')
    st.vega_lite_chart(df_player, {
         'mark': {'type': 'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Price', 'type': 'quantitative'},
             'y': {'field': 'Total Points', 'type': 'quantitative'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 1000,
         'height': 400,
     })

    #This is our header
    st.markdown('### Goals per 90')
    st.markdown('##### ***Player Total Goals, Assists and Points per 90 Minutes***')
    st.vega_lite_chart(df_player, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'Total Goals P90', 'type': 'quantitative'},
         'y': {'field': 'Total Assists P90', 'type': 'quantitative'},
         'color': {'field': 'Position', 'type': 'nominal'},
         'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Goals P90', 'type': 'quantitative'}, {'field': 'Total Assists P90', 'type': 'quantitative'}, {'field': 'Total Points P90', 'type': 'quantitative'}],
     },
     'width': 1000,
     'height': 400,
     })

if selected == "Points & Fixtures":
    st.markdown('### Player Points Across 2022/2023 Season & Next Fixture Difficulty')
    st.markdown('##### ***Select Multiple Players For Comparison***')
    
    st.markdown('##### ***:arrow_backward: :arrow_backward: :arrow_backward: Select Player***')

    df_history_2023 = pd.read_csv('data/history_update-20230526.csv')
    df_fixtures_2023 = pd.read_csv('data/fixtures_update-20230526.csv')
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='Gameweek')

    players_fixtures = list(df_fixtures_2023['Player Name'].drop_duplicates())
    players_fixtures.sort()

    players = list(df_history_2023['Player Name'].drop_duplicates())
    players.sort()
    
    # Add filter column 'Position'
    positions = list(df_history_2023['Position'].drop_duplicates())
    positions.sort()
    position_choice = st.sidebar.selectbox('Choose position:', positions)
    position_filter = df_history_2023[df_history_2023['Position'] == position_choice]
    position_filter = df_history_2023[df_history_2023['Position'] == position_choice]['Player Name'].unique()

    # Create a new DataFrame called teams_filter that contains the teams in the df_history_2023 DataFrame.
    teams_filter = list(df_history_2023['Team'].drop_duplicates())

    # Use the st.sidebar.multiselect() function to create a multiselect box for teams_choice.
    teams_choice = st.sidebar.multiselect('Choose team:', teams_filter)

    # Create a new DataFrame called players_filter that contains the players who are on the selected teams and play the selected position.
    players_filter = df_history_2023[(df_history_2023['Team'].isin(teams_choice)) & (df_history_2023['Position'] == position_choice)]

    # Use the st.sidebar.multiselect() function to create a multiselect box for players_choice.
    players_choice = st.sidebar.multiselect('Choose player:', players_filter['Player Name'].unique())

    for i, player in enumerate(players_choice):
        df_history_2023_player = df_history_2023[(df_history_2023['Player Name'] == player) & (df_history_2023['Position'] == position_choice) & (df_history_2023['Team'].isin(teams_choice))]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'### {player} Match Points')
            c = alt.Chart(df_history_2023_player).mark_bar().encode(
                x='Opponent',
                y=alt.Y('Gameweek Points'),
                color=alt.Color('Venue', scale=alt.Scale(domain=['Home', 'Away'], range=['red', 'blue'])),
                tooltip=['Gameweek','Gameweek Points','Goals Scored', 'Assists', 'Bonus']
            )
            st.altair_chart(c, use_container_width=True, theme="streamlit")

        df_fixtures_2023_player = df_fixtures_2023[(df_fixtures_2023['Player Name'] == player) &  (df_fixtures_2023['Team'].isin(teams_choice))]

        with col2:
            st.markdown(f'### {player} Next Fixtures')
            color_scale = alt.Scale(domain=[5, 4, 3, 2], range=['red', 'blue', 'yellow', 'green'])
            y_limit = [0, 5]
            d = alt.Chart(df_fixtures_2023_player).mark_bar().encode(
                x=alt.X('Opponent', sort=alt.EncodingSortField('Gameweek')),
                y=alt.Y('Difficulty', axis=alt.Axis(format='d'), scale=alt.Scale(domain=y_limit)),
                color=alt.Color('Difficulty', scale=color_scale),
                tooltip=['Gameweek','Player Name', 'Opponent', 'Difficulty']
            ).interactive()

            st.altair_chart(d, use_container_width=True, theme="streamlit")

        
        
if selected == "In-Form & Differential Player":
    
    st.markdown(f'### Top Performer Player Based On Last 3 Gameweeks')
    
    df_history_2023 = pd.read_csv('data/history_update-20230526.csv')


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
    
    # Convert 'Selected By(%)' column to numeric data type
    goalkeepers['Selected By(%)'] = pd.to_numeric(goalkeepers['Selected By(%)'], errors='coerce')
    defenders['Selected By(%)'] = pd.to_numeric(defenders['Selected By(%)'], errors='coerce')
    midfielders['Selected By(%)'] = pd.to_numeric(midfielders['Selected By(%)'], errors='coerce')
    forwards['Selected By(%)'] = pd.to_numeric(forwards['Selected By(%)'], errors='coerce')
    
    
    # Sort players based on desired criteria
    gk_top = goalkeepers[goalkeepers['Availability'] == 'a'].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    def_top = defenders[defenders['Availability'] == 'a'].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA','Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Conceded','Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, False, False, False, True, True])
    mid_top = midfielders[midfielders['Availability'] == 'a'].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA'], ascending=False)
    fwd_top = forwards[forwards['Availability'] == 'a'].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Assists', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA'], ascending=False)
    gk_diff = goalkeepers[(goalkeepers['Availability'] == 'a') & (goalkeepers['Selected By(%)'] < 10)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    def_diff = defenders[(defenders['Availability'] == 'a') & (defenders['Selected By(%)'] < 10)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    mid_diff = midfielders[(midfielders['Availability'] == 'a') & (midfielders['Selected By(%)'] < 10)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    fwd_diff = forwards[(forwards['Availability'] == 'a') & (forwards['Selected By(%)'] < 10)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])

    
    max_goalkeeper_price = 5.0
    max_defender_price = 5.0
    max_midfielder_price = 6.0
    max_forward_price = 6.5
    
    gk_price = goalkeepers[(goalkeepers['Availability'] == 'a') & (goalkeepers['Price'] < max_goalkeeper_price)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    def_price = defenders[(defenders['Availability'] == 'a') & (defenders['Price'] < max_defender_price)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    mid_price = midfielders[(midfielders['Availability'] == 'a') & (midfielders['Price'] < max_midfielder_price)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    fwd_price = forwards[(forwards['Availability'] == 'a') & (forwards['Price'] < max_forward_price)].sort_values(['Last 3 Gameweek Points', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded'], ascending=[False, False, False, False, True, True])
    
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
    
    # Create separate bar chart figures for each position
    goalkeeper_chart = alt.Chart(gk_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Team'),
        tooltip=['Last 3 Gameweek Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Saves', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded']
    ).interactive()

    defender_chart = alt.Chart(def_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Team'),
        tooltip=['Last 3 Gameweek Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek Clean Sheets', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA', 'Last 3 Gameweek Conceded', 'Last 3 Gameweek xG Conceded']
    ).interactive()

    midfielder_chart = alt.Chart(mid_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Team'),
        tooltip=['Last 3 Gameweek Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA']
    ).interactive()

    forward_chart = alt.Chart(fwd_top).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Team'),
        tooltip=['Last 3 Gameweek Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA']
    ).interactive()
    
    diff_chart = alt.Chart(diff_players).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Position'),
        tooltip=['Team','Selected By(%)','Last 3 Gameweek Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA']
    ).interactive()
    
    price_chart = alt.Chart(price_players).mark_bar().encode(
        x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek')),
        y=alt.Y('Last 3 Gameweek Points'),
        color=alt.Color('Position'),
        tooltip=['Team','Price','Last 3 Gameweek Points', 'Last 3 Gameweek Goals', 'Last 3 Gameweek Bonus Points', 'Last 3 Gameweek xG', 'Last 3 Gameweek xA']
    ).interactive()

    # Display the bar chart figures
    st.markdown(f'##### ***Goalkeeper***')
    st.altair_chart(goalkeeper_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Defender***')
    st.altair_chart(defender_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Midfielder***')
    st.altair_chart(midfielder_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'##### ***Forwards***')
    st.altair_chart(forward_chart, use_container_width=True, theme="streamlit")
    st.markdown(f'### In-Form Differential Players Based On Position')
    st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Selected By Lower Than 10%***')
    st.markdown(f'##### ***Value of Selected By Subject To Change***')
    
    
    st.altair_chart(diff_chart, use_container_width=True, theme="streamlit")
    
    st.markdown(f'### In-Form Budget Players Based On Position')
    st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Budget Price***')
    st.markdown(f'##### ***:green[Goalkeeper < $5.0]***')
    st.markdown(f'##### ***:green[Defender < $5.0]***')
    st.markdown(f'##### ***:green[Midfielder < $6.0]***')
    st.markdown(f'##### ***:green[Forward < $6.5]***')
    st.altair_chart(price_chart, use_container_width=True, theme="streamlit")


    
if selected == "Match Prediction":
    st.markdown(f'### Match Prediction from FiveThirtyEight.com')
    st.markdown(f'##### ***Prediction For League Standings & Upcoming Matches***')
    

    # embed streamlit docs in a streamlit app
    components.iframe("https://projects.fivethirtyeight.com/soccer-predictions/premier-league/", width=1500, height=2000, scrolling=True)
