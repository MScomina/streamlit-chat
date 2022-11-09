#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:42:17 2022




"""

import yaml
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import numpy as np

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
    
    title = mittente.capitalize() + "'s conversation"
    
    st.title(title)

    with st.expander("New Chat"):
        user = st.text_input('Enter an username', '')
        if st.button('Create'):
            st.session_state['destinatario'] = user
            cf.switch_page('chat')

    file_csv = 'chat.csv'
    x=cf.getConv(file_csv)
    m=np.array(x)
    
    
    contacts=[]
    
    for i in range(0,len(m)):
        if m[i][1]==mittente:
            if(m[i][2] not in contacts):
                contacts.append(m[i][2])
        if m[i][2]==mittente:
            if(m[i][1] not in contacts):
                contacts.append(m[i][1])
         
    
    for i in range(0,len(contacts)):
        if st.button(contacts[i]):
            st.session_state['destinatario'] = contacts[i]
            cf.switch_page('chat')
    