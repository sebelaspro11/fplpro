
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components






def perform_predict():
    
    st.header(":mailbox: Get In Touch With Me!")
    st.markdown('##### ***Suggestions for any feature improvementsss :keyboard:***')


    contact_form = """
    <form action="https://formsubmit.co/sebelaspro11@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email (Optional)">
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("css/style.css")
    
    # st.markdown(f'### Match Prediction from FiveThirtyEight.com')
    # st.markdown(f'##### ***Prediction For League Standings & Upcoming Matches***')
    # # with st.echo():
    # #     st.write(f"streamlit version: {st.__version__}")

    # # embed streamlit docs in a streamlit app
    # components.iframe("https://projects.fivethirtyeight.com/soccer-predictions/premier-league/", width=1500, height=2000, scrolling=True)
    
    
    
