#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:42:17 2022




"""

import yaml
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import numpy as np

import custom_functions as cf
import database_handler as dh
from PIL import Image


im = Image.open("logo.png")
st.set_page_config(page_title='How''s Goin', page_icon=im, layout='wide',
                   initial_sidebar_state='collapsed')

dh.create_connection()
dh.initialize_database()
dh.initialize_session_state()
    
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
    
    title = mittente.capitalize() + "'s conversation"
    
    st.title(title)

    #Expander per creare una nuova chat
    with st.expander("New Chat"):
        user = st.text_input('Enter an username', '')
        if st.button('Create'):
            st.session_state['destinatario'] = user.lower()
            cf.switch_page('chat')

    #Recupero dati dal DB
    x=dh.get_last_interactions(mittente)
    m=np.array(x)
    
    #Visualizzazione utenti con cui si ha interagito
    contacts=[]
    timestamp=[]
    
    for i in range(0,len(m)):
        contacts.append(m[i][0])
        timestamp.append(m[i][1])

    for i in range(0,len(contacts)):
        if st.button(contacts[i]+' - '+timestamp[i]):
            st.session_state['destinatario'] = contacts[i]
            cf.switch_page('chat')
    
