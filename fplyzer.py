import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Analysis", "Player Data"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)




st.title(f"Fantasy Football 2022/2023 Analysis")

if selected == "Analysis":
    
    df_player = pd.read_csv('fpl_data-update-1.csv')
    df_player.drop(['Unnamed: 0'], axis=1, inplace=True)



    df_player['90s'] = df_player['minutes']/90
    calc_elements = ['goals_scored', 'assists', 'total_points']
    for each in calc_elements:
        df_player[f'{each}_p90'] = df_player[each] / df_player['90s']


    teams = list(df_player['team'].drop_duplicates())
    teams_choice = st.sidebar.multiselect("Teams:", teams, default=teams)



    positions = list(df_player['position'].drop_duplicates())
    position_choice = st.sidebar.multiselect(
    'Choose position:', positions, default=positions)

    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=.5, value=15.0)


    df_player = df_player[df_player['position'].isin(position_choice)]
    df_player = df_player[df_player['team'].isin(teams_choice)]
    df_player = df_player[df_player['now_cost'] < price_choice]


    st.markdown('### Player Overall Data', 
                unsafe_allow_html=True)
    st.dataframe(df_player.sort_values('total_points',
                 ascending=False).reset_index(drop=True))

    st.markdown('### Cost vs 22/23 Points')
    st.vega_lite_chart(df_player, {
         'mark': {'type': 'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'now_cost', 'type': 'quantitative'},
             'y': {'field': 'total_points', 'type': 'quantitative'},
             'color': {'field': 'position', 'type': 'nominal'},
             'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'now_cost', 'type': 'quantitative'}, {'field': 'total_points', 'type': 'quantitative'}],
         },
         'width': 700,
         'height': 400,
     })

    #This is our header
    st.markdown('### Goals and Assists per 90')
    st.vega_lite_chart(df_player, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'goals_scored_p90', 'type': 'quantitative'},
         'y': {'field': 'assists_p90', 'type': 'quantitative'},
         'color': {'field': 'position', 'type': 'nominal'},
         'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'now_cost', 'type': 'quantitative'}, {'field': 'total_points', 'type': 'quantitative'}],
     },
     'width': 700,
     'height': 400,
     })

else:
    df_history_2023 = pd.read_csv('all_history_2023_df-merge-20230505.csv', usecols=lambda column: column != 'Unnamed: 0.1')
    df_history_2023.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_fixtures_2023 = pd.read_csv('all_fixtures_2023_merge_df.csv')
    df_fixtures_2023.drop(['Unnamed: 0.1'], axis=1, inplace=True)
    df_fixtures_2023 = df_fixtures_2023.sort_values(by='gameweek')
    

    players_fixtures = list(df_fixtures_2023['player_name'].drop_duplicates())
    players_fixtures.sort()


    players = list(df_history_2023['player_name'].drop_duplicates())
    players.sort()
    player_choice = st.sidebar.multiselect('Choose player:', players)
    df_history_2023 = df_history_2023[df_history_2023['player_name'].isin(player_choice)]
    df_fixtures_2023 = df_fixtures_2023[df_fixtures_2023['player_name'].isin(player_choice)]


    st.markdown('### Player Performance', 
            unsafe_allow_html=True)
    st.dataframe(df_history_2023.sort_values('game_points',
             ascending=False).reset_index(drop=True))
    st.markdown('### Player Next Fixture', 
            unsafe_allow_html=True)
    st.dataframe(df_fixtures_2023.sort_values('team',
             ascending=True).reset_index(drop=True))
    st.markdown('### Season Performance')
    c = alt.Chart(df_history_2023).mark_bar().encode(
    x='opponent_team',
    y=alt.Y('game_points'),  
    color=alt.Color('venue', scale=alt.Scale(domain=['Home', 'Away'], range=['red', 'blue'])),
    tooltip=['gameweek','game_points','match_goals_scored', 'game_assists', 'game_bonus']
    )

    st.altair_chart(c, use_container_width=True, theme="streamlit")



    st.markdown('### Season Fixtures')
    color_scale = alt.Scale(domain=[5, 4, 3, 2], range=['red', 'blue', 'yellow', 'green'])
    d = alt.Chart(df_fixtures_2023).mark_bar().encode(
    x=alt.X('opponent', sort=alt.EncodingSortField('gameweek')),
    y=alt.Y('difficulty'),
    color=alt.Color('difficulty', scale=color_scale),
    tooltip=['gameweek','player_name', 'opponent', 'difficulty']
    ).interactive()

    st.altair_chart(d, use_container_width=True, theme="streamlit")
