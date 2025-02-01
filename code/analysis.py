import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import altair as alt
import plotly.express as px
import plotly.io as pio
from st_aggrid import AgGrid, GridOptionsBuilder
import numpy as np


# Define the function for the "Analysis" process
def perform_analysis():
    # Fetch the data using cache
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
    collection_player = db["player"]


    @st.cache_resource(show_spinner=False)
    def fetch_data_player(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    # Fetch the player data
    df_player = fetch_data_player(collection_player)
   
    
  


    st.markdown('## 24/25 Season')
    st.markdown('##### ***Filter Teams, Positions and Price***')


    # Calculate additional columns
    df_player['90s'] = df_player['Minutes Played'] / 90
    calc_elements = ['Total Goals', 'Total Assists', 'Total Points']
    for each in calc_elements:
        df_player[f'{each} P90'] = df_player[each] / df_player['90s']
    df_player = df_player.drop('90s', axis=1)
    
    # Convert to numeric, coercing errors to NaN



    # Display the main title or description
    st.markdown("### Filter Players")

    
    # Create two columns for side-by-side layout
    col1, col2, col3 = st.columns(3)

    # Place the filters in the respective columns
    with col1:
        teams = st.multiselect("Select Teams:", options=list(df_player['Team'].unique()))

    with col2:
        positions = st.multiselect("Select Positions:", options=list(df_player['Position'].unique()))

    with col3:
        price_choice = st.slider("Select Maximum Price:", min_value=4.0, max_value=15.0, step=0.5, value=15.0)



    # Apply the filters immediately based on user selection
    if teams:  # Check if teams are selected
        if positions:  # Check if positions are selected
            df_filtered_player = df_player[
                (df_player['Team'].isin(teams)) & 
                (df_player['Position'].isin(positions)) & 
                (df_player['Price'] <= price_choice)
            ]
        else:  # If no specific positions are selected, include all positions
            df_filtered_player = df_player[
                (df_player['Team'].isin(teams)) & 
                (df_player['Price'] <= price_choice)
            ]
    elif positions:  # If no teams are selected but positions are selected
        df_filtered_player = df_player[
            (df_player['Position'].isin(positions)) & 
            (df_player['Price'] <= price_choice)
        ]
    else:  # If no teams or positions are selected, show all players within price range
        df_filtered_player = df_player[df_player['Price'] <= price_choice]
        
    
        # Define custom colors for each position
    position_colors = {
        'Goalkeeper': '#04f5ff',
        'Defender': '#cc0249',
        'Midfielder': '#fa9b28',
        'Forward': '#00ff85',
    }
    
    
    
    def table_data(data, sort, key=None):
        data.reset_index(drop=True, inplace=True)

        data.index += 1  # Start index from 1
    
        # Calculate min and max for every field explicitly
        min_total_points = int(df_filtered_player["Total Points"].min())
        max_total_points = int(df_filtered_player["Total Points"].max())

        min_goal = int(df_filtered_player["Total Goals"].min())
        max_goal = int(df_filtered_player["Total Goals"].max())

        min_price = float(df_filtered_player["Price"].min())
        max_price = float(df_filtered_player["Price"].max())

        min_assists = int(df_filtered_player["Total Assists"].min())
        max_assists = int(df_filtered_player["Total Assists"].max())

        min_cs = int(df_filtered_player["Total CS"].min())
        max_cs = int(df_filtered_player["Total CS"].max())

        min_bonus = int(df_filtered_player["Total Bonus"].min())
        max_bonus = int(df_filtered_player["Total Bonus"].max())

        min_mp = int(df_filtered_player["Minutes Played"].min())
        max_mp = int(df_filtered_player["Minutes Played"].max())

        min_saves = int(df_filtered_player["Total Saves"].min())
        max_saves = int(df_filtered_player["Total Saves"].max())

        min_dreamteam = int(df_filtered_player["Dreamteam"].min())
        max_dreamteam = int(df_filtered_player["Dreamteam"].max())

        min_influence = int(df_filtered_player["Total Influence"].min())
        max_influence = int(df_filtered_player["Total Influence"].max())



        min_creativity = int(df_filtered_player["Total Creativity"].min())
        max_creativity = int(df_filtered_player["Total Creativity"].max())

        min_threat = int(df_filtered_player["Total Threat"].min())
        max_threat = int(df_filtered_player["Total Threat"].max())

        min_xg = float(df_filtered_player["Total xG"].min())
        max_xg = float(df_filtered_player["Total xG"].max())

        min_xa = float(df_filtered_player["Total xA"].min())
        max_xa = float(df_filtered_player["Total xA"].max())

    

        min_ict_index = int(df_filtered_player["Total ICT Index"].min())
        max_ict_index = int(df_filtered_player["Total ICT Index"].max())



        min_yc = int(df_filtered_player["Total YC"].min())
        max_yc = int(df_filtered_player["Total YC"].max())

        min_rc = int(df_filtered_player["Total RC"].min())
        max_rc = int(df_filtered_player["Total RC"].max())

        min_goals_p90 = int(df_filtered_player["Total Goals P90"].min())
        max_goals_p90 = int(df_filtered_player["Total Goals P90"].max())

        min_assists_p90 = int(df_filtered_player["Total Assists P90"].min())
        max_assists_p90 = int(df_filtered_player["Total Assists P90"].max())


        min_points_p90 = float(df_filtered_player["Total Points P90"].min())
        max_points_p90 = float(df_filtered_player["Total Points P90"].max())
        
        
        st.data_editor(
                    data.sort_values(sort, ascending=False).reset_index(drop=True),
                            column_config={
                        "Rank": st.column_config.NumberColumn(
                            "Rank",
                            help="Rank",
                            format="%d",
                        ),
                        "Player Name": st.column_config.TextColumn(
                            "Name",
                            help="Player Name",
                            max_chars=50,
                            validate="^st\.[a-z_]+$",
                        ),
                        "Total Points": st.column_config.ProgressColumn(
                            "Points",
                            min_value=min_total_points,
                            max_value=max_total_points,
                            help="Total Points",
                            format="%d",
                        ),
                        "Price": st.column_config.ProgressColumn(
                            "Price",
                            min_value=min_price,
                            max_value=max_price,
                            help="Player Price",
                            format="$%.2f",
                        ),
                        "Total Goals": st.column_config.ProgressColumn(
                            "Goals",
                            min_value=min_goal,
                            max_value=max_goal,
                            help="Total Goals",
                            format="%d",
                            
                        ),
                        "Total Assists": st.column_config.ProgressColumn(
                            "Assists",
                            min_value=min_assists,
                            max_value=max_assists,
                            help="Total Assists",
                            format="%d",
                            
                        ),
                        "Total CS": st.column_config.ProgressColumn(
                            "CS",
                            min_value=min_cs,
                            max_value=max_cs,
                            help="Total Clean Sheets",
                            format="%d",
                        ),
                        "Total Bonus": st.column_config.ProgressColumn(
                            "Bonus",
                            min_value=min_bonus,
                            max_value=max_bonus,
                            help="Total Bonus Points",
                            format="%d",
                        ),
                        "Minutes Played": st.column_config.ProgressColumn(
                            "MP",
                            min_value=min_mp,
                            max_value=max_mp,
                            help="Minutes Played",
                            format="%d",
                        ),
                        "Total Saves": st.column_config.ProgressColumn(
                            "Saves",
                            min_value=min_saves,
                            max_value=max_saves,
                            help="Total Saves (GK)",
                            format="%d",
                        ),
                        "Dreamteam": st.column_config.ProgressColumn(
                            "Dreamteam",
                            min_value=min_dreamteam,
                            max_value=max_dreamteam,
                            help="Total Number Of Dreamteam Selected",
                            format="%d",
                        ),
                        "Total Influence": st.column_config.ProgressColumn(
                            "Influence",
                            min_value=min_influence,
                            max_value=max_influence,
                            help="Total Influence Points",
                            format="%d",
                        ),
                        "Influence Rank": st.column_config.NumberColumn(
                            "Influence Rank",
                            help="Influence Points Rank",
                            format="%d",
                        ),
                        "Position Influence Rank": st.column_config.NumberColumn(
                            "Position Influence Rank",
                            help="Influence Points Rank Based On Position",
                            format="%d",
                        ),
                        "Total Creativity": st.column_config.ProgressColumn(
                            "Creativity",
                            min_value=min_creativity,
                            max_value=max_creativity,
                            help="Total Creativity Points",
                            format="%d",
                        ),
                        "Total Threat": st.column_config.ProgressColumn(
                            "Threat",
                            min_value=min_threat,
                            max_value=max_threat,
                            help="Total Threat Points",
                            format="%d",
                        ),
                        "Total xG": st.column_config.ProgressColumn(
                            "xG",
                            min_value=min_xg,
                            max_value=max_xg,
                            help="Total Expected Goals",
                            format="%f",
                        ),
                        "Total xA": st.column_config.ProgressColumn(
                            "xA",
                            min_value=min_xa,
                            max_value=max_xa,
                            help="Total Expected Assists",
                            format="%f",
                        ),           
                        "Creativity Rank": st.column_config.NumberColumn(
                            "Creativity Rank",
                            help="Creativity Rank",
                            format="%d",
                        ),
                        "Position Creativity Rank": st.column_config.NumberColumn(
                            "Position Creativity Rank",
                            help="Total Creativity Rank Based On Position",
                            format="%d",
                        ),
                        "Threat Rank": st.column_config.NumberColumn(
                            "Threat Rank",
                            help="Total Threat Rank",
                            format="%d",
                        ),
                        "Position Threat Rank": st.column_config.NumberColumn(
                            "Position Threat Rank",
                            help="Total Threat Rank Based On Position",
                            format="%d",
                        ),
                        "Total ICT Index": st.column_config.ProgressColumn(
                            "ICT Index",
                            min_value=min_ict_index,
                            max_value=max_ict_index,
                            help="Total ICT Index Points",
                            format="%d",
                        ),
                        "ICT Index Rank": st.column_config.NumberColumn(
                            "ICT Index Rank",
                            help="Total ICT Index Overall Rank",
                            format="%d",
                        ),
                        "Position ICT Index Rank": st.column_config.NumberColumn(
                            "Position ICT Index Rank",
                            help="Total ICT Index Rank Based On Position",
                            format="%d",
                        ),
                        "Corners/Indirect Freekick Order": st.column_config.NumberColumn(
                            "Set Piece Order",
                            help="Corners/Indirect Freekick Order",
                            format="%d",
                        ),
                        "Direct Freekick Order": st.column_config.NumberColumn(
                            "Direct FK Order",
                            help="Direct Freekick Order",
                            format="%d",
                        ),
                        "Form Rank": st.column_config.NumberColumn(
                            "Form Rank",
                            help="Form Overall Ranking",
                            format="%d",
                        ),
                        "Position Form Rank": st.column_config.NumberColumn(
                            "Position Form Rank",
                            help="Form Ranking Based On Position",
                            format="%d",
                        ),
                        "Points/Game Rank": st.column_config.NumberColumn(
                            "Points/Game Ranking",
                            help="Points Per Game Overall Ranking",
                            format="%d",
                        ),
                        "Position Points/Game Rank": st.column_config.NumberColumn(
                            "Position Points/Game Ranking",
                            help="Points Per Game Ranking Based On Position",
                            format="%d",
                        ),
                        "Total YC": st.column_config.ProgressColumn(
                            "YC",
                            min_value=min_yc,
                            max_value=max_yc,
                            help="Total Yellow Cards",
                            format="%d",
                        ),
                        "Total RC": st.column_config.ProgressColumn(
                            "RC",
                            min_value=min_rc,
                            max_value=max_rc,
                            help="Total Red Cards",
                            format="%d",
                        ),
                        "Total Goals P90": st.column_config.ProgressColumn(
                            "Goals P90",
                            min_value=min_goals_p90,
                            max_value=max_goals_p90,
                            help="Player Total Goals Per 90",
                            format="%d",
                        ),
                        "Total Assists P90": st.column_config.ProgressColumn(
                            "Assists P90",
                            min_value=min_assists_p90,
                            max_value=max_assists_p90,
                            help="Player Total Assists Per 90",
                            format="%d",
                        ),
                        "Total Points P90": st.column_config.ProgressColumn(
                            "Points P90",
                            min_value=min_points_p90,
                            max_value=max_points_p90,
                            help="Total Points Per 90",
                            format="%d",
                        ),  
                        
                        "Team": st.column_config.TextColumn(
                            "Team",
                            help="Team",
                            max_chars=50,
                            validate="^st\.[a-z_]+$",
                        ),
                        "Position": st.column_config.TextColumn(
                            "Position",
                            help="Player Position",
                            max_chars=50,
                            validate="^st\.[a-z_]+$",
                        ),   
                    },
                    hide_index=True,
                    key=key
                )
                
    
    
    
    if not df_filtered_player.empty:
        
        def display_set_piece_table(df, order_column):
            # Filter players ranked 1 in the given order column
            filtered_df = df[df[order_column] == 1.0][
                ['Player Name', 'Team', 'Total Goals', 'Total Assists', 'Position','Penalties Order', 'Corners/Indirect Freekick Order', 'Direct Freekick Order']
            ]

            # Convert the order column to integer for cleaner display
            filtered_df[order_column] = filtered_df[order_column].astype(int)

            # # Streamlit rendering for the table with auto-adjusted column widths
            # st.markdown(f'### {title}')
            columns_to_convert = ["Penalties Order", 'Corners/Indirect Freekick Order', 'Direct Freekick Order']

            # ✅ Replace NaN with 0 and infinity with finite values, then convert to integer
            filtered_df[columns_to_convert] = (
                filtered_df[columns_to_convert]
                .apply(pd.to_numeric, errors="coerce")  # Convert all to numeric (handles strings)
                .fillna(0)  # Replace NaN with 0
                .replace([float("inf"), float("-inf")], 0)  # Replace infinities with 0
                .astype(int)  # Convert to integer
            )
            filtered_df = filtered_df.reset_index(drop=True)
            filtered_df.index += 1  # Start index at 1
            filtered_df.index.name = "Rank"  # Rename index to "Rank"
            

            #Display the table in col2
            # col2.write(top_10_f)
            st.dataframe(
                filtered_df.style.set_table_styles(
                    [
                        {'selector': 'th', 'props': [('text-align', 'center')]},
                        {'selector': 'td', 'props': [('text-align', 'center')]},
                    ]
                )
            )

        


        
        def create_xg_xa_chart(df):
            # Define custom markers for each position
        #     position_markers = {
        #     'Goalkeeper': 'circle',
        #     'Defender': 'square',
        #     'Midfielder': 'diamond',
        #     'Forward': 'star',
        # }
            
            # Filter data for players with non-zero values in xG and xA
            df = df_filtered_player[(df_filtered_player['Total xG'] > 0) & (df_filtered_player['Total Goals'] > 0) & (df_filtered_player['Total xA'] > 0) & (df_filtered_player['Total Assists'] > 0)].sort_values(by=['Total Goals', 'Total Assists'], ascending=False).head(10)

            
            # Create subplots for xG vs Goals and xA vs Assists
            fig_xg = px.scatter(
                df,
                x="Total Goals",
                y="Total xG",
                size="Minutes Played",
                color="Position",
                #symbol="Position",
                text=df["Player Name"].apply(lambda x: f"<b>{x}</b>"),
                color_discrete_map=position_colors,
                hover_name="Player Name",
                title="Goals vs Expected Goals (xG)",
                #labels={"Total xG": "Expected Goals (xG)", "Total Goals": "Actual Goals"}
            )
            
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig_xg.update_layout(
                font_family=custom_font_family,
                font_color="white"  # Optionally, set the font color
            )
            fig_xg.update_traces(marker=dict(size=20), textfont=dict(size=14))
            # Update traces to set textposition and dodge
        
            def improve_text_position(x):

                positions = ['top center', 'bottom center', 'middle center']  # you can add more: left center ...
                return [positions[i % len(positions)] for i in range(len(x))]
        
            fig_xg.update_traces(
            
            textposition=improve_text_position(df) # Adjust text angle if needed
            )
        
            # Update the y-axis to display decimal values
            fig_xg.update_yaxes(
                tickformat=".2f",  # Format ticks as two decimal places
                # title_text=f"{category}"  # Optional: Update the y-axis title
            )

            fig_xa = px.scatter(
                df,
                x="Total Assists",
                y="Total xA",
                size="Minutes Played",
                color="Position",
                color_discrete_map=position_colors,
                text=df["Player Name"].apply(lambda x: f"<b>{x}</b>"),
                hover_name="Player Name",
                title="Expected Assists (xA) vs Assists",
            )
            custom_font_family = "Arial"
                        
            # Set the custom font for the text
            fig_xa.update_layout(
                font_family=custom_font_family,
                font_color="white"  # Optionally, set the font color
            )
            fig_xa.update_traces(marker=dict(size=20), textfont=dict(size=14))
            # Update traces to set textposition and dodge
        
            def improve_text_position(x):

                positions = ['top center', 'bottom center', 'middle center']  # you can add more: left center ...
                return [positions[i % len(positions)] for i in range(len(x))]
        
            fig_xa.update_traces(
            
            textposition=improve_text_position(df) # Adjust text angle if needed
            )
        
            # Update the y-axis to display decimal values
            fig_xa.update_yaxes(
                tickformat=".2f",  # Format ticks as two decimal places
                # title_text=f"{category}"  # Optional: Update the y-axis title
            )
            
            
            # Customize layouts
            custom_font_family = "Arial"
            fig_xg.update_layout(font_family=custom_font_family)
            fig_xa.update_layout(font_family=custom_font_family)

            return fig_xg, fig_xa
        

        
        
        
        st.markdown('### 🪄Overall Chart')
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
        def all_chart(df_filtered_player, category, tooltip):
            # Filter the data to include only the top 10 players and remove rows with null values
            df = df_filtered_player.dropna(subset=[category]).sort_values(category, ascending=False).head(10)
            # Exclude players with zero values in the specified category
            df = df[df[category] != 0]
                    
            # Create the bar chart
            fig = px.scatter(
                df,
                y=category,
                x="Price",
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text=df["Player Name"].apply(lambda x: f"<b>{x}</b>"),
                hover_name="Player Name",
                hover_data=tooltip.get(category, {})

            )
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="white",  # Optionally, set the font color
            )
            fig.update_traces(marker=dict(size=20), textfont=dict(size=14))
            # Update traces to set textposition and dodge
        
            def improve_text_position(x):
    
                positions = ['top center', 'bottom center', 'middle center']  # you can add more: left center ...
                return [positions[i % len(positions)] for i in range(len(x))]
        
            fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
            )
        
            # Update the y-axis to display decimal values
            fig.update_yaxes(
                tickformat=".0f",  # Format ticks as two decimal places
                title_text=f"{category}"  # Optional: Update the y-axis title
            )
            
            return fig
            


        tooltip = {
        "Total Points": {"Player Name": True, "Team": True, "Total Points": True},
        "Total Bonus": {"Player Name": True, "Team": True, "Total Bonus": True},
        "Dreamteam": {"Player Name": True, "Team": True, "Dreamteam": True},
        "Total YC": {"Player Name": True, "Team": True, "Total YC": True},
        "Total RC": {"Player Name": True, "Team": True, "Total RC": True},

        }
        tab_points, tab_xg, tab_xa, tab_sp, tab_bonus, tab_dreamteam, tab_yc, tab_rc = st.tabs(["Points", "xG vs Goals", "xA vs Assists", "Set Piece", "Bonus", "Dreamteam", "Yellow Cards", "Red Cards"])

        with tab_points:
            fig_points = all_chart(df_filtered_player, "Total Points", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_points, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total Points', ascending=False).head(10)

            
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            
            
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)



        
        with tab_xg:
            #red_card_players = df_filtered_player[df_filtered_player["Total RC"] > 0]['Player Name'].tolist()
            fig_xg = all_chart(df_filtered_player, "Total xG", tooltip) #red_card_players)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_xg)

            
            top_10_f = top_10[["Player Name", "Team", "Total Points", 'Total Goals', 'Total xG', 'Minutes Played',  'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)


           
        with tab_xa:
            #red_card_players = df_filtered_player[df_filtered_player["Total RC"] > 0]['Player Name'].tolist()
            fig_xa = all_chart(df_filtered_player, "Total xA", tooltip) #red_card_players)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_xa)

            # Reset index and start from 1
            
            top_10_f = top_10[["Player Name", "Team", "Total Points", 'Total Assists', 'Total xA', 'Minutes Played',  'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)



            
        with tab_sp:
            #red_card_players = df_filtered_player[df_filtered_player["Total RC"] > 0]['Player Name'].tolist()
            # fig_xg = all_chart(df_filtered_player, "Total RC", tooltip) #red_card_players)
            # Create Streamlit columns for side-by-side display
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f'### Penalties')
                display_set_piece_table(df_filtered_player, 'Penalties Order')

            


            with col2:
                st.markdown(f'### Corner/Indirect FK')
                display_set_piece_table(df_filtered_player, 'Corners/Indirect Freekick Order')

            with col3:
                st.markdown(f'### Freekick')
                display_set_piece_table(df_filtered_player, 'Direct Freekick Order')

             
        with tab_bonus:
            fig_bonus = all_chart(df_filtered_player, "Total Bonus", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)
            top_10 = df_filtered_player.sort_values('Total Bonus', ascending=False).head(10)

            # Reset index and start from 1
            
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
           
            
        with tab_dreamteam:
            fig_dreamteam = all_chart(df_filtered_player, "Dreamteam", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_dreamteam, theme="streamlit", use_container_width=True)
            top_10 = df_filtered_player.sort_values('Dreamteam', ascending=False).head(10)

            # Reset index and start from 1
        
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Dreamteam", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]


            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
            
            
        with tab_yc:
            fig_yc = all_chart(df_filtered_player, "Total YC", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_yc, theme="streamlit", use_container_width=True)
            top_10 = df_filtered_player.sort_values('Total YC', ascending=False).head(10)

            # Reset index and start from 1
            
            top_10_f = top_10[["Player Name", "Team", "Total Points", 'Total YC', 'Total RC', 'Minutes Played',  'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)


        with tab_rc:
            #red_card_players = df_filtered_player[df_filtered_player["Total RC"] > 0]['Player Name'].tolist()
            fig_rc = all_chart(df_filtered_player, "Total RC", tooltip) #red_card_players)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
            top_10 = df_filtered_player.sort_values('Total YC', ascending=False).head(10)

            # Reset index and start from 1
            top_10_f = top_10[["Player Name", "Team", "Total Points", 'Total YC', 'Total RC', 'Minutes Played',  'Position']]

            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)


            
            
        st.markdown('### 🎯Offensive Chart')  
        def off_chart(df_filtered_player, category, tooltip):
            # Filter the data to include only the top 10 players and remove rows with null values
            df = df_filtered_player.dropna(subset=[category]).sort_values(category, ascending=False).head(10)
            # Exclude players with zero values in the specified category
            df = df[df[category] != 0]
                    
            # Create the bar chart
            fig = px.scatter(
                df,
                y=category,
                x="Price",
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text=df["Player Name"].apply(lambda x: f"<b>{x}</b>"),
                hover_name="Player Name",
                hover_data=tooltip.get(category, {})

            )
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="white",  # Optionally, set the font color
            )
            fig.update_traces(marker=dict(size=20), textfont=dict(size=14))
            # Update traces to set textposition and dodge
        
            def improve_text_position(x):
    
            # fix indentation 
                positions = ['top center', 'bottom center', 'middle center']  # you can add more: left center ...
                return [positions[i % len(positions)] for i in range(len(x))]
        
            fig.update_traces(
           
            textposition=improve_text_position(df) # Adjust text angle if needed
            )
        
            
            return fig

        tooltip_att = {
        "Total Goals": {"Player Name": True, "Team": True, "Total Goals": True},
        "Total Assists": {"Player Name": True, "Team": True, "Total Assists": True},
        "Total xG": {"Player Name": True, "Team": True, "Total xG": True},
        "Total Creativity": {"Player Name": True, "Team": True, "Total Creativity": True},
        "Total Influence": {"Player Name": True, "Team": True, "Total Influence": True},
        "Total ICT Index": {"Player Name": True, "Team": True, "Total ICT Index": True}
        }

        
        
        
        tab_goal, tab_assists, tab_xg, tab_creative, tab_influence, tab_ict = st.tabs(["Goals", "Assists", "xG", "Creatvity", "Influence", "ICT Index"])
 

        with tab_goal:
    # Generate the goal chart
            fig_goal = off_chart(df_filtered_player, "Total Goals", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_goal, theme="streamlit", use_container_width=True)

            # Prepare the top 10 data
            top_10 = df_filtered_player.sort_values('Total Goals', ascending=False).head(10)

            # Reset index and start from 1
    
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)

        
        with tab_assists:
            fig_assists = off_chart(df_filtered_player, "Total Assists", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_assists, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total Assists', ascending=False).head(10)
            # Reset index and start from 1

            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)


        with tab_xg:
            fig_xg = off_chart(df_filtered_player, "Total xG", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_xg, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total xG', ascending=False).head(10)

            # Reset index and start from 1

            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            # Use table_data with the top_10 DataFrame
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
            
        with tab_creative:
            fig_creative = off_chart(df_filtered_player, "Total Creativity", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_creative, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total Creativity', ascending=False).head(10)

            # Reset index and start from 1

            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]

            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)

        with tab_influence:
            fig_influence = off_chart(df_filtered_player, "Total Influence", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_influence, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total Influence', ascending=False).head(10)

            # Reset index and start from 1
       
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
            # Use table_data with the top_10 DataFrame


        with tab_ict:
            fig_ict = off_chart(df_filtered_player, "Total ICT Index", tooltip_att)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_ict, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total ICT Index', ascending=False).head(10)

            # Reset index and start from 1
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total Goals", "Total Assists", "Price", 'Total Bonus', 'Total xG', 'Total xA', 'Minutes Played', 'Total Influence', 'Total Creativity', 'Total ICT Index', 'Position']]

            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
            
                     
        st.markdown('### 🚫Defensive Chart')
        def def_chart(df_filtered_player, category, tooltip):
            # Filter the data to include only defenders and remove rows with null values in the specified category
            #df = df_filtered_player[df_filtered_player["Position"].isin(["Defender", "Goalkeeper"])].dropna(subset=[category])
            df = df_filtered_player.dropna(subset=[category]).sort_values(category, ascending=False).head(10)

            # Sort and select the top 10 players based on the specified category
            df = df.sort_values(category, ascending=False).head(10)
            
            # Exclude players with zero values in the specified category
            df = df[df[category] != 0]
            
            # Create the scatter plot
            fig = px.scatter(
                df,
                y=category,
                x="Price",
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text=df["Player Name"].apply(lambda x: f"<b>{x}</b>"),
                hover_name="Player Name",
                hover_data=tooltip.get(category, {})
            )
            
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="white",  # Optionally, set the font color
            )
            
            fig.update_traces(marker=dict(size=20), textfont=dict(size=14))
            
            def improve_text_position(x):
                positions = ['top center', 'bottom center', 'middle center']  # You can add more: left center ...
                return [positions[i % len(positions)] for i in range(len(x))]
            
            fig.update_traces(
                textposition=improve_text_position(df)  # Adjust text position if needed
            )
            
            return fig


        
        tooltip = {
        "Total CS": {"Player Name": True, "Team": True, "Total CS": True},
        "Total Saves": {"Player Name": True, "Team": True, "Total Saves": True},
        }
        
        tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

        with tab_cs:
            fig_cs = def_chart(df_filtered_player, "Total CS", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total CS', ascending=False).head(10)

            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total CS", "Total Saves", "Price", 'Total Bonus', 'Position']]
            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)
       

        with tab_saves:
            fig_saves = def_chart(df_filtered_player, "Total Saves", tooltip)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)

            top_10 = df_filtered_player.sort_values('Total Saves', ascending=False).head(10)

            # Reset index and start from 1
  
  
            top_10_f = top_10[["Player Name", "Team", "Total Points", "Total CS", "Total Saves", "Price", 'Total Bonus', 'Position']]


            top_10_f = top_10_f.reset_index(drop=True)
            top_10_f.index += 1  # Start index at 1
            top_10_f.index.name = "Rank"  # Rename index to "Rank"

            #Display the table in col2
            col2.write(top_10_f)                   
        

        # Define custom markers for each position
        position_markers = {
            'Goalkeeper': 'circle',
            'Defender': 'square',
            'Midfielder': 'diamond',
            'Forward': 'star',
        }
        
    
        st.markdown('### 🔎Per 90 Stats')
        
        tab_p90, tab_g90= st.tabs(["Points/90", "Goals/90"])


        with tab_p90:
            st.markdown('##### ***Player Total Points per 90 Minutes***') 
            def points_p90_chart(df_filtered_player):


                # Create the scatter plot
                fig = px.scatter(
                    df_filtered_player,
                    y="Total Points",
                    x="Price",
                    color="Position",
                    color_discrete_map=position_colors,
                    symbol="Position",
                    symbol_map=position_markers,
                    hover_name="Player Name",
                )
                custom_font_family = "Arial"

                # Set the custom font for the text
                fig.update_layout(
                    font_family=custom_font_family,
                    font_color="white",  # Optionally, set the font color
                )

                return fig



            # Create the scatter plot with differentiated position markers and colors
            fig_cost_price = points_p90_chart(df_filtered_player)

            # Display the scatter plot using Streamlit
            st.plotly_chart(fig_cost_price, theme="streamlit", use_container_width=True)
        
        with tab_g90:
            
            st.markdown('##### ***Player Total Goals per 90 Minutes***')
            
            def goals_p90_chart(df_filtered_player):


                # Create the scatter plot
                fig = px.scatter(
                    df_filtered_player,
                    y="Total Goals",
                    x="Price",
                    color="Position",
                    color_discrete_map=position_colors,
                    symbol="Position",
                    symbol_map=position_markers,
                    hover_name="Player Name",
                    # Set custom colors and markers for each position
                    #text_auto=True,
                    #text="Team"
                )
                custom_font_family = "Arial"

                # Set the custom font for the text
                fig.update_layout(
                    font_family=custom_font_family,
                    font_color="white",  # Optionally, set the font color
                )

                return fig



            # Create the scatter plot with differentiated position markers and colors
            fig_goals_price = goals_p90_chart(df_filtered_player)

            # Display the scatter plot using Streamlit
            st.plotly_chart(fig_goals_price, theme="streamlit", use_container_width=True)

    
    st.markdown('### ℹ️Overall Table')
    df_filtered_player = df_filtered_player.sort_values('Total Points', ascending=False)
    df_filtered_player = df_filtered_player.reset_index(drop=True)
    df_filtered_player.index += 1  # Start index at 1
    df_filtered_player.index.name = "Rank"  # Rename index to "Rank"
    
    st.dataframe(df_filtered_player)
    # table_data(df_filtered_player, key='z', sort='Total Points')
 
