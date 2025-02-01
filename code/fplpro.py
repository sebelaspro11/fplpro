import streamlit as st
from streamlit_option_menu import option_menu
from analysis import perform_analysis
from pointfix import perform_point_fixture
from formdiff import perform_formdiff
from history import perform_history
from history import perform_history
from manager import perform_manager
from predict import perform_predict




# Page Configuration
page_title = "Fantasy Premier League Analytics"
page_icon = ":bar_chart:"  # Emoji Icon
layout = "wide"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# ✅ Center Title Using HTML & CSS
st.markdown(
    f"""
    <h1 style="text-align: center;">{page_title} 📊</h1>
    """,
    unsafe_allow_html=True
)

st.write(
    '<div style="position: absolute; bottom: 110px; right: 4px; opacity: 0.15;">Powered by Sebelaspro</div>',
    unsafe_allow_html=True
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Analytics", "Points & Fixture", "Scouting",  "FPL History", "Manager Details",  "About"],
    icons=["bi-file-earmark-bar-graph-fill", "bi-calendar-check",  "bi-bullseye",  "bi-clock-history", "bi-person-circle",  "bi-card-list"], # https://icons.getbootstrap.com/
    orientation="horizontal",
)


if selected == "Analytics":
    perform_analysis()
 
 
  
if selected == "Points & Fixture":
    perform_point_fixture()
    
        
        
if selected == "Scouting":
    perform_formdiff()
    
    

    

if selected == "Manager Details":
    perform_manager()

    
if selected == "FPL History":
    perform_history()

    
    
if selected == "About":
    perform_predict()
