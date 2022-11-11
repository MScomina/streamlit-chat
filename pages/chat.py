import streamlit as st
import streamlit_authenticator as stauth
import csv
import yaml
from pathlib import Path
from datetime import datetime
import custom_functions as cf


file_path = Path(__file__).parent / '../config.yaml'
with file_path.open('r') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
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
elif st.session_state["authentication_status"]:     
    authenticator.logout('Logout', 'main')
    mittente = st.session_state["username"]
    destinatario = st.session_state["destinatario"]
    
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
                with open("chat.csv","a", newline="") as csvfile:       # Scrittura csv
                    writer = csv.writer(csvfile)
                    writer.writerow([datetime.today().strftime('%Y-%m-%d %H:%M:%S'), mittente, destinatario, message])
                
    cf.displayChat(mittente, destinatario) #Chat tra utenti
