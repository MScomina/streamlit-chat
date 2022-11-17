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
    
def displayChat(u1, u2):
    import pandas as pd
    from streamlit_chat import message
    import database_handler as dh
    df = pd.DataFrame.from_records(dh.retrieve_chat(u1,specific=u2), columns=["Mittente", "Destinatario", "Messaggio", "Timestamp"])
    for i,row in enumerate(df.itertuples()):
        if row.Mittente == u1:
            message(row.Messaggio, is_user=True, avatar_style="avataaars", key=str(i))
        else:
            message(row.Messaggio, avatar_style="micah", key=str(i))
        
def getConv(file_csv):
    import pandas as pd
    df = pd.read_csv(file_csv)
    return df

def isBanned(userData, username):
    return userData['credentials']['usernames'][username].get('banned', False)
        

def isAdmin(userData, username):
    return userData['credentials']['usernames'][username].get('admin', False)