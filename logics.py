import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
from pathlib import Path


# мб эти все переменный надо перевести в хай регистр ибо это константы
conn = sqlite3.connect("vault.db")
cursor = conn.cursor()
path_to_salt = Path("salt.key")
master_password = None
fernet = None
def start(enter_password):
    global master_password
    global fernet
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
        if len(master_password) < 10:
            print("minimal length of password - 10 chapters")
            sys.exit()
        create_salt()
        fernet = Fernet(master_key())
        create_element("test", "test","test")
    fernet = Fernet(master_key())
    try:
        show_elements()
        print("Enter")
    except Exception as e:
        print("incorrect password")
        #print(e)
        return sys.exit()# здесь мб надо сделать что бы спрашивался, 3 раза
                # и только потом закрывался

def create_salt():
    if not path_to_salt.exists():
        salt = os.urandom(16)
        with open("salt.key", 'wb') as file:
            file.write(salt)
            print("crated ",salt)

def master_key():
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
    link_binary = fernet.encrypt(link.encode())
    login_binary = fernet.encrypt(login.encode())
    password_binary = fernet.encrypt(password.encode())
    for element in show_elements():
        if link and login and password in element:
            print("This element already added")
            return
    cursor.execute("INSERT INTO vault (link, login, password) VALUES (?,?,?)",
                (sqlite3.Binary(link_binary),
                            sqlite3.Binary(login_binary),
                            sqlite3.Binary(password_binary)))
    conn.commit()

def show_elements (decrypt = True):
    elements = cursor.execute("SELECT * FROM vault").fetchall()
    elements_decrypt = []
    index = 0
    for record in elements:
        elements_decrypt.append([])
        for element in record:
            if decrypt:
                elements_decrypt[index].append(fernet.decrypt(element).decode())
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

def update_element(index, new_link, new_login, new_password):
    cursor.execute("UPDATE vault set "
                   "link = ?, login = ?, password = ? "
                   "WHERE link = ? AND login = ? AND password = ?", (
                    fernet.encrypt(new_link.encode()),
                    fernet.encrypt(new_login.encode()),
                    fernet.encrypt(new_password.encode()),
                    show_element_secret_data(index, False)[0],
                    show_element_secret_data(index, False)[1],
                    show_element_secret_data(index, False)[2]
    ))
    conn.commit()
    print("done")

def db_close():
    conn.close()

def find_element (link):
    index = 0
    list_found = []
    for element in show_elements():
        if index == 0:
            index += 1
            continue
        finding_link = element[0]
        result = [chapter for chapter in str(finding_link).lower()
                  if str(link).lower() in str(finding_link).lower()]
        if result:
            list_found.append(show_element_secret_data(index))
        index += 1
    return list_found # мб надо добавить что бы возвращались только линки
    # а все остальное через *** и открывалось по запросу

start("password123")
print(find_element("aM"))
#update_element(1, "Apple", "Tim Cock", "orange135")
#delete_element(4)
#create_salt()
#print(show_elements())
#print("NVIDEA" in show_element_secret_data(4))
#create_element("NVIDEA", "chinese dude", "pi333")
#print(show_elements())
#conn.close()
# мб надо придумать как хронить salt в бд вместе с данными
