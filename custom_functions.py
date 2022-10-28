#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:42:17 2022

@author: alessandrooddone


"""
#@author blackary

def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")
    
def displayChat(u1, u2, ph):
    import streamlit as st
    import pandas as pd
    ph.empty()
    df = pd.read_csv("chat.csv", usecols=["Mittente", "Destinatario", "Messaggio"]).loc[((pd.read_csv("chat.csv")["Mittente"]==u1)&(pd.read_csv("chat.csv")["Destinatario"]==u2))|((pd.read_csv("chat.csv")["Mittente"]==u2)&(pd.read_csv("chat.csv")["Destinatario"]==u1))]
    with ph.container():
        st.table(df)