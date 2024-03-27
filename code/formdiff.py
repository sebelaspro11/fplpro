import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import plotly.express as px
import plotly.graph_objects as go
import numpy as np





def perform_formdiff():

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
    
    
    
    @st.cache_resource(show_spinner=False)
    def fetch_data_history(_collect):
    # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    df_history_2023 = fetch_data_history(collection_details)

    #df_history_2023['Selected By(%)'] = df_history_2023['Selected By(%)'] + '%'

    # Apply the custom formatting function to the 'Percentage' column
    # df_history_2023['Selected By(%)'] = df_history_2023['Selected By(%)'].apply(add_percent_symbol)

    
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
    
    gk_bonus = goalkeepers[goalkeepers['Availability'] == 'a'].sort_values(['Last 3 GW Bonus Points', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)
    def_bonus = defenders[defenders['Availability'] == 'a'].sort_values(['Last 3 GW Bonus Points', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)
    mid_bonus = midfielders[midfielders['Availability'] == 'a'].sort_values(['Last 3 GW Bonus Points', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)
    fwd_bonus = forwards[forwards['Availability'] == 'a'].sort_values(['Last 3 GW Bonus Points', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xG', 'Last 3 GW xA'], ascending=False)

    def_xg = defenders[defenders['Availability'] == 'a'].sort_values([ 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xA', 'Last 3 GW Bonus Points'], ascending=False)
    mid_xg = midfielders[midfielders['Availability'] == 'a'].sort_values(['Last 3 GW xG', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xA', 'Last 3 GW Bonus Points'], ascending=False)
    fwd_xg = forwards[forwards['Availability'] == 'a'].sort_values(['Last 3 GW xG', 'Last 3 GW Points', 'Last 3 GW Goals', 'Last 3 GW Assists', 'Last 3 GW xA', 'Last 3 GW Bonus Points'], ascending=False)
    
    
    # Select top players for each position
    gk_top = gk_top.head(10).drop_duplicates(subset=['Player Name'])
    def_top = def_top.head(10).drop_duplicates(subset=['Player Name'])
    mid_top = mid_top.head(10).drop_duplicates(subset=['Player Name'])
    fwd_top = fwd_top.head(10).drop_duplicates(subset=['Player Name'])
    bonus_top = bonus_top.head(10).drop_duplicates(subset=['Player Name'])
    gk_diff = gk_diff.head(10).drop_duplicates(subset=['Player Name'])
    def_diff = def_diff.head(10).drop_duplicates(subset=['Player Name'])
    mid_diff = mid_diff.head(10).drop_duplicates(subset=['Player Name'])
    fwd_diff = fwd_diff.head(10).drop_duplicates(subset=['Player Name'])
    gk_price = gk_price.head(10).drop_duplicates(subset=['Player Name'])
    def_price = def_price.head(10).drop_duplicates(subset=['Player Name'])
    mid_price = mid_price.head(10).drop_duplicates(subset=['Player Name'])
    fwd_price = fwd_price.head(10).drop_duplicates(subset=['Player Name'])
    
    gk_bonus = gk_bonus.head(10).drop_duplicates(subset=['Player Name'])
    def_bonus = def_bonus.head(10).drop_duplicates(subset=['Player Name'])
    mid_bonus = mid_bonus.head(10).drop_duplicates(subset=['Player Name'])
    fwd_bonus = fwd_bonus.head(10).drop_duplicates(subset=['Player Name'])
    
    def_xg = def_xg.head(10).drop_duplicates(subset=['Player Name'])
    mid_xg = mid_xg.head(10).drop_duplicates(subset=['Player Name'])
    fwd_xg = fwd_xg.head(10).drop_duplicates(subset=['Player Name'])

    # Concatenate selected players into a final DataFrame
    selected_players = pd.concat([gk_top, def_top, mid_top, fwd_top])
    diff_players = pd.concat([gk_diff, def_diff, mid_diff, fwd_diff])
    price_players = pd.concat([gk_price, def_price, mid_price, fwd_price])

    
    st.markdown(f'### In-Form Player Based On The Last 3 Gameweeks')
    # st.markdown(f'##### ***Top Player For Every Position***')
    st.markdown(f'##### ****Points****')
    

    # def perform_chart(df_perform_player, category, tooltip):

    #             # Define custom colors for each position
    #     position_colors = {
    #         'Goalkeeper': '#04f5ff',
    #         'Defender': '#cc0249',
    #         'Midfielder': '#fa9b28',
    #         'Forward': '#00ff85',
    #     }
    #     # Filter the data to include only the top 5 players
    #     #df = df_perform_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
        
    #     df = df_perform_player.sort_values('Last 3 GW Points', ascending=False).reset_index(drop=True).head(10)

        
    #     # Create the bar chart
    #     fig = px.bar(
    #         df,
    #         x=category,
    #         y="Last 3 GW Points",
    #         color="Position",
    #         color_discrete_map=position_colors,  # Set custom colors for each position
    #         text="Team",
    #         hover_name="Player Name",
    #         hover_data=tooltip.get(category, {})

    #     )
    #     custom_font_family = "Arial"
        
    #     # Set the custom font for the text
    #     fig.update_layout(
    #         font_family=custom_font_family,
    #         font_color="black",  # Optionally, set the font color
    #     )
    #     fig.update_yaxes( showgrid=False)
    #     fig.update_xaxes(showgrid=False)
    #     # Adjust the text properties for the 'Team' labels
    #     fig.update_traces(
    #         texttemplate="%{text}",
    #         textposition="inside",
    #         textfont=dict(family=custom_font_family, color="black"),
    #     )
        
        
    #     return fig
  
    #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
    def perform_chart(df_perform_player, category, tooltip):

    #Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#04f5ff',
            'Defender': '#cc0249',
            'Midfielder': '#fa9b28',
            'Forward': '#00ff85',
        }
        
        # Filter the data to include only the top 5 players
        df = df_perform_player.sort_values('Last 3 GW Points', ascending=False).reset_index(drop=True).head(10)
        # Create the scatter plot
        fig = px.scatter(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Team",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Player Name",
            hover_name="Player Name",
            hover_data=tooltip.get("Player Name", {}),
            size=[10] * len(df),
        )
        custom_font_family = "Arial"

        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="white",  # Optionally, set the font color
        )

      # Update traces to set textposition and dodge
        
        def improve_text_position(x):
    
            # fix indentation 
            positions = ['top center', 'bottom center', 'middle center']  # you can add more: left center ...
            return [positions[i % len(positions)] for i in range(len(x))]
        
        fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
        )
        
        
        fig.update_yaxes(range=[min(df['Last 3 GW Points']) - 5, max(df['Last 3 GW Points']) + 5])

        selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]

        #st.write(df_perform_player[selected_columns])

        return fig




    
    def diff_chart(df_diff_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#04f5ff',
            'Defender': '#cc0249',
            'Midfielder': '#fa9b28',
            'Forward': '#00ff85',
        }
        # Filter the data to include only the top 5 players
        #df = df_perform_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
        
        df = df_diff_player.sort_values('Last 3 GW Points', ascending=False).reset_index(drop=True).head(10)

        df['Selected By(%)'] = df['Selected By(%)'].astype(str) + '%'
        # Create the bar chart
        # Create the scatter plot
        fig = px.scatter(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Team",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Player Name",
            hover_name="Player Name",
            hover_data=tooltip.get("Player Name", {}),
            size=[10] * len(df),
        )
        custom_font_family = "Arial"

        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="white",  # Optionally, set the font color
        )
        def improve_text_position(x):
    
            # fix indentation 
            positions = ['top center', 'bottom center', 'middle center']   # you can add more: left center ...
            return [positions[i % len(positions)] for i in range(len(x))]
        
        fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
        )
        
        fig.update_yaxes(range=[min(df['Last 3 GW Points']) - 5, max(df['Last 3 GW Points']) + 5])
        
        
        return fig
    
    
    def price_chart(df_price_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#04f5ff',
            'Defender': '#cc0249',
            'Midfielder': '#fa9b28',
            'Forward': '#00ff85',
        }
            # Filter the data to include only the top 5 players
        #df = df_perform_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
        
        df = df_price_player.sort_values('Last 3 GW Points', ascending=False).reset_index(drop=True).head(10)

        #df['Price'] = '£' + df['Price'].astype(str)
        # Create the bar chart
        fig = px.scatter(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Team",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Player Name",
            hover_name="Player Name",
            hover_data=tooltip.get("Player Name", {}),
            size=[10] * len(df),
        )
        custom_font_family = "Arial"

        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="white",  # Optionally, set the font color
        )
        def improve_text_position(x):
    
            # fix indentation 
            positions = ['top center', 'bottom center', 'middle center']   # you can add more: left center ...
            return [positions[i % len(positions)] for i in range(len(x))]
        
        fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
        )
        
        fig.update_yaxes(range=[min(df['Last 3 GW Points']) - 5, max(df['Last 3 GW Points']) + 5])
        
        
        return fig
        
    
    
    
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
    def bonus_chart(df_bonus_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#04f5ff',
            'Defender': '#cc0249',
            'Midfielder': '#fa9b28',
            'Forward': '#00ff85',
        }
        # Filter the data to include only the top 5 players
        df = df_bonus_player.sort_values('Last 3 GW Bonus Points', ascending=False).reset_index(drop=True).head(10)
        
        # Create the bar chart
        fig = px.scatter(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Team",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Player Name",
            hover_name="Player Name",
            hover_data=tooltip.get("Player Name", {}),
            size=[10] * len(df),
        )
        custom_font_family = "Arial"

        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="white",  # Optionally, set the font color
        )
        def improve_text_position(x):
    
            # fix indentation 
            positions = ['top center', 'bottom center', 'middle center']   # you can add more: left center ...
            return [positions[i % len(positions)] for i in range(len(x))]
        
        fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
        )
        
        fig.update_yaxes(range=[min(df['Last 3 GW Points']) - 5, max(df['Last 3 GW Points']) + 5])
        
        
        return fig
    
    
    
    def xg_chart(df_xg_player, category, tooltip):

                # Define custom colors for each position
        position_colors = {
            'Goalkeeper': '#04f5ff',
            'Defender': '#cc0249',
            'Midfielder': '#fa9b28',
            'Forward': '#00ff85',
        }
        # Filter the data to include only the top 5 players
        df = df_xg_player.sort_values('Last 3 GW xG', ascending=False).reset_index(drop=True).head(10)
        df['text'] = df['Player Name'] + '<br>Last 3 GW xG: ' + df['Last 3 GW xG'].astype(str)

        # Create the bar chart
        fig = px.scatter(
            df,
            x=category,
            y="Last 3 GW Points",
            color="Team",
            color_discrete_map=position_colors,  # Set custom colors for each position
            text="Player Name",
            hover_name="Player Name",
            hover_data=tooltip.get("Player Name", {}),
            size=[10] * len(df),


        )
    
        custom_font_family = "Arial"

        # Set the custom font for the text
        fig.update_layout(
            font_family=custom_font_family,
            font_color="white",  # Optionally, set the font color
        )
        # fig.update_traces(
        # textposition="top center"  # Set the desired text position here
        # )
        
        def improve_text_position(x):
    
            # fix indentation 
            positions = ['top center', 'bottom center', 'middle center']   # you can add more: left center ...
            return [positions[i % len(positions)] for i in range(len(x))]
        
        fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
        )
        
        fig.update_yaxes(range=[min(df['Last 3 GW Points']) - 5, max(df['Last 3 GW Points']) + 5])
        
        
        return fig



    tooltip_gk = {
    "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Saves": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Bonus Points": True},
    }

    tooltip_def = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }

    tooltip_mid = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True}
    }

    tooltip_fwd = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }

    tooltip_diff_gk = {
    "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Selected By(%)": True, "Last 3 GW Saves": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Bonus Points": True},
    }
    tooltip_diff_def = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }
    tooltip_diff_mid_fwd = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }


    tooltip_price_gk = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Price": True,  "Last 3 GW Saves": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Bonus Points": True},
    }
    tooltip_price_def = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Price": True, "Last 3 GW Clean Sheets": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }
    tooltip_price_mid_fwd = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Price": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True, "Last 3 GW Bonus Points": True},
    }
    
    tooltip_bonus_gk = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Bonus Points": True,  "Last 3 GW Saves": True, "Last 3 GW Clean Sheets": True},
    }
    
    tooltip_bonus_def = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Bonus Points": True,  "Last 3 GW Clean Sheets": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }
    tooltip_bonus_mid_fwd = {
        "Player Name": {"Player Name": True, "Team": True, "Last 3 GW Points": True, "Last 3 GW Bonus Points": True, "Price": True, "Last 3 GW Goals": True, "Last 3 GW Assists": True},
    }
    
    tab_gk, tab_def, tab_mid, tab_fwd = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward"])
    #tab_gk, tab_def, tab_mid, tab_fwd, tab_diff, tab_price, tab_bonus = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward", "Differential", "Budget", "Bonus"])

    selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

    with tab_gk:
        fig_gk = perform_chart(gk_top, "Price", tooltip_diff_gk)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_gk, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = gk_top[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_def:
        fig_def = perform_chart(def_top, "Price", tooltip_diff_def)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_def, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = def_top[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
        
    with tab_mid:
        fig_mid = perform_chart(mid_top, "Price", tooltip_diff_mid_fwd)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_mid, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = mid_top[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1
        # Display the selected columns in col2
        col2.write(df_selected_columns)

    with tab_fwd:
        fig_fwd = perform_chart(fwd_top, "Price", tooltip_diff_mid_fwd)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_fwd, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = fwd_top[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)

        

    
    st.markdown(f'##### ***Differential***')
    st.markdown(f'##### Selected by less than 10%')


    tab_diff_gk, tab_diff_def, tab_diff_mid, tab_diff_fwd = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward"])
    
    
    with tab_diff_gk:
        fig_diff_gk = diff_chart(gk_diff, "Price", tooltip_fwd)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_diff_gk, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = gk_diff[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_diff_def:
        fig_diff_def = diff_chart(def_diff, "Price", tooltip_fwd)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_diff_def, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = def_diff[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_diff_mid:
        fig_diff_mid = diff_chart(mid_diff, "Price", tooltip_mid)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_diff_mid, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = mid_diff[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_diff_fwd:
        fig_diff_fwd = diff_chart(fwd_diff, "Price", tooltip_fwd)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_diff_fwd, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = fwd_diff[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    
    
    st.markdown(f'##### ***Budget***')
    st.markdown("GK price  <  5.0")
    st.markdown("DEF price  <  5.0")
    st.markdown("MID price  <  6.0")
    st.markdown("FWD price  <  6.5")

    tab_price_gk, tab_price_def, tab_price_mid, tab_price_fwd = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward"])
    
    
    with tab_price_gk:
        # fig_price_gk = price_chart(gk_price, "Price", tooltip_price_gk)
        # st.plotly_chart(fig_price_gk, theme="streamlit", use_container_width=True)
        fig_price_gk = price_chart(gk_price, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_price_gk, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = gk_price[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_price_def:
        fig_price_def = price_chart(def_price, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_price_def, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = def_price[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_price_mid:
        fig_price_mid = price_chart(mid_price, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_price_mid, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = mid_price[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_price_fwd:
        fig_price_fwd = price_chart(fwd_price, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_price_fwd, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = fwd_price[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
        
        
    st.markdown(f'##### ***Bonus***')
    st.markdown("##### Player Bonus Points ")

    tab_bonus_gk, tab_bonus_def, tab_bonus_mid, tab_bonus_fwd = st.tabs(["Goalkeeper", "Defender", "Midfielder", "Forward"])
    
    with tab_bonus_gk:
        fig_bonus_gk = bonus_chart(gk_bonus, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Total Saves", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_bonus_gk, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = gk_bonus[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_bonus_def:
        fig_bonus_def = bonus_chart(def_bonus, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_bonus_def, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = def_bonus[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_bonus_mid:
        fig_bonus_mid = bonus_chart(mid_bonus, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_bonus_mid, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = mid_bonus[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_bonus_fwd:
        fig_bonus_fwd = bonus_chart(fwd_bonus, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xG", "Last 3 GW xA"]

        col1.plotly_chart(fig_bonus_fwd, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = fwd_bonus[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    
    
    
    st.markdown(f'##### ***xG***')
    st.markdown(f'##### Player Expected Goals')

    tab_xg_def, tab_xg_mid, tab_xg_fwd = st.tabs(["Defender", "Midfielder", "Forward"])
    
    with tab_xg_def:
        fig_xg_def = xg_chart(def_xg, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xA"]

        col1.plotly_chart(fig_xg_def, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = def_xg[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_xg_mid:
        fig_xg_mid = xg_chart(mid_xg, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xA"]

        col1.plotly_chart(fig_xg_mid, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = mid_xg[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
    with tab_xg_fwd:
        fig_xg_fwd = xg_chart(fwd_xg, "Price", tooltip_gk)
        col1, col2 = st.columns(2)
        selected_columns = ["Player Name", "Team", "Price", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Selected By(%)", "Last 3 GW Bonus Points", "Last 3 GW xA"]

        col1.plotly_chart(fig_xg_fwd, use_container_width=True)
        
        # Select the columns to display
        # selected_columns = ["Player Name", "Team", "Last 3 GW Points", "Goals Scored", "Assists", "Last 3 GW xG", "Last 3 GW xA"]
        
        # Get the selected columns
        df_selected_columns = fwd_xg[selected_columns]
        df_selected_columns = df_selected_columns.reset_index(drop=True)
        df_selected_columns.index += 1 

        # Display the selected columns in col2
        col2.write(df_selected_columns)
