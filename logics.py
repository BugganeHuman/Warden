import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3
import string
import secrets
import pyperclip


CONN = sqlite3.connect("vault.db")
CURSOR = CONN.cursor()
MASTER_PASSWORD = None
FERNET = None
counter_of_enter_password = 0

def start(enter_password):
    global MASTER_PASSWORD
    global FERNET
    MASTER_PASSWORD = enter_password
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS vault (
        link BLOB, 
        login BLOB,
        password BLOB
        )
        """)
    CONN.commit()
    if not salt_exists():
        if len(MASTER_PASSWORD) < 10:
            print("minimal length of password - 10 chapters")
            return False
        create_salt()
        FERNET = Fernet(master_key())
        CURSOR.execute("UPDATE meta SET test_link = ?, test_login = ?," 
                       " test_password = ?  WHERE flag = 1",
        (FERNET.encrypt("test".encode()), FERNET.encrypt("test".encode()),
                    FERNET.encrypt("test".encode())))
        CONN.commit()
    FERNET = Fernet(master_key())
    try:
        CURSOR.execute("SELECT test_link, test_login, test_password FROM meta")
        test = CURSOR.fetchall()
        test_decrypt = []
        for iteration in test:
            for element in iteration:
                test_decrypt.append(FERNET.decrypt(element))
        if test_decrypt:
            print("Enter")
            pyperclip.copy("")
            return True # это надо что бы удобно обрабатывать в интерфейсе
                    # типо если вход успешный возвращает True
                    # если нет то False
    except Exception:
        print("incorrect password")
        global counter_of_enter_password
        counter_of_enter_password += 1
        if counter_of_enter_password > 3:
            pyperclip.copy("")
            sys.exit()

def salt_exists():
    CURSOR.execute("SELECT name FROM sqlite_master"
                   " WHERE type='table' AND name='meta'")
    result = bool(CURSOR.fetchone())
    return result

def create_salt():
    if not salt_exists():
        CURSOR.execute("""CREATE TABLE IF NOT EXISTS meta (flag INTEGER,salt BLOB,
                        test_link BLOB, test_login BLOB, test_password BLOB)
                       """)
        CONN.commit()
        salt = os.urandom(16)
        CURSOR.execute("INSERT INTO meta (flag,salt)"
                       " VALUES (?,?)", (1, salt))
        CONN.commit()
    result = CURSOR.execute("SELECT salt FROM meta").fetchall()
    return result[0]

def master_key():
    salt = str(create_salt()).encode()
    kdf = PBKDF2HMAC (
        salt=salt,
        iterations=1_200_000,
        length=32,
        algorithm=hashes.SHA256(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD.encode()))
    return key

def create_element(link, login, password):
    link_binary = FERNET.encrypt(link.encode())
    login_binary = FERNET.encrypt(login.encode())
    password_binary = FERNET.encrypt(password.encode())
    for element in show_elements():
        if link in element and login in element and password in element:
            print("This element already added")
            return
    CURSOR.execute("INSERT INTO vault (link, login, password) VALUES (?,?,?)",
                (sqlite3.Binary(link_binary),
                            sqlite3.Binary(login_binary),
                            sqlite3.Binary(password_binary)))
    CONN.commit()

def show_elements (decrypt = True):
    elements = CURSOR.execute("SELECT * FROM vault").fetchall()
    elements_decrypt = []
    index = 0
    for record in elements:
        elements_decrypt.append([])
        for element in record:
            if decrypt:
                elements_decrypt[index].append(FERNET.decrypt(element).decode())
            if not decrypt:
                elements_decrypt[index].append(element)
        index += 1
    return elements_decrypt

def show_element_secret_data(index, decrypt = True):
    return show_elements(decrypt)[index]
def delete_element(index):
    CURSOR.execute("DELETE FROM vault WHERE link = ? AND login = ? AND password = ?"
                   , (show_element_secret_data(index, False)[0],
                   show_element_secret_data(index, False)[1],
                      show_element_secret_data(index, False)[2]))
    CONN.commit()
    print("done")

def update_element(index, new_link, new_login, new_password):
    CURSOR.execute("UPDATE vault set "
                   "link = ?, login = ?, password = ? "
                   "WHERE link = ? AND login = ? AND password = ?", (
                    FERNET.encrypt(new_link.encode()),
                    FERNET.encrypt(new_login.encode()),
                    FERNET.encrypt(new_password.encode()),
                    show_element_secret_data(index, False)[0],
                    show_element_secret_data(index, False)[1],
                    show_element_secret_data(index, False)[2]
    ))
    CONN.commit()
    print("done")

def db_close():
    CONN.close()

def find_element (link):
    index = 0
    index_of_list_found = 0
    list_found = []
    for element in show_elements():
        finding_link = element[0]
        result = [chapter for chapter in str(finding_link).lower()
                  if str(link).lower() in str(finding_link).lower()]
        if result:
            list_found.append(show_element_secret_data(index))
            list_found[index_of_list_found].append(index)
            index_of_list_found += 1
        index += 1
    return list_found

def generate_password (amount, lower_case = False,
                       upper_case = False, numbers = False,
                       special_symbols = False):
    lower_case_all = string.ascii_lowercase
    upper_case_all = string.ascii_uppercase
    numbers_all = string.digits
    special_symbols_all = string.punctuation
    result_list_chapters = []
    if lower_case:
        result_list_chapters.append(lower_case_all)
    if upper_case:
        result_list_chapters.append(upper_case_all)
    if numbers:
        result_list_chapters.append(numbers_all)
    if special_symbols:
        result_list_chapters.append(special_symbols_all)
    result_string_chapters = "".join(result_list_chapters)
    result = ""
    result_list = []
    for password in range(5):
        result = ""
        for i in range(amount):
            result += secrets.choice(result_string_chapters)
        result_list.append(result)
    print(result_list)
    return result_list

#start("password123")
#print(SALT_EXISTS)
#create_salt()
#generate_password(10, True, False, True, )
#print(find_element("a"))
#update_element(1, "SONY", "JapaneseDude", "oop333")
#delete_element(1)
#create_salt()
#print(show_elements())
#print("NVIDEA" in show_element_secret_data(4)
#create_element("Amazon", "JB", "dog0101")
#print(show_elements())
#conn.close()
# мб надо логику как то распределить на несколько файлов,
#   а то в одном уже много
