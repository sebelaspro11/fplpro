import pandas as pd
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
    
    
    
    
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
    player_hist = st.sidebar.multiselect("Player Name:", df_past_history_2023[df_past_history_2023['Seasons'].isin(season_hist)]['Player Name'].drop_duplicates().tolist())
    # Apply filters to the player data
    df_hist_player_filter = df_past_history_2023[df_past_history_2023['Seasons'].isin(season_hist) & df_past_history_2023['Player Name'].isin(player_hist)]
    
    #st.dataframe(df_hist_player_filter.sort_values('Seasons', ascending=False).reset_index(drop=True))
    st.data_editor(
    df_hist_player_filter,
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
            format="$%f",
        )
        #  "Total Assists": st.column_config.TextColumn(
        #     "Total Assists",
        #     help="Player Total of Assists",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Bonus": st.column_config.TextColumn(
        #     "Total Bonus",
        #     help="Player Total of Bonus Points",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total BPS": st.column_config.TextColumn(
        #     "Total BPS",
        #     help="Player Total Bonus Point System",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Clean Sheets": st.column_config.TextColumn(
        #     "Total Clean Sheets",
        #     help="Player Total Clean Sheets",
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Creativity": st.column_config.TextColumn(
        #     "Total Creativity",
        #     help="Player Total Creativity Points",
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Goals": st.column_config.TextColumn(
        #     "Total Goals",
        #     help="Player Total Goals",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Goals Conceded": st.column_config.TextColumn(
        #     "Total CGoals Conceded",
        #     help="Player Total Goals Conceded",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total ICT Index": st.column_config.TextColumn(
        #     "Total ICT Index",
        #     help="Player Total Influence, Creativity & Threat Index",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Influence": st.column_config.TextColumn(
        #     "Total Influence",
        #     help="Player Total Influence Points",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Own Goals": st.column_config.TextColumn(
        #     "Total Own Goals",
        #     help="Player Total Own Goals",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Penalties Saved": st.column_config.TextColumn(
        #     "Total Penalties Saved",
        #     help="Player Total Penalties Saved",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Points": st.column_config.TextColumn(
        #     "Total Points",
        #     help="Player Total Fantasy Points",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Red Cards": st.column_config.TextColumn(
        #     "Total Red Cards",
        #     help="Player Total Red Cards",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Yellow Cards": st.column_config.TextColumn(
        #     "Total Yellow Cards",
        #     help="Player Total Yellow Cards",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Saves": st.column_config.TextColumn(
        #     "Total Saves",
        #     help="Player Total Saves (GK)",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Starts": st.column_config.TextColumn(
        #     "Total Starts",
        #     help="Player Total Games Started as First 11",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total Threat": st.column_config.TextColumn(
        #     "Total Threat",
        #     help="Player Total Threat Points",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total xA": st.column_config.TextColumn(
        #     "Total xA",
        #     help="Player Total Expected Assists",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total xG": st.column_config.TextColumn(
        #     "Total xG",
        #     help="Player Total Expected Goals",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total xG Against": st.column_config.TextColumn(
        #     "Total xG Against",
        #     help="Player Total Expected Goals Againts",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #  "Total xG Involvements": st.column_config.TextColumn(
        #     "Total xG Involvements",
        #     help="Player Total Expected Goals Involvements",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # ),
        #   "Total Penalty Missed": st.column_config.TextColumn(
        #     "Total Penalty Missed",
        #     help="Player Total Penalty Missed",
        # 
        #     max_chars=50,
        #     validate="^st\.[a-z_]+$",
        # )
        
         
        
    },
    hide_index=True,
)