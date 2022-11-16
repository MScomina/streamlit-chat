# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:52:53 2022

@author: pis
"""
import streamlit as st 
import pandas as pd
import yaml
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import custom_functions as cf


# load usernames and passwords into mem
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
elif st.session_state["authentication_status"] and cf.isAdmin(config, st.session_state["username"]):  
    authenticator.logout('Logout', 'main')
    
    
    
    convos = pd.read_csv('chat.csv')
    file_path = Path(__file__).parent / '../config.yaml'
    with file_path.open('r') as file:
        config = yaml.safe_load(file)
    utenti=config['credentials']['usernames']
    conversazioni, msgutenti, ban, admin = st.tabs(['Conversazioni','Messaggi utenti',' ban/unban', 'admin'])
    
    #Controlla la lista dei messaggi e controlla quali sono gli utenti
    #Praticamente controlla se in un messaggio ci sono come mittente o destinatario uno dei 2 utenti
    #Potrebbero esserci problemi nel caso possiamo far mandare messaggi a se stessi
    with  conversazioni:
        utente1 = st.selectbox("Utente1", options = utenti.keys())
        utente2 = st.selectbox("Utente2", options = utenti.keys())
        if st.button('Mostra chat'): #Mostra i messaggi inviati tra i due utenti scelti, se ce ne sono
            tempData = convos[((convos['Mittente'] == utente1) | (convos['Mittente'] ==utente2)) & ((convos['Destinatario'] == utente1) | (convos['Destinatario'] ==utente2)) ]
            st.dataframe(tempData)   
    #Controlla messaggi singolo utente
    with msgutenti:
                utente = st.selectbox("Utente", options = utenti.keys())
                if st.button('Mostra messaggi'):
                    messaggi= convos[convos['Mittente']==utente]
                    st.dataframe(messaggi)
                    
    #Ban o Unban
    with ban:
            utenteBan = st.selectbox("Seleziona un utente", options = utenti.keys())
            col1, col2 = st.columns([1,1], gap='medium')
            with col1:
                if st.button('Banna utente'):
                    st.write(utenteBan, 'bannato')
                    config['credentials']['usernames'][utenteBan].update(banned=True)
                    with file_path.open('w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    
            with col2:
                if st.button('Sbanna utente'):
                    st.write(utenteBan, 'sbannato')
                    config['credentials']['usernames'][utenteBan].update(banned=False)
                    with file_path.open('w') as file:
                        yaml.dump(config, file, default_flow_style=False)
    
    #Creazione Admin
    with admin:
        utenteAdmin = st.selectbox("Seleziona un utente da rendere admin", options = utenti.keys())
        colA, colB = st.columns([1,1], gap='medium')
        with colA:
            if st.button('Rendi utente un admin'):
                st.write(utenteAdmin, 'è ora un admin')
                config['credentials']['usernames'][utenteAdmin].update(admin=True)
                with file_path.open('w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        with colB:        
            if st.button('Togli a utente privilegi admin'):
                st.write(utenteAdmin, 'non è più un admin')
                config['credentials']['usernames'][utenteAdmin].update(admin=False)
                with file_path.open('w') as file:
                    yaml.dump(config, file, default_flow_style=False)
