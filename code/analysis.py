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

    # Sidebar filters
    teams = st.sidebar.multiselect("Teams:", list(df_player['Team'].drop_duplicates()), default=list(df_player['Team'].drop_duplicates()))
    positions = st.sidebar.multiselect("Choose position:", list(df_player['Position'].drop_duplicates()), default=list(df_player['Position'].drop_duplicates()))
    price_choice = st.sidebar.slider('Max Price:', min_value=4.0, max_value=15.0, step=0.5, value=15.0)

    # Apply filters to the player data
    df_filtered_player = df_player[df_player['Position'].isin(positions) & df_player['Team'].isin(teams) & (df_player['Price'] < price_choice)]

    
    
        
    # Display player data
    st.markdown('### Player Overall Data', unsafe_allow_html=True)
    st.dataframe(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True))
   
    
        # Define custom colors for each position
    position_colors = {
        'Goalkeeper': '#60DB00',
        'Defender': '#B141FF',
        'Midfielder': '#00DADA',
        'Forward': '#9DB600',
    }
    
    st.markdown('### Overall Chart')
    #st.markdown('##### ***Player Total Goals per 90 Minutes***')    
    def all_chart(df_filtered_player, category, tooltip):

        
        # Filter the data to include only the top 5 players
        df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
        
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

    with tab_rc:
        fig_rc = all_chart(df_filtered_player, "Total RC", tooltip)
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
        df = df_filtered_player.sort_values(category, ascending=False).reset_index(drop=True).head(5)
            
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
    "Total Clean Sheets": {"Player Name": True, "Team": True, "Total Clean Sheets": True},
    "Total Saves": {"Player Name": True, "Team": True, "Total Saves": True},
    }
    tab_cs, tab_saves= st.tabs(["Clean Sheets", "Saves"])

    with tab_cs:
        fig_cs = def_chart(df_filtered_player, "Total Clean Sheets", tooltip)
        st.plotly_chart(fig_cs, theme="streamlit", use_container_width=True)

    with tab_saves:
        fig_saves = def_chart(df_filtered_player, "Total Saves", tooltip)
        st.plotly_chart(fig_saves, theme="streamlit", use_container_width=True)
        
    
   

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
   
    
    # st.vega_lite_chart(df_filtered_player, {
    #      'mark': {'type': 'circle', 'tooltip': True},
    #      'encoding': {
    #          'x': {'field': 'Price', 'type': 'quantitative'},
    #          'y': {'field': 'Total Points', 'type': 'quantitative'},
    #          'color': {'field': 'Position', 'type': 'nominal'},
    #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    #      },
    #      'width': 800,
    #      'height': 400,
    #  })

    # # Goals per 90 chart
    # st.markdown('### Goals per 90')
    # st.markdown('##### ***Player Total Goals, Assists and Points per 90 Minutes***')
    # st.vega_lite_chart(df_filtered_player, {
    #  'mark': {'type': 'circle', 'tooltip': True},
    #  'encoding': {
    #      'x': {'field': 'Total Goals P90', 'type': 'quantitative'},
    #      'y': {'field': 'Total Assists P90', 'type': 'quantitative'},
    #      'color': {'field': 'Position', 'type': 'nominal'},
    #      'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Goals P90', 'type': 'quantitative'}, {'field': 'Total Assists P90', 'type': 'quantitative'}, {'field': 'Total Points P90', 'type': 'quantitative'}],
    #  },
    #  'width': 800,
    #  'height': 400,
    # })
    
    # st.markdown('### Influence')
    # st.vega_lite_chart(df_filtered_player.sort_values('Total Influence', ascending=False).reset_index(drop=True).head(5), {
    #      'mark': {'type': 'bar', 'tooltip': True},
    #      'encoding': {
    #          'x': {'field': 'Total Influence', 'type': 'quantitative'},
    #          'y': {'field': 'Player Name', 'type': 'nominal'},
    #          'color': pos_color_scale,
    #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Influence', 'type': 'quantitative'}, {'field': 'Team', 'type': 'nominal'}],
    #      },
    #      'width': 800,
    #      'height': 400,
    # })
    

    # st.markdown('### Influence')

    # chart = alt.Chart(df_filtered_player.sort_values('Total Influence', ascending=False).reset_index(drop=True).head(5)).mark_bar().encode(
    #     x=alt.X('Total Influence', type='quantitative'),
    #     y=alt.Y('Player Name', type='nominal'),
    #     color=alt.Color('Position'),
    #     tooltip=[
    #         {"field": 'Player Name', 'type': 'nominal'},
    #         {'field': 'Price', 'type': 'quantitative'},
    #         {'field': 'Total Influence', 'type': 'quantitative'},
    #         {'field': 'Team', 'type': 'nominal'}
    #     ]
    # ).properties(
    #     width=800,
    #     height=400
    # )

    # text = chart.mark_text(
    #     align='center',
    #     baseline='middle',
    #     dx= 25, # Adjust the horizontal position of the text
    #     color='grey'   
    # ).encode(
    #     text='Team'  # Display the 'Position' field as the text inside the bar
    # )


    # st.altair_chart(chart + text, use_container_width=True)
    
    
    

