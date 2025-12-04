import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
"""
password = b"zalupa335"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_200_000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
fernet = Fernet(key)
with open ("test.txt", 'w+') as file:
    token = fernet.encrypt(b"secret text?")
    file.write(str(token))
"""
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
    #cursor.execute("INSERT INTO secrets (salt) VALUES (?)", (sqlite3.Binary(salt),))
    with open("salt.key", 'wb') as file:
        file.write(salt)

def master_key(password):
    #salt = cursor.execute("SELECT salt FROM secrets").fetchone()
    #salt = salt[0]
    salt = open("salt.key", 'rb').read()


    print("start")
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
    print(login_binary, link_binary, password_binary)
    cursor.execute("INSERT INTO secrets (link, login, password) VALUES (?,?,?)",
                   (sqlite3.Binary(link_binary),
                              sqlite3.Binary(login_binary),
                              sqlite3.Binary(password_binary)))
    conn.commit()

def show_elements (password):
    elements = cursor.execute("SELECT * FROM secrets").fetchall()
    fernet = Fernet(master_key(password))
    for record in elements:
        for element in record:
            print(element)
            d = fernet.decrypt(element) # bug
            print(d)



start()
create_salt()
create_element("fucking", "pig", "d123")
show_elements("password")
conn.close()
