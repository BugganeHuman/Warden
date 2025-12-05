import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
from pathlib import Path


conn = sqlite3.connect("vault.db")
cursor = conn.cursor()
path_to_salt = Path("salt.key")
master_password = None

def start(enter_password):
    global master_password
    master_password = enter_password
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
        link BLOB, 
        login BLOB,
        password BLOB
        )
        """)
    conn.commit()
    if not path_to_salt.exists():
        if len(master_password) < 11:
            print("minimal length of password - 10 chapters")
            sys.exit()
        create_salt()
        create_element("test", "test","test")
    try:
        show_elements()
        print("Enter")
    except Exception as e:
        print("incorrect password")
        return sys.exit()# здесь мб надо сделать что бы спрашивался, 3 раза
                # и только потом закрывался

def create_salt():
    if not path_to_salt.exists():
        salt = os.urandom(16)
        with open("salt.key", 'wb') as file:
            file.write(salt)
            print("crated ",salt)

def master_key(): # надо убрать pas
    salt = open("salt.key", 'rb').read()
    kdf = PBKDF2HMAC (
        salt=salt,
        iterations=1_200_000,
        length=32,
        algorithm=hashes.SHA256(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def create_element(link, login, password):
    key = master_key()
    fernet = Fernet(key)
    link_binary = fernet.encrypt(link.encode())
    login_binary = fernet.encrypt(login.encode())
    password_binary = fernet.encrypt(password.encode())
    #надо сделать что бы не добавлялись дубликаты
    cursor.execute("INSERT INTO vault (link, login, password) VALUES (?,?,?)",
                   (sqlite3.Binary(link_binary),
                              sqlite3.Binary(login_binary),
                              sqlite3.Binary(password_binary)))
    conn.commit()

def show_elements (decrypt = True):
    elements = cursor.execute("SELECT * FROM vault").fetchall()
    fernet = Fernet(master_key())
    elements_decrypt = []
    index = 0
    for record in elements:
        elements_decrypt.append([])
        for element in record:
            if decrypt:
                elements_decrypt[index].append(fernet.decrypt(element))
            if not decrypt:
                elements_decrypt[index].append(element)
        index += 1
    return elements_decrypt

def show_element_secret_data(index, decrypt = True):
    return show_elements(decrypt)[index]

def delete_element(index):
    cursor.execute("DELETE FROM vault WHERE link = ? AND login = ? AND password = ?"
                   , (show_element_secret_data(index, False)[0],
                   show_element_secret_data(index, False)[1],
                      show_element_secret_data(index, False)[2]))
    conn.commit()
    print("done")


#start("password123")
#delete_element(1)
#create_salt()
#create_element("Microsoft", "Bill Gates", "poop444")
#print(show_elements())
#conn.close()
# мб надо придумать как хронить salt в бд вместе с данными
