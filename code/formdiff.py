import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient





def perform_formdiff():

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
        x=alt.X('Total Yellow Cards', axis=alt.Axis(labelAngle=0, format='d')),
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
        x=alt.X('Total Yellow Cards', axis=alt.Axis(labelAngle=0, format='d')),
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
        x=alt.X('Total Red Cards:Q', axis=alt.Axis(labelAngle=0, format='d')),
        y=alt.Y('Player Name', sort=alt.EncodingSortField('Total Red Cards:Q'), axis=alt.Axis(labelAngle=0)),
        color=alt.Color('Position'),
        tooltip=['Player Name', 'Total Red Cards'],
        #order=alt.Order("Total Red Cards", sort="ascending"),
    ).properties(
        width=500,
    ).configure_axis(grid=False)
    
    
    top_dreamteam = df_history_2023.sort_values('Dreamteam', ascending=False)
    top_dreamteam = top_dreamteam.drop_duplicates(subset=['Player Name']).head(10)
    #top_dreamteam['Dreamteam'] = pd.to_numeric(top_10_red_cards['Total Red Cards'])
    
    # Create the altair chart
    dreamteam_chart = alt.Chart(top_dreamteam.sort_values('Dreamteam', ascending=False).reset_index(drop=True)).mark_bar().encode(
        x=alt.X('Dreamteam', axis=alt.Axis(labelAngle=0, format='d')),
        y=alt.Y('Player Name', sort=alt.EncodingSortField('Dreamteam:Q'), axis=alt.Axis(labelAngle=0)),
        color=alt.Color('Position'),
        tooltip=['Player Name', 'Dreamteam'],
        #order=alt.Order("Total Red Cards", sort="ascending"),
    ).properties(
        width=500,
    ).configure_axis(grid=False)

    # Create a multi-select widget to select the charts
    selected_charts = st.multiselect("Select Charts", ["Goalkeeper Chart", "Defender Chart", "Midfielder Chart", "Forward Chart", "Budget Player Chart", "Differential Player Chart",  "Yellow Cards Chart", "Suspension Warning Chart", "Red Cards Chart", "Dreamteam Chart"])

    # Check if the Goalkeeper Chart is selected
    if "Goalkeeper Chart" in selected_charts:
        st.markdown(f'##### ***Goalkeeper***')
        st.altair_chart(goalkeeper_chart, use_container_width=True, theme="streamlit")

    # Check if the Defender Chart is selected
    if "Defender Chart" in selected_charts:
        st.markdown(f'##### ***Defender***')
        st.altair_chart(defender_chart, use_container_width=True, theme="streamlit")

    # Check if the Midfielder Chart is selected
    if "Midfielder Chart" in selected_charts:
        st.markdown(f'##### ***Midfielder***')
        st.altair_chart(midfielder_chart, use_container_width=True, theme="streamlit")

    # Check if the Forward Chart is selected
    if "Forward Chart" in selected_charts:
        st.markdown(f'##### ***Forwards***')
        st.altair_chart(forward_chart, use_container_width=True, theme="streamlit")
    
    if "Budget Player Chart" in selected_charts:    
        st.markdown(f'### Top Eleven In-Form Budget Players')
        st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Budget Price***')
        st.markdown(f'##### ***:green[Goalkeeper < $5.0]***')
        st.markdown(f'##### ***:green[Defender < $5.0]***')
        st.markdown(f'##### ***:green[Midfielder < $6.0]***')
        st.markdown(f'##### ***:green[Forward < $6.5]***')
        st.altair_chart(price_chart, use_container_width=True, theme="streamlit")
        
    if "Differential Player Chart" in selected_charts:    
        st.markdown(f'### Top Eleven In-Form Differential Players')
        st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Selected By Lower Than 10%***')
        st.markdown(f'##### ***Value of Selected By Subject To Change***')
        st.altair_chart(diff_chart, use_container_width=True, theme="streamlit")

    # Check if the Yellow Cards Chart is selected
    if "Yellow Cards Chart" in selected_charts:
        st.markdown(f'### Yellow Cards Record')
        st.altair_chart(yc_chart, use_container_width=True, theme="streamlit")

    # Check if the Red Cards Chart is selected
    if "Suspension Warning Chart" in selected_charts:
        st.markdown(f'### Suspension Warning')
        st.altair_chart(yc_warn_chart, use_container_width=True, theme="streamlit")
        
    # Check if the Red Cards Chart is selected
    if "Red Cards Chart" in selected_charts:
        st.markdown(f'### Red Cards Record')
        st.altair_chart(rc_chart, use_container_width=True, theme="streamlit")
    
       # Check if the Red Cards Chart is selected
    if "Dreamteam Chart" in selected_charts:
        st.markdown(f'### Dreamteam')
        st.altair_chart(dreamteam_chart, use_container_width=True, theme="streamlit")
    
    # # Display the bar chart figures
    # st.markdown(f'##### ***Goalkeeper***')
    # st.altair_chart(goalkeeper_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'##### ***Defender***')
    # st.altair_chart(defender_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'##### ***Midfielder***')
    # st.altair_chart(midfielder_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'##### ***Forwards***')
    # st.altair_chart(forward_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'### Top Eleven In-Form Differential Players')
    # st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Selected By Lower Than 10%***')
    # st.markdown(f'##### ***Value of Selected By Subject To Change***')
    
    
    # st.altair_chart(diff_chart, use_container_width=True, theme="streamlit")
    
    # st.markdown(f'### Top Eleven In-Form Budget Players')
    # st.markdown(f'##### ***Top Performer Player For Last 3 Gameweeks With Budget Price***')
    # st.markdown(f'##### ***:green[Goalkeeper < $5.0]***')
    # st.markdown(f'##### ***:green[Defender < $5.0]***')
    # st.markdown(f'##### ***:green[Midfielder < $6.0]***')
    # st.markdown(f'##### ***:green[Forward < $6.5]***')
    # st.altair_chart(price_chart, use_container_width=True, theme="streamlit")
    
    # st.markdown(f'### Yellow Cards Record')
    # st.altair_chart(yc_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'### Suspension Warning')
    # st.altair_chart(yc_warn_chart, use_container_width=True, theme="streamlit")
    # st.markdown(f'### Red Cards Record')
    # st.altair_chart(rc_chart, use_container_width=True, theme="streamlit")
