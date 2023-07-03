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
        'Goalkeeper': 'red',
        'Defender': 'pink',
        'Midfielder': 'green',
        'Forward': 'blue',
    }
    
    # Filter the data to include only the top 5 players
    df = df_filtered_player.sort_values('Total Influence', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_influence = px.bar(
        df,
        y="Player Name",
        x="Total Influence",
        color="Position",
        color_discrete_map=position_colors,  # Set custom colors for each position
        #text_auto=True,
        text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_influence.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
    
     # Filter the data to include only the top 5 players
    df_goal = df_filtered_player.sort_values('Total Goals', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_goal = px.bar(
        df_goal,
        y="Player Name",
        x="Total Goals",
        color="Position",
        color_discrete_map=position_colors,  # Set custom colors for each position
        #text_auto=True,
        text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_goal.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
    
     # Filter the data to include only the top 5 players
    df_assists = df_filtered_player.sort_values('Total Assists', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_assists = px.bar(
        df_assists,
        y="Player Name",
        x="Total Assists",
        color="Position",
        color_discrete_map=position_colors,  # Set custom colors for each position
        #text_auto=True,
        text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_assists.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
     # Filter the data to include only the top 5 players
    df_creative = df_filtered_player.sort_values('Total Creativity', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_creative = px.bar(
        df_creative,
        y="Player Name",
        x="Total Creativity",
        color="Position",
        color_discrete_map=position_colors,  # Set custom colors for each position
        #text_auto=True,
        text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_creative.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
     # Filter the data to include only the top 5 players
    df_xg = df_filtered_player.sort_values('Total xG', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_xg = px.bar(
        df_xg,
        y="Player Name",
        x="Total xG",
        color="Position",
        color_discrete_map=position_colors,  # Set custom colors for each position
        #text_auto=True,
        text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_xg.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
    
    tab_goal, tab_assists, tab_xg, tab_creative, tab_influence = st.tabs(["Goals", "Assists", "xG", "Creatvity", "Influence"])

    with tab_goal:
        st.plotly_chart(fig_goal, theme="streamlit", use_container_width=True)
    with tab_assists:
        st.plotly_chart(fig_assists, theme="streamlit", use_container_width=True)
    with tab_xg:
        st.plotly_chart(fig_xg, theme="streamlit", use_container_width=True)
    with tab_creative:
        st.plotly_chart(fig_creative, theme="streamlit", use_container_width=True)
    with tab_influence:
        st.plotly_chart(fig_influence, theme="streamlit", use_container_width=True)
   
   
   
    # Filter the data to include only the top 5 players
    #df_cost_price = df_filtered_player.sort_values('Total Po', ascending=False).reset_index(drop=True).head(5)
    
    # Create the bar chart
    fig_cost_price = px.scatter(
        df_filtered_player,
        y="Total Points",
        x="Price",
        color="Position",
        color_discrete_map=position_colors,
        # Set custom colors for each position
        #text_auto=True,
        #text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_cost_price.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
    st.plotly_chart(fig_cost_price, theme="streamlit", use_container_width=True)
    
    
    
    
    # Create the bar chart
    fig_point_p90 = px.scatter(
        df_filtered_player,
        y="Total Assists P90",
        x="Total Goals P90",
        color="Position",
        color_discrete_map=position_colors,
        # Set custom colors for each position
        #text_auto=True,
        #text="Team"
    )
    custom_font_family = "Arial"
    

    # Set the custom font for the text
    fig_point_p90.update_layout(
        font_family=custom_font_family,
        font_color="black",  # Optionally, set the font color
        
    )
    
    st.plotly_chart(fig_point_p90, theme="streamlit", use_container_width=True)

    #download data
    # my_large_df = df_filtered_player
    # @st.cache
    # def convert_df_to_csv(df):
    # # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #     return df.to_csv().encode('utf-8')

    # st.download_button(
    #     label="Download data as CSV",
    #     data=convert_df_to_csv(my_large_df),
    #     file_name='player.csv',
    #     mime='text/csv',
    # )



    # # Define position colors
    # pos_colors = {
    #     'Defender': 'pink',
    #     'Forward': 'blue',
    #     'Goalkeeper': 'red',
    #     'Midfielder': 'green',
        
    # }
    
    
    
    # # Define color scale based on positions
    # pos_color_scale = {
    #     'field': 'Position',
    #     'type': 'nominal',
    #     'scale': {'range': [pos_colors[pos] for pos in df_filtered_player['Position'].unique()]}
    # }
    # color_pos = set(df_filtered_player['Position']) 
    # pos_colors = {pos: color for pos, color in pos_colors.items() if pos in color_pos}
    
    # st.markdown('### Points')
    # # st.vega_lite_chart(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True).head(5), {
    # #      'mark': {'type': 'bar', 'tooltip': True},
    # #      'encoding': {
    # #          'x': {'field': 'Total Points', 'type': 'quantitative'},
    # #          'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
    # #          'color': {
    # #          'field': 'Position',
    # #          'type': 'nominal',
    # #          'scale': {
    # #              'domain': list(pos_colors.keys()),  # List of position values
    # #              'range': list(pos_colors.values())  # List of corresponding colors
    # #          },
    # #      },
    # #          #'color': {'field': 'Position', 'type': 'nominal'},
    # #          #'color': pos_color_scale,
    # #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    # #      },
    # #      'width': 800,
    # #      'height': 400,
    # #  })

    # # Create the bar chart
    # goalkeeper_chart = alt.Chart(df_filtered_player.sort_values('Total Points', ascending=False).reset_index(drop=True).head(5)).mark_bar().encode(
    #     x=alt.X('Player Name', sort=alt.EncodingSortField('Gameweek'), axis=alt.Axis(labelAngle=0)),
    #     y=alt.Y('Total Points'),
    #     fill=alt.Fill('Position:N', scale=alt.Scale(domain=list(pos_colors.keys()), range=list(pos_colors.values()))),
    #     tooltip=[
    #         'Player Name',
    #         'Price'
    #     ]
    # ).configure_axis(grid=False)
    # st.altair_chart(goalkeeper_chart, use_container_width=True, theme="streamlit")
 
    
    # st.markdown('### Goals')
    # st.vega_lite_chart(df_filtered_player.sort_values('Total Goals', ascending=False).reset_index(drop=True).head(5), {
    #      'mark': {'type': 'bar', 'tooltip': True},
    #      'encoding': {
    #          'x': {'field': 'Total Goals', 'type': 'quantitative'},
    #          'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
    #          'color': pos_color_scale,
    #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    #      },
    #      'width': 800,
    #      'height': 400,
    #  })
    
    # st.markdown('### Assists')
    # st.vega_lite_chart(df_filtered_player.sort_values('Total Assists', ascending=False).reset_index(drop=True).head(5), {
    #      'mark': {'type': 'bar', 'tooltip': True},
    #      'encoding': {
    #          'x': {'field': 'Total Assists', 'type': 'quantitative'},
    #          'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
    #          'color': pos_color_scale,
    #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    #      },
    #      'width': 800,
    #      'height': 400,
    #  })
    
    # st.markdown('### Bonus')
    # st.vega_lite_chart(df_filtered_player.sort_values('Total Bonus', ascending=False).reset_index(drop=True).head(5), {
    #      'mark': {'type': 'bar', 'tooltip': True},
    #      'encoding': {
    #          'x': {'field': 'Total Bonus', 'type': 'quantitative'},
    #          'y': {'field': 'Player Name', 'type': 'nominal', 'sort': '-y'},
    #          'color': pos_color_scale,
    #          'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
    #      },
    #      'width': 800,
    #      'height': 400,
    #  })
    
    # Cost vs 22/23 Season Points chart
    st.markdown('### Cost vs 22/23 Season Points')
    st.markdown('##### ***Identify Low Price Player With High Points Return***')
    st.vega_lite_chart(df_filtered_player, {
         'mark': {'type': 'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Price', 'type': 'quantitative'},
             'y': {'field': 'Total Points', 'type': 'quantitative'},
             'color': {'field': 'Position', 'type': 'nominal'},
             'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Points', 'type': 'quantitative'}],
         },
         'width': 800,
         'height': 400,
     })

    # Goals per 90 chart
    st.markdown('### Goals per 90')
    st.markdown('##### ***Player Total Goals, Assists and Points per 90 Minutes***')
    st.vega_lite_chart(df_filtered_player, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'Total Goals P90', 'type': 'quantitative'},
         'y': {'field': 'Total Assists P90', 'type': 'quantitative'},
         'color': {'field': 'Position', 'type': 'nominal'},
         'tooltip': [{"field": 'Player Name', 'type': 'nominal'}, {'field': 'Price', 'type': 'quantitative'}, {'field': 'Total Goals P90', 'type': 'quantitative'}, {'field': 'Total Assists P90', 'type': 'quantitative'}, {'field': 'Total Points P90', 'type': 'quantitative'}],
     },
     'width': 800,
     'height': 400,
    })
    
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
    
    
    

