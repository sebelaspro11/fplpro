import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import requests
from PIL import Image





def perform_manager():

    image = Image.open("data/fpl.png")

    st.image(image, caption='Manager ID')
    manager_id = st.text_input("Enter manager ID:")
    if st.button("Get Manager Details"):
        if manager_id:
            url = 'https://fantasy.premierleague.com/api/entry//' + manager_id
            r = requests.get(url)
            json = r.json()
            manager_df = pd.DataFrame(json)
            manager_df = manager_df.iloc[[0, 3], :]
            manager_df['All Leagues'] = manager_df['leagues'].apply(lambda x: ', '.join([item['name'] for item in x]))
            manager_df = manager_df[['joined_time', 'player_first_name', 'player_last_name', 'player_region_iso_code_short', 'summary_overall_points', 'summary_overall_rank', 'summary_event_rank','summary_event_points', 'All Leagues', 'current_event' ]]

            # Rename the columns using the rename() method
            new_names = {
                "player_first_name" : "First Name",
                "player_last_name" : "Last Name",
                "player_region_iso_code_short" : "Country Code",
                "joined_time" : "Registered Time",
                "summary_event_points" : "Gameweek Points",
                "summary_overall_points" : "Total Points",
                "summary_event_rank" : "Gameweek Rank",
                "summary_overall_rank" : "Last Rank",
                "All Leagues" : "League Entered",
                "current_event" : "Gameweek"
            }
            manager_df = manager_df.rename(columns=new_names)

    
    
    
        # Display First Name and Last Name
        st.write("First Name:", manager_df['First Name'].values[0])
        st.write("Last Name:", manager_df['Last Name'].values[0])
        st.write("Registered Time:", manager_df['Registered Time'].values[0])
        st.write("League Entered:", manager_df['League Entered'].values[0])
        st.write("Gameweek Points:", manager_df['Gameweek Points'].values[0])
        st.write("Total Points:", manager_df['Total Points'].values[0])
        st.write("Gameweek Rank:", manager_df['Gameweek Rank'].values[0])
        st.write("Last Rank:", manager_df['Last Rank'].values[0])
        st.write("Gameweek:", manager_df['Gameweek'].values[0])
        
        
        
