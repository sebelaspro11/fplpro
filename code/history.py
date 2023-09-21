import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import plotly.express as px
    
    
    
    
def perform_history():    
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
    collection_history = db["history"]
    
    
    
    @st.cache_resource
    def fetch_data_past_history(_collect):
    # Fetch the data from the collection
        return pd.DataFrame(list(_collect.find({}, {"_id": 0})))

    df_past_history_2023 = fetch_data_past_history(collection_history)
    
    
    
    # Sidebar filters
    season_hist = st.sidebar.multiselect("Seasons:", list(df_past_history_2023['Seasons'].drop_duplicates()), default=list(df_past_history_2023['Seasons'].drop_duplicates()))
    player_hist = st.sidebar.multiselect("Player Name:", df_past_history_2023.sort_values("Total Points", ascending=False)[df_past_history_2023['Seasons'].isin(season_hist)]['Player Name'].drop_duplicates().tolist())
    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=0.5, value=15.0)
    show_filtered = st.sidebar.checkbox("Show filtered data", value=False)

    
    
    
    # Apply filters to the player data
    df_filtered_player = df_past_history_2023[df_past_history_2023['Seasons'].isin(season_hist) & df_past_history_2023['Player Name'].isin(player_hist) & (df_past_history_2023['End Price'] < price_choice)]
    
    if show_filtered:
            st.data_editor(
    df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True),
    column_config={
        "Seasons": st.column_config.TextColumn(
            "Seasons",
            help="Seasons Played",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
         "Player Name": st.column_config.TextColumn(
            "Player Name",
            help="Player Name",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
        "Total Points": st.column_config.ProgressColumn(
            "Total Points",
            help="Player Total Fantasy Points",
            min_value=-2,
            max_value=136,
            format="%d",
        ),
         "End Price": st.column_config.ProgressColumn(
            "End Price",
            help="End of Season Price",
            min_value=3.5,
            max_value=14.2,
            format="$%f",
        ),
         "Minutes Played": st.column_config.ProgressColumn(
            "Minutes Played",
            help="Player Total Minutes Played",
            min_value=0,
            max_value=3420,
            format="%d",
        ),
         "Start Price": st.column_config.NumberColumn(
            "Start Price",
            help="Start of Season Price",
            min_value=3.5,
            max_value=14.0,
            format="$%.1f",
        ),
         "Total Assists": st.column_config.ProgressColumn(
            "Total Assists",
            help="Player Total of Assists",
            min_value=0,
            max_value=23,
            format="%d",
            
        ),
         "Total Bonus": st.column_config.ProgressColumn(
            "Total Bonus",
            help="Player Total of Bonus Points",
            min_value=0,
            max_value=48,
            format="%d",
        ),
         "Total BPS": st.column_config.ProgressColumn(
            "Total BPS",
            help="Player Total of Bonus Points System",
            min_value=-2,
            max_value=1040,
            format="%d",
        ),
         "Total Clean Sheets": st.column_config.ProgressColumn(
            "Total CS",
            help="Player Total Clean Sheets",
            min_value=0,
            max_value=21,
            format="%d",
        ),
         "Total Creativity": st.column_config.ProgressColumn(
            "Total Creativity",
            help="Player Total Creativity Points",
            min_value=0,
            max_value=1990.8,
            format="%d",
        ),
         "Total Goals": st.column_config.ProgressColumn(
            "Total Goals",
            help="Player Total Goals",
            min_value=0,
            max_value=36,
            format="%d",
        ),
         "Total Goals Conceded": st.column_config.ProgressColumn(
            "Total GC",
            help="Player Total Goals Conceded",
            min_value=0,
            max_value=79,
            format="%d",
        ),
         "Total ICT Index": st.column_config.ProgressColumn(
            "Total ICT Index",
            help="Player Total Influence, Creativity & Threat Index",
            min_value=0,
            max_value=454.4,
            format="%d",
        ),
         "Total Influence": st.column_config.ProgressColumn(
            "Total Influence",
            help="Player Total Influence Points",
            min_value=0,
            max_value=1496.2,
            format="%d",
        ),
         "Total OG": st.column_config.ProgressColumn(
            "Total OG",
            help="Player Total Own Goals",
            min_value=0,
            max_value=4,
            format="%d",
        ),
         "Total Penalties Saved": st.column_config.ProgressColumn(
            "Total Penalties Saved",
            help="Player Total Penalties Saved",
            min_value=0,
            max_value=3,
            format="%d",
        ),
         "Total RC": st.column_config.ProgressColumn(
            "Total RC",
            help="Player Total Red Cards",
            min_value=0,
            max_value=2,
            format="%d",
        ),
         "Total YC": st.column_config.ProgressColumn(
            "Total YC",
            help="Player Total Yellow Cards",
            min_value=0,
            max_value=14,
            format="%d",
        ),
         "Total Saves": st.column_config.ProgressColumn(
            "Total Saves",
            help="Player Total Saves (GK)",
            min_value=0,
            max_value=167,
            format="%d",
        ),
         "Total Starts": st.column_config.ProgressColumn(
            "Total Starts",
            help="Player Total Games Started as First 11",
        
            min_value=0,
            max_value=38,
            format="%d",
        ),
         "Total Threat": st.column_config.ProgressColumn(
            "Total Threat",
            help="Player Total Threat Points",
            min_value=0,
            max_value=2355,
            format="%d",
        ),
         "Total xA": st.column_config.ProgressColumn(
            "Total xA",
            help="Player Total Expected Assists",
        
            min_value=0,
            max_value=13.69,
            format="%d",
        ),
         "Total xG": st.column_config.ProgressColumn(
            "Total xG",
            help="Player Total Expected Goals",
        
            min_value=0,
            max_value=14,
            format="%d",
        ),
         "Total xG Against": st.column_config.ProgressColumn(
            "Total xG Against",
            help="Player Total Expected Goals Againts",
        
            min_value=0,
            max_value=67.45,
            format="%d",
        ),
         "Total xG Involvements": st.column_config.ProgressColumn(
            "Total xG Involvements",
            help="Player Total Expected Goals Involvements",
        
            min_value=0,
            max_value=31.65,
            format="%d",
        ),
          "Total Penalties Missed": st.column_config.ProgressColumn(
            "Total Penalties Missed",
            help="Player Total Penalties Missed",
        
            min_value=0,
            max_value=14,
            format="%d",
        )
        
         
        
    },
    hide_index=True,
)
    else:
        
        
        st.data_editor(
    df_past_history_2023.sort_values('Total Points', ascending=False).reset_index(drop=True),
    column_config={
        "Seasons": st.column_config.TextColumn(
            "Seasons",
            help="Seasons Played",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
         "Player Name": st.column_config.TextColumn(
            "Player Name",
            help="Player Name",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
        "Total Points": st.column_config.ProgressColumn(
            "Total Points",
            help="Player Total Fantasy Points",
            min_value=-2,
            max_value=136,
            format="%d",
        ),
         "End Price": st.column_config.ProgressColumn(
            "End Price",
            help="End of Season Price",
            min_value=3.5,
            max_value=14.2,
            format="$%f",
        ),
         "Minutes Played": st.column_config.ProgressColumn(
            "Minutes Played",
            help="Player Total Minutes Played",
            min_value=0,
            max_value=3420,
            format="%d",
        ),
         "Start Price": st.column_config.NumberColumn(
            "Start Price",
            help="Start of Season Price",
            min_value=3.5,
            max_value=14.0,
            format="$%.1f",
        ),
         "Total Assists": st.column_config.ProgressColumn(
            "Total Assists",
            help="Player Total of Assists",
            min_value=0,
            max_value=23,
            format="%d",
            
        ),
         "Total Bonus": st.column_config.ProgressColumn(
            "Total Bonus",
            help="Player Total of Bonus Points",
            min_value=0,
            max_value=48,
            format="%d",
        ),
         "Total BPS": st.column_config.ProgressColumn(
            "Total BPS",
            help="Player Total of Bonus Points System",
            min_value=-2,
            max_value=1040,
            format="%d",
        ),
         "Total Clean Sheets": st.column_config.ProgressColumn(
            "Total CS",
            help="Player Total Clean Sheets",
            min_value=0,
            max_value=21,
            format="%d",
        ),
         "Total Creativity": st.column_config.ProgressColumn(
            "Total Creativity",
            help="Player Total Creativity Points",
            min_value=0,
            max_value=1990.8,
            format="%d",
        ),
         "Total Goals": st.column_config.ProgressColumn(
            "Total Goals",
            help="Player Total Goals",
            min_value=0,
            max_value=36,
            format="%d",
        ),
         "Total Goals Conceded": st.column_config.ProgressColumn(
            "Total GC",
            help="Player Total Goals Conceded",
            min_value=0,
            max_value=79,
            format="%d",
        ),
         "Total ICT Index": st.column_config.ProgressColumn(
            "Total ICT Index",
            help="Player Total Influence, Creativity & Threat Index",
            min_value=0,
            max_value=454.4,
            format="%d",
        ),
         "Total Influence": st.column_config.ProgressColumn(
            "Total Influence",
            help="Player Total Influence Points",
            min_value=0,
            max_value=1496.2,
            format="%d",
        ),
         "Total OG": st.column_config.ProgressColumn(
            "Total OG",
            help="Player Total Own Goals",
            min_value=0,
            max_value=4,
            format="%d",
        ),
         "Total Penalties Saved": st.column_config.ProgressColumn(
            "Total Penalties Saved",
            help="Player Total Penalties Saved",
            min_value=0,
            max_value=3,
            format="%d",
        ),
         "Total RC": st.column_config.ProgressColumn(
            "Total RC",
            help="Player Total Red Cards",
            min_value=0,
            max_value=2,
            format="%d",
        ),
         "Total YC": st.column_config.ProgressColumn(
            "Total YC",
            help="Player Total Yellow Cards",
            min_value=0,
            max_value=14,
            format="%d",
        ),
         "Total Saves": st.column_config.ProgressColumn(
            "Total Saves",
            help="Player Total Saves (GK)",
            min_value=0,
            max_value=167,
            format="%d",
        ),
         "Total Starts": st.column_config.ProgressColumn(
            "Total Starts",
            help="Player Total Games Started as First 11",
        
            min_value=0,
            max_value=38,
            format="%d",
        ),
         "Total Threat": st.column_config.ProgressColumn(
            "Total Threat",
            help="Player Total Threat Points",
            min_value=0,
            max_value=2355,
            format="%d",
        ),
         "Total xA": st.column_config.ProgressColumn(
            "Total xA",
            help="Player Total Expected Assists",
        
            min_value=0,
            max_value=13.69,
            format="%d",
        ),
         "Total xG": st.column_config.ProgressColumn(
            "Total xG",
            help="Player Total Expected Goals",
        
            min_value=0,
            max_value=14,
            format="%d",
        ),
         "Total xG Against": st.column_config.ProgressColumn(
            "Total xG Against",
            help="Player Total Expected Goals Againts",
        
            min_value=0,
            max_value=67.45,
            format="%d",
        ),
         "Total xG Involvements": st.column_config.ProgressColumn(
            "Total xG Involvements",
            help="Player Total Expected Goals Involvements",
        
            min_value=0,
            max_value=31.65,
            format="%d",
        ),
          "Total Penalties Missed": st.column_config.ProgressColumn(
            "Total Penalties Missed",
            help="Player Total Penalties Missed",
        
            min_value=0,
            max_value=14,
            format="%d",
        )
        
         
        
    },
    hide_index=True,
)
  
    
   
    
    if show_filtered:
            # Define custom colors for each Seasons
        season_colors = {
            '2006/2007': '#60DB00',
            '2007/2008': '#B141FF',
            '2008/2009': '#00DADA',
            '2009/2010': '#9DB602',
            '2010/2011': '#9DB603',
            '2008/2012': '#9DB604',
            '2008/2013': '#9DB605',
            '2008/2014': '#9DB606',
            '2008/2015': '#9DB607',
            '2008/2016': '#9DB605',
            '2008/2017': '#9DB602',
            '2008/2018': '#9DB605',
            '2008/2019': '#9DB602',
            '2020/2021': '#9DB606',
            '2022/2023': '#9DB608',
        }
        
        st.markdown('### Overall Chart')
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
        def all_chart_history(df_filtered_player, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Points": {"Player Name": True, "Seasons": True, "Total Points": True, "Total Points": True},
        "Total Bonus": {"Player Name": True, "Seasons": True, "Total Bonus": True},
        "Total Yellow Cards": {"Player Name": True,  "Seasons": True, "Total Yellow Cards": True},
        "Total Red Cards": {"Player Name": True, "Seasons": True, "Total Red Cards": True},

        }
        tab_points, tab_bonus, tab_yc, tab_rc = st.tabs(["Points", "Bonus", "Yellow Cards", "Red Cards"])

        with tab_points:
            fig_points = all_chart_history(df_filtered_player, "Total Points", tooltip)
            st.plotly_chart(fig_points, theme="streamlit", use_container_width=True)
        with tab_bonus:
            fig_bonus = all_chart_history(df_filtered_player, "Total Bonus", tooltip)
            st.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)

        with tab_yc:
            fig_yc = all_chart_history(df_filtered_player, "Total YC", tooltip)
            st.plotly_chart(fig_yc, theme="streamlit", use_container_width=True)

        with tab_rc:
            fig_rc = all_chart_history(df_filtered_player, "Total RC", tooltip)
            st.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
            
            
        st.markdown('### Offensive Chart')  
        def off_chart(df_filtered_player, category, tootltip):

            
            # Filter the data to include only the top 5 players
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Goals": {"Player Name": True, "Seasons": True, "Total Goals": True},
        "Total Assists": {"Player Name": True, "Seasons": True, "Total Assists": True},
        "Total xG": {"Player Name": True, "Seasons": True, "Total xG": ":.2f"},
        "Total Creativity": {"Player Name": True, "Seasons": True, "Total Creativity": ":.2f"},
        "Total Influence": {"Player Name": True, "Seasons": True, "Total Influence": ":.2f"},
        "Total ICT Index": {"Player Name": True, "Seasons": True, "Total ICT Index": ":.2f"}
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
            df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
                
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Clean Sheets": {"Player Name": True, "Seasons": True, "Total Clean Sheets": True},
        "Total Saves": {"Player Name": True, "Seasons": True, "Total Saves": True},
        }
        tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

        with tab_cs:
            fig_cs = def_chart(df_filtered_player, "Total Clean Sheets", tooltip)
            st.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

        with tab_saves:
            fig_saves = def_chart(df_filtered_player, "Total Saves", tooltip)
            st.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)
            
    else:    
        # Define custom colors for each Seasons
        season_colors = {
            '2006/2007': '#60DB00',
            '2007/2008': '#B141FF',
            '2008/2009': '#00DADA',
            '2009/2010': '#9DB602',
            '2010/2011': '#9DB603',
            '2008/2012': '#9DB604',
            '2008/2013': '#9DB605',
            '2008/2014': '#9DB606',
            '2008/2015': '#9DB607',
            '2008/2016': '#9DB605',
            '2008/2017': '#9DB602',
            '2008/2018': '#9DB605',
            '2008/2019': '#9DB602',
            '2020/2021': '#9DB606',
            '2022/2023': '#9DB608',
        }
        
        st.markdown('### Overall Chart')
        #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
        def all_chart_history(df_past_history_2023, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_past_history_2023.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Points": {"Player Name": True, "Seasons": True, "Total Points": True, "Total Points": True},
        "Total Bonus": {"Player Name": True, "Seasons": True, "Total Bonus": True},
        "Total Yellow Cards": {"Player Name": True,  "Seasons": True, "Total Yellow Cards": True},
        "Total Red Cards": {"Player Name": True, "Seasons": True, "Total Red Cards": True},

        }
        tab_points, tab_bonus, tab_yc, tab_rc = st.tabs(["Points", "Bonus", "Yellow Cards", "Red Cards"])

        with tab_points:
            fig_points = all_chart_history(df_past_history_2023, "Total Points", tooltip)
            st.plotly_chart(fig_points, theme="streamlit", use_container_width=True)
        with tab_bonus:
            fig_bonus = all_chart_history(df_past_history_2023, "Total Bonus", tooltip)
            st.plotly_chart(fig_bonus, theme="streamlit", use_container_width=True)

        with tab_yc:
            fig_yc = all_chart_history(df_past_history_2023, "Total YC", tooltip)
            st.plotly_chart(fig_yc, theme="streamlit", use_container_width=True)

        with tab_rc:
            fig_rc = all_chart_history(df_past_history_2023, "Total RC", tooltip)
            st.plotly_chart(fig_rc, theme="streamlit", use_container_width=True)
            
            
        st.markdown('### Offensive Chart')  
        def off_chart(df_past_history_2023, category, tootltip):

            
            # Filter the data to include only the top 5 players
            df = df_past_history_2023.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Goals": {"Player Name": True, "Seasons": True, "Total Goals": True},
        "Total Assists": {"Player Name": True, "Seasons": True, "Total Assists": True},
        "Total xG": {"Player Name": True, "Seasons": True, "Total xG": ":.2f"},
        "Total Creativity": {"Player Name": True, "Seasons": True, "Total Creativity": ":.2f"},
        "Total Influence": {"Player Name": True, "Seasons": True, "Total Influence": ":.2f"},
        "Total ICT Index": {"Player Name": True, "Seasons": True, "Total ICT Index": ":.2f"}
        }

        
        
        
        tab_goal, tab_assists, tab_xg, tab_creative, tab_influence, tab_ict = st.tabs(["Goals", "Assists", "xG", "Creatvity", "Influence", "ICT Index"])

        with tab_goal:
            fig_goal = off_chart(df_past_history_2023, "Total Goals", tooltip)
            st.plotly_chart(fig_goal, theme="streamlit", use_container_width=True)

        with tab_assists:
            fig_assists = off_chart(df_past_history_2023, "Total Assists", tooltip)
            st.plotly_chart(fig_assists, theme="streamlit", use_container_width=True)

        with tab_xg:
            fig_xg = off_chart(df_past_history_2023, "Total xG", tooltip)
            st.plotly_chart(fig_xg, theme="streamlit", use_container_width=True)

        with tab_creative:
            fig_creative = off_chart(df_past_history_2023, "Total Creativity", tooltip)
            st.plotly_chart(fig_creative, theme="streamlit", use_container_width=True)

        with tab_influence:
            fig_influence = off_chart(df_past_history_2023, "Total Influence", tooltip)
            st.plotly_chart(fig_influence, theme="streamlit", use_container_width=True)

        with tab_ict:
            fig_ict = off_chart(df_past_history_2023, "Total ICT Index", tooltip)
            st.plotly_chart(fig_ict, theme="streamlit", use_container_width=True)
            
        st.markdown('### Defensive Chart')   
        def def_chart(df_past_history_2023, category, tooltip):

            
            # Filter the data to include only the top 5 players
            df = df_past_history_2023.sort_values(category, ascending=False).reset_index(drop=True).head(5)
                
            # Create the bar chart
            fig = px.bar(
                df,
                y="Player Name",
                x=category,
                color="Seasons",
                color_discrete_map=season_colors,  # Set custom colors for each Seasons
                text="Seasons",
                hover_name="Player Name",
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
        "Total Clean Sheets": {"Player Name": True, "Seasons": True, "Total Clean Sheets": True},
        "Total Saves": {"Player Name": True, "Seasons": True, "Total Saves": True},
        }
        tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

        with tab_cs:
            fig_cs = def_chart(df_past_history_2023, "Total CS", tooltip)
            st.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

        with tab_saves:
            fig_saves = def_chart(df_past_history_2023, "Total Saves", tooltip)
            st.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)
