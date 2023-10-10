import streamlit as st
from streamlit_option_menu import option_menu
from analysis import perform_analysis
from pointfix import perform_point_fixture
from formdiff import perform_formdiff
from history import perform_history
from history import perform_history
from manager import perform_manager
from predict import perform_predict


page_title = "Fantasy Football Analyzer"
page_icon = ":bar_chart:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
#st.markdown('##### *****Powered by Sebelaspro*****')
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
st.write(
    '<div style="position: absolute; bottom: 25px; right: 4px; opacity: 0.2;">Powered by Sebelaspro</div>',
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
    options=["Analysis", "Points & Fixture", "In-Form & Differential Player", "FPL History", "Manager Details", "Feedback"],
    icons=["bi-magic", "bi-file-earmark-bar-graph-fill", "bi-capslock", "bi-clock-history", "bi-person-circle", "bi-card-list"], # https://icons.getbootstrap.com/
    orientation="horizontal",
)


if selected == "Analysis":
    perform_analysis()
 
 
  
if selected == "Points & Fixture":
    perform_point_fixture()
    
        
        
if selected == "In-Form & Differential Player":
    perform_formdiff()
    
    

    
if selected == "FPL History":
    perform_history()

if selected == "Manager Details":
    perform_manager()

    
    
    
    
if selected == "Feedback":
    perform_predict()

    
    
    
    

#client.close()
