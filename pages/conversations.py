#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:42:17 2022

@author: alessandrooddone


"""

import yaml
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

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
    st.session_state['destinatario'] = 'joel'
    cf.switch_page('chat')

    
    

