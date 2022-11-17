import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path
import custom_functions as cf
from PIL import Image
import database_handler as dh

dh.create_connection()
dh.initialize_database()
dh.initialize_session_state()
    
im = Image.open("logo.png")
st.set_page_config(page_title='How''s Goin', page_icon=im, layout='wide',
                   initial_sidebar_state='collapsed')

file_path = Path(__file__).parent / '../config.yaml'
with file_path.open('r') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    st.session_state["dbcredentials"],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
    cf.switch_page('app')
elif st.session_state["authentication_status"] == None:
    st.warning('You are not logged in.')
    cf.switch_page('app')
elif st.session_state["authentication_status"] and dh.is_banned(st.session_state["username"])[0]: 
    cf.switch_page('app')
elif st.session_state["authentication_status"] and not dh.is_banned(st.session_state["username"])[0]:  
    authenticator.logout('Logout', 'main')
    mittente = st.session_state["username"]
    try:
        destinatario = st.session_state["destinatario"]
    except:
        cf.switch_page('conversations')
    
    if st.button("Back to conversations"):
        cf.switch_page("conversations")
    
    st.title("Chat")
    
    with st.form("Message", clear_on_submit = True):
        message = st.text_input("Insert a message:")
        submitted = st.form_submit_button("Send")
        if submitted:
            if message == "":
                st.error("Can't send empty messages!")      # In caso si cercasse di inviare un messaggio vuoto
            else:
                dh.save_message([mittente, destinatario, message])
                
    cf.displayChat(mittente, destinatario) #Chat tra utenti
