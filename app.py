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

#https://media.tenor.com/rrLadwcIvTIAAAAM/unicorn-magic.gif
magicEnabled = True

st.set_page_config(page_title='How''s Goin', page_icon='💬', layout='wide', 
                   initial_sidebar_state='collapsed')


# --- USER AUTHENTICATION ---

# load usernames and passwords into mem
file_path = Path(__file__).parent / 'config.yaml'
with file_path.open('r') as file:
    config = yaml.safe_load(file)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#Creating tabs for login and registration widgets
login, register = st.tabs(['Login', 'Registration'])

with login:
    name, authentication_status, username = authenticator.login("Login", "main")

with register:
   try:
       if authenticator.register_user('Register user', preauthorization=False):
           st.success('User registered successfully')
           with file_path.open('w') as file:
               yaml.dump(config, file, default_flow_style=False)
   except Exception as e:
       st.error(e)

   
#LUser Login Checks
if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    cf.switch_page('conversations')

