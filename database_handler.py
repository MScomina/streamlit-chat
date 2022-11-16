# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:09:27 2022

@author: Michele
"""

import sqlite3
from sqlite3 import Error
from time import time




__conn = None


# Se la connessione esiste, salva i cambiamenti e la chiude, poi imposta la variabile __conn a None.
def close_connection():
    global __conn
    try:
        if __conn != None:
             __conn.commit()
             __conn.close()
             __conn = None
    except Error as e:
        print(e)


#  Crea una connessione col database (chiude e riapre se esiste già).
def create_connection():
    global __conn
    close_connection()
    __conn = None
    try:
        __conn = sqlite3.connect(r"database.db")
    except Error as e:
        print(e)
        
        
#   Salva i cambiamenti al database, se esiste la connessione.
def save_changes():
    global __conn
    if __conn != None:
        __conn.commit()
        

#   Inizializza il database (se non esiste).
def initialize_database():
    try:
        __conn.execute('''CREATE TABLE IF NOT EXISTS utente (
            "USERNAME" VARCHAR(50) PRIMARY KEY,
            "MAIL" VARCHAR(75) UNIQUE NOT NULL,
            "NAME" VARCHAR(50) NOT NULL,
            "PASSWORD" VARCHAR(255) NOT NULL,
            "ISADMIN" BOOLEAN NOT NULL
            );''')
        __conn.execute('''CREATE TABLE IF NOT EXISTS messaggio (
            "ID" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "SENDER" VARCHAR(50) NOT NULL,
            "RECEIVER" VARCHAR(50) NOT NULL,
            "MESSAGE" VARCHAR(4096) NOT NULL,
            "TIMESTAMP" INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(SENDER) REFERENCES utente(USERNAME) ON DELETE CASCADE,
            FOREIGN KEY(RECEIVER) REFERENCES utente(USERNAME) ON DELETE CASCADE
            );''')
        __conn.execute('''CREATE TABLE IF NOT EXISTS ban (
            "USER" VARCHAR(50) PRIMARY KEY REFERENCES utente(USERNAME),
            "ADMIN" VARCHAR(50) REFERENCES utente(USERNAME),
            "REASON" VARCHAR(512) DEFAULT "Sei stato bannato da questo servizio." NOT NULL
            );''')
        insert_user(["1234","1234","1234","$2b$12$NUNa.67YQdya.MIduX/cq.Exj8o59nsXQvVzsZ7X5N4aBOYT7lYla"])
        insert_user(["ciao","ciao","ciao","$2b$12$QaZETOSP8fHxiO63cxAKTehWTiOvxCdm4r.N98VWBn4GOJuvi3d9i"])
        insert_user(["luigi","Luigi","Luigi","$2b$12$0J/uklRLobAx37l4ZY3/K.QtK9uoFAGzEJgB.1AQpHCtgPDuQfBsa"])
        insert_user(["joel","Joel","Joel","$2b$12$a.anduF9S1M0JsZ9k7USJOtZFd4oE5V/Z0Esmmo.5fowSl9V30v5W"])
        insert_user(["asd","asd","asd","$2b$12$dHi5h/RHal0TnK1ZiHgXreerxh01B3m2vSBFl5ZiyJ4JmbLMqaZN2"],isAdmin=True)
        __conn.commit()
    except Error as e:
        print(e)
            

#   Inserisce un utente/admin nel database.
#   Formato: [utente, mail, nome, password]
def insert_user(data, isAdmin=False):
    try:
        __conn.execute('''INSERT INTO utente (USERNAME, MAIL, NAME, PASSWORD, ISADMIN) VALUES (?,?,?,?,?);''', (*data,isAdmin))
        __conn.commit()
    except Error as e:
        print(e)
    
#   Recupera i dati di un utente tramite lo username, None se non esiste.
def retrieve_user(name):
    cursor = __conn.execute('''SELECT username,mail,name,password,isAdmin FROM utente WHERE username=? LIMIT 1;''', (name,))
    data = None
    for row in cursor:
        data = row
    return data

#   Salva un messaggio nel database. Data è un array di stringhe contenenti rispettivamente chi lo ha inviato, chi lo ha ricevuto e il messaggio.
#   Formato: [sender, receiver, message]
#   ATTENZIONE, GLI UTENTI DEVONO ESISTERE NEL DATABASE!
def save_message(data, timestamp=int(time())):
    try:
        __conn.execute('''INSERT INTO messaggio (SENDER, RECEIVER, MESSAGE, TIMESTAMP) VALUES (?,?,?,?);''', (*data,timestamp))
        __conn.commit()
    except Error as e:
        print(e)
    
    
#   Recupera gli ultimi number (default 100) messaggi della chat dal database (sia ricevuta che inviata), ordinata in base al timestamp (dalla più recente alla più vecchia).
#   Formato: [sender, receiver, message, timestamp]
def retrieve_chat(name, number=100):
    cursor = __conn.execute('''SELECT sender,receiver,message,timestamp FROM messaggio WHERE sender=? OR receiver=? ORDER BY TIMESTAMP DESC LIMIT ?;''',(name,name,number))
    data = []
    for row in cursor:
        data.append(row)
    return data

#   Inserisce un utente all'interno della ban list nel database.
def ban_user(user, admin=None, message="Sei stato bannato da questo servizio."):
    try:
        __conn.execute('''INSERT INTO ban (user, admin, message) VALUES (?,?,?);''', (user, admin, message))
        __conn.commit()
    except Error as e:
        print(e)
        

#   Salva messaggi multipli nel database. Data è un array di stringhe contenenti rispettivamente chi lo ha inviato, chi lo ha ricevuto e il messaggio.
#   Formato: [(sender, receiver, message),...]
#   ATTENZIONE, GLI UTENTI DEVONO ESISTERE NEL DATABASE! I MESSAGGI VERRANNO SALVATI CON LO STESSO TIMESTAMP!
def save_messages(data):
    try:
        c = __conn.cursor()
        c.executemany('''INSERT INTO messaggio (SENDER, RECEIVER, MESSAGE) VALUES (?,?,?);''', data)
        __conn.commit()
    except Error as e:
        print(e)