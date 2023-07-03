
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components





def perform_predict():
    st.markdown(f'### Match Prediction from FiveThirtyEight.com')
    st.markdown(f'##### ***Prediction For League Standings & Upcoming Matches***')
    # with st.echo():
    #     st.write(f"streamlit version: {st.__version__}")

    # embed streamlit docs in a streamlit app
    components.iframe("https://projects.fivethirtyeight.com/soccer-predictions/premier-league/", width=1500, height=2000, scrolling=True)
    