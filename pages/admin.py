# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:52:53 2022

@author: pis
"""
import streamlit as st 
import pandas as pd

convos = pd.read_csv('chat.csv')
conversazioni, msgutenti, ban, admin = st.tabs(['Conversazioni','Messaggi utenti',' ban/unban', 'admin'])

#Controlla la lista dei messaggi e controlla quali sono gli utenti
with  conversazioni:
    utente1 = st.selectbox("Utente1", options = convos.loc[:,"Mittente"])
    utente2 = st.selectbox("Utente2", options = convos.loc[:,"Mittente"])
    if st.button('Mostra chat'): #Mostra i messaggi inviati tra i due utenti scelti, se ce ne sono
        tempData = convos[((convos['Mittente'] == utente1) | (convos['Mittente'] ==utente2)) & ((convos['Destinatario'] == utente1) | (convos['Destinatario'] ==utente2)) ]
        st.dataframe(tempData)   
        
