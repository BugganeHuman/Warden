import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3

"""
нужны функции:
start() - создается sqlite файл с полями salt, link, login, password
create_master_key (password) - создается master key с помощью пароля, 
    и соль записывается в бд
create_element(link, login, password) // link может записыватся просто
    как название сайта. шифрует принятые данные используя master key,
    и записывает в sqlite
show_elements (password) - впринципе просто return ит бд, но при этом 
    дешифрует каждый элемент
"""

conn = sqlite3.connect("secret.db")
cursor = conn.cursor()
def start():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
        link BLOB, 
        login BLOB,
        password BLOB
        )
        """)
    conn.commit()

def create_salt():
    salt = os.urandom(16)
    print("crated ",salt)
    with open("salt.key", 'wb') as file:
        file.write(salt)

def master_key(password):
    salt = open("salt.key", 'rb').read()
    kdf = PBKDF2HMAC (
        salt=salt,
        iterations=1_200_000,
        length=32,
        algorithm=hashes.SHA256(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def create_element(link, login, password):
    key = master_key("password")
    fernet = Fernet(key)
    link_binary = fernet.encrypt(link.encode())
    login_binary = fernet.encrypt(login.encode())
    password_binary = fernet.encrypt(password.encode())
    cursor.execute("INSERT INTO secrets (link, login, password) VALUES (?,?,?)",
                   (sqlite3.Binary(link_binary),
                              sqlite3.Binary(login_binary),
                              sqlite3.Binary(password_binary)))
    conn.commit()

def show_elements (password):
    elements = cursor.execute("SELECT * FROM secrets").fetchall()
    fernet = Fernet(master_key(password))
    elements_decrypt = []
    counter = 0
    for record in elements:
        elements_decrypt.append([])
        for element in record:
            elements_decrypt[counter].append(fernet.decrypt(element))
        counter += 1
    print(elements_decrypt)
    return elements_decrypt

start()
#create_salt()
#create_element("amazon", "admin", "password")
print(show_elements("password"))
conn.close()
# мб надо придумать как хронить salt в бд вместе с данными
