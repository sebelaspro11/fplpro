import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import plotly.express as px
import plotly.graph_objects as go






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

    st.markdown(f'### Top Performer Player Based On Last Gameweeks')

    
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
    bonus_top = df1[df1['Availability'] == 'a'].sort_values(['Last 3 GW Bonus Points', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)

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
    bonus_top = bonus_top.head(5).drop_duplicates(subset=['Player Name'])
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
    


  
    #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
    def perform_chart(df_perform_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
           'Goalkeeper': '#008000',
           'Defender': '#FF4B4B',
           'Midfielder': '#ffdab9',
           'Forward': '#ffd700',
    }
        # Filter the data to include only the top 5 players
        df = df_perform_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
        
        # Create the bar chart
        fig = px.bar(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Position",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Team",
            hover_name="Player Name",
            hover_data=tooltip.get(category, {})

        )
        custom_font_family = "Arial"
        
        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="black",  # Optionally, set the font color
        )
        

        # Adjust the text properties for the 'Team' labels
        fig.update_traces(
            texttemplate="%{text}",
            textposition="inside",
            textfont=dict(family=custom_font_family, color="black"),
        )
        
        
        return fig
    
    
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
    def bonus_chart(df_bonus_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
           'Goalkeeper': '#008000',
           'Defender': '#FF4B4B',
           'Midfielder': '#ffdab9',
           'Forward': '#ffd700',
    }
        # Filter the data to include only the top 5 players
        df = df_bonus_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
        
        # Create the bar chart
        fig = px.bar(
            df,
            x=category,
            y="Last 3 GW Bonus Points",
            color="Position",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Team",
            hover_name="Player Name",
            hover_data=tooltip.get(category, {})

        )
        custom_font_family = "Arial"
        
        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="black",  # Optionally, set the font color
        )
        

        # Adjust the text properties for the 'Team' labels
        fig.update_traces(
            texttemplate="%{text}",
            textposition="inside",
            textfont=dict(family=custom_font_family, color="black"),
        )
        
        
        return fig


    tooltip_gk = {
    "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Saves": True, "Last 3 GW Clean Sheets": True},
    }

    tooltip_def = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Clean Sheets": True},
    }

    tooltip_mid = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True}
    }

    tooltip_fwd = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }

    tooltip_diff = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Selected By(%)": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }

    tooltip_price = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Price": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }
    
    tooltip_bonus = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Bonus Points": True, "Price": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }
    tab_gk, tab_def, tab_mid, tab_fwd, tab_diff, tab_price, tab_bonus = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward", "Differential", "Budget", "Bonus"])

    with tab_gk:
        fig_gk = perform_chart(gk_top, "Player Name", tooltip_gk)
        st.plotly_chart(fig_gk, theme="streamlit", use_container_width=True)
    with tab_def:
        fig_def = perform_chart(def_top, "Player Name", tooltip_def)
        st.plotly_chart(fig_def, theme="streamlit", use_container_width=True)

    with tab_mid:
        fig_mid = perform_chart(mid_top, "Player Name", tooltip_mid)
        st.plotly_chart(fig_mid, theme="streamlit", use_container_width=True)

    with tab_fwd:
        fig_fwd = perform_chart(fwd_top, "Player Name", tooltip_fwd)
        st.plotly_chart(fig_fwd, theme="streamlit", use_container_width=True)

    with tab_diff:
        fig_diff = perform_chart(diff_players, "Player Name", tooltip_diff)
        st.plotly_chart(fig_diff, theme="streamlit", use_container_width=True)
    with tab_price:
        fig_price = perform_chart(price_players, "Player Name", tooltip_price)
        st.plotly_chart(fig_price, theme="streamlit", use_container_width=True)
    with tab_bonus:
        fig_bonus = bonus_chart(bonus_top, "Player Name", tooltip_bonus)
        st.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)
    
    
        

