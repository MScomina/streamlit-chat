# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:09:27 2022

@author: Michele
"""

from streamlit import session_state
import sqlite3
from sqlite3 import Error


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
        __conn = sqlite3.connect(r"database.db",check_same_thread=False)
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
        __conn.execute('''CREATE TABLE IF NOT EXISTS utenti (
            "USERNAME" VARCHAR(50) PRIMARY KEY,
            "MAIL" VARCHAR(75) UNIQUE NOT NULL,
            "NAME" VARCHAR(50) NOT NULL,
            "PASSWORD" VARCHAR(255) NOT NULL,
            "ISADMIN" BOOLEAN NOT NULL DEFAULT 0
            );''')
        __conn.execute('''CREATE TABLE IF NOT EXISTS messaggi (
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
            

#   Inserisce un utente/admin nel database. Nel caso un utente con lo stesso nome esista già il comando verrà ignorato.
#   Formato: [utente, mail, nome, password]
def insert_user(data, isAdmin=False):
    try:
        __conn.execute('''INSERT INTO utenti (USERNAME, MAIL, NAME, PASSWORD, ISADMIN) VALUES (?,?,?,?,?) ON CONFLICT DO NOTHING;''', (*data,isAdmin))
        __conn.commit()
    except Error as e:
        print(e)
    
    
#   Recupera i dati di un utente tramite lo username, None se non esiste.
def retrieve_user(name):
    cursor = __conn.execute('''SELECT username,mail,name,password,isAdmin FROM utenti WHERE username=? LIMIT 1;''', (name,))
    data = None
    for row in cursor:
        data = row
    return data


#   Salva un messaggio nel database. Data è un array di stringhe contenenti rispettivamente chi lo ha inviato, chi lo ha ricevuto e il messaggio.
#   Formato: [sender, receiver, message]
#   ATTENZIONE, GLI UTENTI DEVONO ESISTERE NEL DATABASE!
def save_message(data):
    try:
        __conn.execute('''INSERT INTO messaggi (SENDER, RECEIVER, MESSAGE) VALUES (?,?,?);''', (*data,))
        __conn.commit()
    except Error as e:
        print(e)
    
    
#   Recupera gli ultimi number (default 100) messaggi della chat dal database (sia ricevuta che inviata), ordinata in base al timestamp (dalla più recente alla più vecchia).
#   Formato: [sender, receiver, message, timestamp]
def retrieve_chat(name, specific=None, number=100):
    cursor = None
    if specific==None:
        cursor = __conn.execute('''SELECT sender,receiver,message,timestamp FROM messaggi WHERE sender=? OR receiver=? ORDER BY timestamp DESC LIMIT ?;''',(name,name,number))
    else:
        cursor = __conn.execute('''SELECT sender,receiver,message,timestamp FROM messaggi WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?) ORDER BY timestamp DESC LIMIT ?''',(name,specific,specific,name,number))
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
        c.executemany('''INSERT INTO messaggi (sender, receiver, message) VALUES (?,?,?);''', data)
        __conn.commit()
    except Error as e:
        print(e)
        
        
#   Elimina un utente all'interno del database.
#   ATTENZIONE, QUESTA OPERAZIONE NON E' REVERSIBILE!
def delete_user(name):
    try:
        __conn.execute('''DELETE FROM utenti WHERE username=? LIMIT 1;''', name)
        __conn.commit()
    except Error as e:
        print(e)
        
        
#   Rimuove un utente dalla lista ban.
def unban_user(name):
    try:
        __conn.execute('''DELETE FROM ban WHERE user=? LIMIT 1;''', name)
        __conn.commit()
    except Error as e:
        print(e)
        
        
#   Imposta il valore admin a un utente. Può rimuovere o aggiungere admin (valori 0 o 1).
def set_admin(name, value):
    try:
        __conn.execute('''UPDATE utenti SET isAdmin=? WHERE username=? LIMIT 1;''', (value,name))
        __conn.commit()
    except Error as e:
        print(e)
        
        
#   Restituisce 1 se il nome è quello di un admin, 0 se non lo è, None se l'utente non è stato trovato.
def is_admin(name):
    out = __conn.execute('''SELECT isAdmin FROM utenti WHERE username=? LIMIT 1;''', name)
    data = None
    for row in out:
        data = row[0]
    return data


#   Restituisce il momento dell'ultima interazione fatta da un utente con tutti gli altri utenti.
def get_last_interactions(name):
    out = __conn.execute('''SELECT receiver, max(timestamp) AS timestamp FROM (SELECT receiver,timestamp FROM (SELECT receiver,timestamp,row_number() OVER(PARTITION BY receiver ORDER BY timestamp DESC) AS rn FROM messaggi WHERE sender=?) t1 WHERE t1.rn=1
                            UNION
                            SELECT sender as receiver,timestamp FROM (SELECT sender,timestamp,row_number() OVER(PARTITION BY receiver ORDER BY timestamp DESC) AS rn FROM messaggi WHERE receiver=?) t2 WHERE t2.rn=1)
                            GROUP BY receiver ORDER BY timestamp DESC''', (name,name))
    data = []
    for row in out:
        data.append(row)
    return data


#   Modifica i dati di un utente all'interno del database.
#   Formato data: [mail, nome, password]
def edit_user(name, data):
    try:
        __conn.execute('''UPDATE utenti SET mail=?, name=?, password=? WHERE username=? LIMIT 1''', (*data, name))
        __conn.commit()
    except Error as e:
        print(e)


#   Controlla se un utente è bannato e ritorna una ragione.
def is_banned(name):
    out = __conn.execute('''SELECT reason FROM ban WHERE user=? LIMIT 1;''', name)
    data = (False, "")
    for row in out:
        data = (True, row[0])
    return data
