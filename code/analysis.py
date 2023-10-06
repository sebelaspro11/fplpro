import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import altair as alt
import plotly.express as px
import plotly.io as pio



# Define the function for the "Analysis" process
def perform_analysis():
    # Fetch the data using cache
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
    collection_player = db["player"]


    @st.cache_resource
    def fetch_data_player(_collect):
        # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    # Fetch the player data
    df_player = fetch_data_player(collection_player)
    
  


    st.markdown('### Player Points Across 2022/2023 Season & Next Fixture Difficulty')
    st.markdown('##### ***Select Multiple Players For Comparison***')


    # Calculate additional columns
    df_player['90s'] = df_player['Minutes Played'] / 90
    calc_elements = ['Total Goals', 'Total Assists', 'Total Points']
    for each in calc_elements:
        df_player[f'{each} P90'] = df_player[each] / df_player['90s']
    df_player = df_player.drop('90s', axis=1)

    
    # all_positions = list(df_player['Position'].drop_duplicates())
    # Sidebar filters
    teams = st.sidebar.multiselect("Teams:", list(df_player['Team'].drop_duplicates()), default=list(df_player['Team'].drop_duplicates()))
    positions = st.sidebar.multiselect("Choose position:", list(df_player['Position'].drop_duplicates()), default=list(df_player['Position'].drop_duplicates()))
    # positions = st.sidebar.multiselect("Choose position:", [all_positions] + list(df_player['Position'].drop_duplicates()), default=[all_positions])
    # if all_positions in positions:
    #     filtered_df = df_player  # No position filtering
    # else:
    #     filtered_df = df_player[df_player['Position'].isin(positions)]  # Filter based on selected positions
    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=0.5, value=15.0)
    show_filtered = st.sidebar.checkbox("Show filtered data", value=False)
    # Apply filters to the player data
    df_filtered_player = df_player[df_player['Position'].isin(positions) & df_player['Team'].isin(teams) & (df_player['Price'] < price_choice)]


    
        
    # Display player data
    st.markdown('### Player Overall Data', unsafe_allow_html=True)
    #st.dataframe(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True))
    
    if show_filtered:
        min_values = df_filtered_player.min()
        max_values = df_filtered_player.max()
        st.data_editor(
        df_filtered_player.sort_values('Total Points', ascending=False),
                column_config={
            "Player Name": st.column_config.TextColumn(
                "Player Name",
                help="Player Name",
                max_chars=50,
                validate="^st\.[a-z_]+$",
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
            "Price": st.column_config.NumberColumn(
                "Price",
                help="Player Price",
                format="$%.1f",
            ),
            "Total Points": st.column_config.NumberColumn(
                "Total Points",
                help="Player Total Points",
                format="%d",
            ),
            "Total Goals": st.column_config.NumberColumn(
                "Total Goals",
                help="Player Total of Goals",
                format="%d",
                
            ),
            "Total Assists": st.column_config.NumberColumn(
                "Total Assists",
                help="Player Total of Assists",
                format="%d",
                
            ),
            "Total CS": st.column_config.NumberColumn(
                "Total CS",
                help="Player Total Clean Sheets",
                format="%d",
            ),
            "Total Bonus": st.column_config.NumberColumn(
                "Total Bonus",
                help="Player Total of Bonus Points",
                format="%d",
            ),
            "Minutes Played": st.column_config.NumberColumn(
                "Minutes Played",
                help="Player Minutes Played",
                format="%d",
            ),
            "Total Saves": st.column_config.NumberColumn(
                "Total Saves",
                help="Player Total Saves (GK)",
                format="%d",
            ),
            "Dreamteam": st.column_config.NumberColumn(
                "Dreamteam",
                help="Player Total Number Of Dreamteam Selected",
                format="%d",
            ),
            "Total Influence": st.column_config.NumberColumn(
                "Total Influence",
                help="Player Total Influence Points",
                format="%d",
            ),
            "Influence Rank": st.column_config.NumberColumn(
                "Influence Rank",
                help="Player Influence Points Overall Rank",
                format="%d",
            ),
            "Position Influence Rank": st.column_config.NumberColumn(
                "Position Influence Rank",
                help="Player Influence Points Rank Based On Position",
                format="%d",
            ),
            "Total Creativity": st.column_config.NumberColumn(
                "Total Creativity",
                help="Player Total Creativity Points",
                format="%d",
            ),
            "Total Threat": st.column_config.NumberColumn(
                "Total Threat",
                help="Player Total Threat Points",
                format="%d",
            ),
            "Total xG": st.column_config.NumberColumn(
                "Total xG",
                help="Player Total Expected Goals",
                format="%d",
            ),
            "Total xA": st.column_config.NumberColumn(
                "Total xA",
                help="Player Total Expected Assists",
                format="%d",
            ),           
            "Creativity Rank": st.column_config.NumberColumn(
                "Creativity Rank",
                help="Player Total GC",
                format="%d",
            ),
            "Position Creativity Rank": st.column_config.NumberColumn(
                "Position Creativity Rank",
                help="Player Total Creativity Rank Based On Position",
                format="%d",
            ),
            "Threat Rank": st.column_config.NumberColumn(
                "Threat Rank",
                help="Player Total Threat Overall Rank",
                format="%d",
            ),
            "Position Threat Rank": st.column_config.NumberColumn(
                "Position Threat Rank",
                help="Player Total Threat Rank Based On Position",
                format="%d",
            ),
            "Total ICT Index": st.column_config.NumberColumn(
                "Total ICT Index",
                help="Player Total ICT Index Points",
                format="%d",
            ),
            "ICT Index Rank": st.column_config.NumberColumn(
                "ICT Index Rank",
                help="Player Total ICT Index Overall Rank",
                format="%d",
            ),
            "Position ICT Index Rank": st.column_config.NumberColumn(
                "Position ICT Index Rank",
                help="Player Total ICT Index Rank Based On Position",
                format="%d",
            ),
            "Corners/Indirect Freekick Order": st.column_config.NumberColumn(
                "Corners/Indirect Freekick Order",
                help="Players Corners/Indirect Freekick Order",
                format="%d",
            ),
            "Direct Freekick Order": st.column_config.NumberColumn(
                "Direct Freekick Order",
                help="Players Direct Freekick Order",
                format="%d",
            ),
            "Form Rank": st.column_config.NumberColumn(
                "Form Rank",
                help="Players Form Overall Ranking",
                format="%d",
            ),
            "Position Form Rank": st.column_config.NumberColumn(
                "Position Form Rank",
                help="Players Form Ranking Based On Position",
                format="%d",
            ),
            "Points/Game Rank": st.column_config.NumberColumn(
                "Points/Game Ranking",
                help="Players Points Per Game Overall Ranking",
                format="%d",
            ),
            "Position Points/Game Rank": st.column_config.NumberColumn(
                "Position Points/Game Ranking",
                help="Players Points Per Game Ranking Based On Position",
                format="%d",
            ),
            "Total YC": st.column_config.NumberColumn(
                "Total YC",
                help="Player Total Yellow Cards",

                format="%d",
            ),
            "Total RC": st.column_config.NumberColumn(
                "Total RC",
                help="Player Total Red Cards",

                format="%d",
            ),
            "Total Goals P90": st.column_config.NumberColumn(
                "Total Goals P90",
                help="Player Total Goals Per 90",
                format="%d",
            ),
            "Total Assists P90": st.column_config.NumberColumn(
                "Total Assists P90",
                help="Player Total Assists Per 90",
                format="%d",
            ),
            "Total Points P90": st.column_config.NumberColumn(
                "Total Points P90",
                help="Player Total Points Per 90",
                format="%d",
            ),   
        },
        hide_index=True,
    )
    else:
        st.data_editor(
        df_player.sort_values('Total Points', ascending=False).reset_index(drop=True),
                column_config={
            "Index": st.column_config.TextColumn(
                "Index",
                help="Player Name",
                max_chars=50,
                validate="^st\.[a-z_]+$",
            ),
            "Player Name": st.column_config.TextColumn(
                "Player Name",
                help="Player Name",
                max_chars=50,
                validate="^st\.[a-z_]+$",
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
            "Price": st.column_config.NumberColumn(
                "Price",
                help="Player Price",
                format="$%.1f",
            ),
            "Total Points": st.column_config.NumberColumn(
                "Total Points",
                help="Player Total Points",
                format="%d",
            ),
            "Total Goals": st.column_config.NumberColumn(
                "Total Goals",
                help="Player Total of Goals",
                format="%d",
                
            ),
            "Total Assists": st.column_config.NumberColumn(
                "Total Assists",
                help="Player Total of Assists",
                format="%d",
                
            ),
            "Total CS": st.column_config.NumberColumn(
                "Total CS",
                help="Player Total Clean Sheets",
                format="%d",
            ),
            "Total Bonus": st.column_config.NumberColumn(
                "Total Bonus",
                help="Player Total of Bonus Points",
                format="%d",
            ),
            "Minutes Played": st.column_config.NumberColumn(
                "Minutes Played",
                help="Player Minutes Played",
                format="%d",
            ),
            "Total Saves": st.column_config.NumberColumn(
                "Total Saves",
                help="Player Total Saves (GK)",
                format="%d",
            ),
            "Dreamteam": st.column_config.NumberColumn(
                "Dreamteam",
                help="Player Total Number Of Dreamteam Selected",
                format="%d",
            ),
            "Total Influence": st.column_config.NumberColumn(
                "Total Influence",
                help="Player Total Influence Points",
                format="%d",
            ),
            "Influence Rank": st.column_config.NumberColumn(
                "Influence Rank",
                help="Player Influence Points Overall Rank",
                format="%d",
            ),
            "Position Influence Rank": st.column_config.NumberColumn(
                "Position Influence Rank",
                help="Player Influence Points Rank Based On Position",
                format="%d",
            ),
            "Total Creativity": st.column_config.NumberColumn(
                "Total Creativity",
                help="Player Total Creativity Points",
                format="%d",
            ),
            "Total Threat": st.column_config.NumberColumn(
                "Total Threat",
                help="Player Total Threat Points",
                format="%d",
            ),
            "Total xG": st.column_config.NumberColumn(
                "Total xG",
                help="Player Total Expected Goals",
                format="%d",
            ),
            "Total xA": st.column_config.NumberColumn(
                "Total xA",
                help="Player Total Expected Assists",
                format="%d",
            ),           
            "Creativity Rank": st.column_config.NumberColumn(
                "Creativity Rank",
                help="Player Total Goals Conceded",
                format="%d",
            ),
            "Position Creativity Rank": st.column_config.NumberColumn(
                "Position Creativity Rank",
                help="Player Total Creativity Rank Based On Position",
                format="%d",
            ),
            "Threat Rank": st.column_config.NumberColumn(
                "Threat Rank",
                help="Player Total Threat Overall Rank",
                format="%d",
            ),
            "Position Threat Rank": st.column_config.NumberColumn(
                "Position Threat Rank",
                help="Player Total Threat Rank Based On Position",
                format="%d",
            ),
            "Total ICT Index": st.column_config.NumberColumn(
                "Total ICT Index",
                help="Player Total ICT Index Points",
                format="%d",
            ),
            "ICT Index Rank": st.column_config.NumberColumn(
                "ICT Index Rank",
                help="Player Total ICT Index Overall Rank",
                format="%d",
            ),
            "Position ICT Index Rank": st.column_config.NumberColumn(
                "Position ICT Index Rank",
                help="Player Total ICT Index Rank Based On Position",
                format="%d",
            ),
            "Corners/Indirect Freekick Order": st.column_config.NumberColumn(
                "Corners/Indirect Freekick Order",
                help="Players Corners/Indirect Freekick Order",
                format="%d",
            ),
            "Direct Freekick Order": st.column_config.NumberColumn(
                "Direct Freekick Order",
                help="Players Direct Freekick Order",
                format="%d",
            ),
            "Form Rank": st.column_config.NumberColumn(
                "Form Rank",
                help="Players Form Overall Ranking",
                format="%d",
            ),
            "Position Form Rank": st.column_config.NumberColumn(
                "Position Form Rank",
                help="Players Form Ranking Based On Position",
                format="%d",
            ),
            "Points/Game Rank": st.column_config.NumberColumn(
                "Points/Game Ranking",
                help="Players Points Per Game Overall Ranking",
                format="%d",
            ),
            "Position Points/Game Rank": st.column_config.NumberColumn(
                "Position Points/Game Ranking",
                help="Players Points Per Game Ranking Based On Position",
                format="%d",
            ),
            "Total YC": st.column_config.NumberColumn(
                "Total YC",
                help="Player Total Yellow Cards",
                format="%d",
            ),
            "Total RC": st.column_config.NumberColumn(
                "Total RC",
                help="Player Total Red Cards",
                format="%d",
            ),
            "Total Goals P90": st.column_config.NumberColumn(
                "Total Goals P90",
                help="Player Total Goals Per 90",
                format="%d",
            ),
            "Total Assists P90": st.column_config.NumberColumn(
                "Total Assists P90",
                help="Player Total Assists Per 90",
                format="%d",
            ),
            "Total Points P90": st.column_config.NumberColumn(
                "Total Points P90",
                help="Player Total Points Per 90",
                format="%d",
            ),   
        },
        hide_index=True,
    )
    

    

   
    
        # Define custom colors for each position
    position_colors = {
        'Goalkeeper': '#04f5ff',
        'Defender': '#cc0249',
        'Midfielder': '#fa9b28',
        'Forward': '#00ff85',
    }
    if show_filtered:
        

        
        
        st.markdown('### Offensive Chart')  
        def off_chart(df_filtered_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            #df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)

            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text="Team",
                hover_data=tooltip.get(category, {})

            )
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )
            
            return fig

        tooltip = {
        "Total Goals": {"Player Name": True, "Team": True, "Total Goals": True},
        "Total Assists": {"Player Name": True, "Team": True, "Total Assists": True},
        "Total xG": {"Player Name": True, "Team": True, "Total xG": ":.2f"},
        "Total Creativity": {"Player Name": True, "Team": True, "Total Creativity": ":.2f"},
        "Total Influence": {"Player Name": True, "Team": True, "Total Influence": ":.2f"},
        "Total ICT Index": {"Player Name": True, "Team": True, "Total ICT Index": ":.2f"}
        }

        
        
        
        tab_goal, tab_assists, tab_xg, tab_creative, tab_influence, tab_ict = st.tabs(["Goals", "Assists", "xG", "Creatvity", "Influence", "ICT Index"])

        with tab_goal:
            fig_goal = off_chart(df_filtered_player, "Total Goals", tooltip)
            st.plotly_chart(fig_goal, theme="streamlit", use_container_width=True)

        with tab_assists:
            fig_assists = off_chart(df_filtered_player, "Total Assists", tooltip)
            st.plotly_chart(fig_assists, theme="streamlit", use_container_width=True)

        with tab_xg:
            fig_xg = off_chart(df_filtered_player, "Total xG", tooltip)
            st.plotly_chart(fig_xg, theme="streamlit", use_container_width=True)

        with tab_creative:
            fig_creative = off_chart(df_filtered_player, "Total Creativity", tooltip)
            st.plotly_chart(fig_creative, theme="streamlit", use_container_width=True)

        with tab_influence:
            fig_influence = off_chart(df_filtered_player, "Total Influence", tooltip)
            st.plotly_chart(fig_influence, theme="streamlit", use_container_width=True)

        with tab_ict:
            fig_ict = off_chart(df_filtered_player, "Total ICT Index", tooltip)
            st.plotly_chart(fig_ict, theme="streamlit", use_container_width=True)
            
        st.markdown('### Defensive Chart')    
        def def_chart(df_filtered_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
                
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text="Team",
                hover_data=tooltip.get(category, {})
                )
            custom_font_family = "Arial"
                
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
                )
                
            return fig


        
        tooltip = {
        "Total Clean Sheets": {"Player Name": True, "Team": True, "Total CS": True},
        "Total Saves": {"Player Name": True, "Team": True, "Total Saves": True},
        }
        tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

        with tab_cs:
            fig_cs = def_chart(df_filtered_player, "Total CS", tooltip)
            st.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

        with tab_saves:
            fig_saves = def_chart(df_filtered_player, "Total Saves", tooltip)
            st.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)
            
        
        
        st.markdown('### Overall Chart')
        st.markdown('##### ***Player Total Goals per 90 Minutes***')    
        def all_chart(df_filtered_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            #df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)

            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text="Team",
                hover_data=tooltip.get(category, {})

            )
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )
            
            return fig


        tooltip = {
        "Total Points": {"Player Name": True, "Team": True, "Total Points": True},
        "Total Bonus": {"Player Name": True, "Team": True, "Total Bonus": True},
        "Dreamteam": {"Player Name": True, "Team": True, "Dreamteam": True},
        "Total YC": {"Player Name": True, "Team": True, "Total YC": True},
        "Total RC": {"Player Name": True, "Team": True, "Total RC": True},

        }
        tab_points, tab_bonus, tab_dreamteam, tab_yc, tab_rc = st.tabs(["Points", "Bonus", "Dreamteam", "Yellow Cards", "Red Cards"])

        with tab_points:
            fig_points = all_chart(df_filtered_player, "Total Points", tooltip)
            st.plotly_chart(fig_points, theme="streamlit", use_container_width=True)
        with tab_bonus:
            fig_bonus = all_chart(df_filtered_player, "Total Bonus", tooltip)
            st.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)

        with tab_dreamteam:
            fig_dreamteam = all_chart(df_filtered_player, "Dreamteam", tooltip)
            st.plotly_chart(fig_dreamteam, theme="streamlit", use_container_width=True)

        with tab_yc:
            fig_yc = all_chart(df_filtered_player, "Total YC", tooltip)
            st.plotly_chart(fig_yc, theme="streamlit", use_container_width=True)

        # with tab_rc:
        #     fig_rc = all_chart(df_filtered_player, "Total RC", tooltip)
        #     st.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
        
        # with tab_rc:
        #     red_card_players = df_filtered_player[df_filtered_player['Total RC'] > 0]['Player Name'].tolist()

        with tab_rc:
            #red_card_players = df_filtered_player[df_filtered_player["Total RC"] > 0]['Player Name'].tolist()
            fig_rc = all_chart(df_filtered_player, "Total RC", tooltip) #red_card_players)
            st.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
    

        # Cost vs 22/23 Season Points chart
        st.markdown('### Cost vs 22/23 Season Points')
        st.markdown('##### ***Identify Low Price Player With High Points Return***')
        # Define custom markers for each position
        position_markers = {
            'Goalkeeper': 'circle',
            'Defender': 'square',
            'Midfielder': 'diamond',
            'Forward': 'star',
        }
        
        st.markdown('### Points per 90')
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
                # Set custom colors and markers for each position
                #text_auto=True,
                #text="Team"
            )
            custom_font_family = "Arial"

            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )

            return fig



        # Create the scatter plot with differentiated position markers and colors
        fig_cost_price = points_p90_chart(df_filtered_player)

        # Display the scatter plot using Streamlit
        st.plotly_chart(fig_cost_price, theme="streamlit", use_container_width=True)
        
        
        st.markdown('### Goals per 90')
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
                # Set custom colors and markers for each position
                #text_auto=True,
                #text="Team"
            )
            custom_font_family = "Arial"

            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )

            return fig



        # Create the scatter plot with differentiated position markers and colors
        fig_goals_price = goals_p90_chart(df_filtered_player)

        # Display the scatter plot using Streamlit
        st.plotly_chart(fig_goals_price, theme="streamlit", use_container_width=True)
    
    else:
        
        
        
        st.markdown('### Offensive Chart')  
        def off_chart(df_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
            # Set the 'Player Name' column as the index for proper sorting in the chart
            #df.set_index('Player Name', inplace=True)
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text="Team",
                hover_name="Total Points",
                hover_data=tooltip.get(category, {})

            )
            custom_font_family = "Arial"
            
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )
            
            return fig

        tooltip = {
        "Total Goals": {"Player Name": True, "Team": True, "Total Goals": True},
        "Total Assists": {"Player Name": True, "Team": True, "Total Assists": True},
        "Total xG": {"Player Name": True, "Team": True, "Total xG": ":.2f"},
        "Total Creativity": {"Player Name": True, "Team": True, "Total Creativity": ":.2f"},
        "Total Influence": {"Player Name": True, "Team": True, "Total Influence": ":.2f"},
        "Total ICT Index": {"Player Name": True, "Team": True, "Total ICT Index": ":.2f"}
        }

        
        
        
        tab_goal, tab_assists, tab_xg, tab_creative, tab_influence, tab_ict = st.tabs(["Goals", "Assists", "xG", "Creatvity", "Influence", "ICT Index"])

        with tab_goal:
            fig_goal = off_chart(df_player, "Total Goals", tooltip)
            st.plotly_chart(fig_goal, theme="streamlit", use_container_width=True)

        with tab_assists:
            fig_assists = off_chart(df_player, "Total Assists", tooltip)
            st.plotly_chart(fig_assists, theme="streamlit", use_container_width=True)

        with tab_xg:
            fig_xg = off_chart(df_player, "Total xG", tooltip)
            st.plotly_chart(fig_xg, theme="streamlit", use_container_width=True)

        with tab_creative:
            fig_creative = off_chart(df_player, "Total Creativity", tooltip)
            st.plotly_chart(fig_creative, theme="streamlit", use_container_width=True)

        with tab_influence:
            fig_influence = off_chart(df_player, "Total Influence", tooltip)
            st.plotly_chart(fig_influence, theme="streamlit", use_container_width=True)

        with tab_ict:
            fig_ict = off_chart(df_player, "Total ICT Index", tooltip)
            st.plotly_chart(fig_ict, theme="streamlit", use_container_width=True)
            
        st.markdown('### Defensive Chart')    
        def def_chart(df_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
                
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Position",
                color_discrete_map=position_colors,  # Set custom colors for each position
                text="Team",
                hover_name="Player Name",
                #hover_data=tooltip.get(category, {})
                )
            custom_font_family = "Arial"
                
            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
                )
            fig.update_xaxes(tickvals=list(map(int, df[category].unique())), tickmode='linear') 
            return fig


        
        tooltip = {
        "Total CS": {"Player Name": True, "Team": True, "Total CS": True},
        "Total Saves": {"Player Name": True, "Team": True, "Total Saves": True},
        }
        tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

        with tab_cs:
            fig_cs = def_chart(df_player, "Total CS", tooltip)
            st.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

        with tab_saves:
            fig_saves = def_chart(df_player, "Total Saves", tooltip)
            st.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)
            
                
        st.markdown('### Overall Chart')
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
        def all_chart(df_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_player.sort_values(category, ascending=False).reset_index(drop=True).head(10)
            #df = df_player.sort_values('Total Points', ascending=False).reset_index(drop=True).head(10)
            
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
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
            #fig.update_xaxes(tickformat=".f")
            fig.update_xaxes(tickvals=list(map(int, df[category].unique())), tickmode='linear')
            return fig


        tooltip = {
        "Total Points": {"Player Name": True, "Team": True, "Total Points": True},
        "Total Bonus": {"Player Name": True, "Team": True, "Total Bonus": True},
        "Dreamteam": {"Player Name": True, "Team": True, "Dreamteam": True},
        "Total YC": {"Player Name": True, "Team": True, "Total YC": True},
        "Total RC": {"Player Name": True, "Team": True, "Total RC": True},

        }
        tab_points, tab_bonus, tab_dreamteam, tab_yc, tab_rc = st.tabs(["Points", "Bonus", "Dreamteam", "Yellow Cards", "Red Cards"])

        with tab_points:
            fig_points = all_chart(df_player, "Total Points", tooltip)
            st.plotly_chart(fig_points, theme="streamlit", use_container_width=True)
        with tab_bonus:
            fig_bonus = all_chart(df_player, "Total Bonus", tooltip)
            st.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)

        with tab_dreamteam:
            fig_dreamteam = all_chart(df_player, "Dreamteam", tooltip)
            st.plotly_chart(fig_dreamteam, theme="streamlit", use_container_width=True)

        with tab_yc:
            fig_yc = all_chart(df_player, "Total YC", tooltip)
            st.plotly_chart(fig_yc, theme="streamlit", use_container_width=True)

        with tab_rc:
            fig_rc = all_chart(df_player, "Total RC", tooltip)
            st.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
    

        # Cost vs 22/23 Season Points chart
        st.markdown('### Cost vs 22/23 Season Points')
        st.markdown('##### ***Identify Low Price Player With High Points Return***')
        # Define custom markers for each position
        position_markers = {
            'Goalkeeper': 'circle',
            'Defender': 'square',
            'Midfielder': 'diamond',
            'Forward': 'star',
        }
        
        st.markdown('### Points per 90')
        st.markdown('##### ***Player Total Points per 90 Minutes***')    
        def points_p90_chart(df_player):


            # Create the scatter plot
            fig = px.scatter(
                df_player,
                y="Total Points",
                x="Price",
                color="Position",
                color_discrete_map=position_colors,
                symbol="Position",
                symbol_map=position_markers,
                hover_name="Player Name",  # Column to be displayed as tooltip
                hover_data=["Team"],
            )
            custom_font_family = "Arial"

            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )

            return fig



        # Create the scatter plot with differentiated position markers and colors
        fig_cost_price = points_p90_chart(df_player)

        # Display the scatter plot using Streamlit
        st.plotly_chart(fig_cost_price, theme="streamlit", use_container_width=True)
        
        
        st.markdown('### Goals per 90')
        st.markdown('##### ***Player Total Goals per 90 Minutes***')
        
        def goals_p90_chart(df_player):


            # Create the scatter plot
            fig = px.scatter(
                df_player,
                y="Total Goals",
                x="Price",
                color="Position",
                color_discrete_map=position_colors,
                symbol="Position",
                symbol_map=position_markers,
                hover_name="Player Name",  # Column to be displayed as tooltip
                hover_data=["Team"],
            )
            custom_font_family = "Arial"

            # Set the custom font for the text
            fig.update_layout(
                font_family=custom_font_family,
                font_color="black",  # Optionally, set the font color
            )

            return fig



        # Create the scatter plot with differentiated position markers and colors
        fig_goals_price = goals_p90_chart(df_player)

        # Display the scatter plot using Streamlit
        st.plotly_chart(fig_goals_price, theme="streamlit", use_container_width=True)
