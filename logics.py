import os
import sys
import hashlib
import base64
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
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS vault (
        link BLOB, 
        login BLOB,
        password BLOB
        )
        """)
    CONN.commit()
    if not salt_exists():
        if not registration(enter_password):
           return False

    try:
        allow_entry = check_hash(enter_password)
        if allow_entry:
            print("\nEnter permitted")
            return True
        else:
            print("incorrect password")
            global counter_of_enter_password
            counter_of_enter_password += 1
            if counter_of_enter_password > 3:
                pyperclip.copy("")
                sys.exit()
    except Exception as e:
        print(e)

def registration (password):
    if len(password) < 10:
        print("minimal length of password - 10 chapters")
        return False
    create_salt()
    salt = create_salt()
    CURSOR.execute("SELECT iterations FROM meta WHERE flag = 1")
    iterations = CURSOR.fetchone()
    create_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=str(password).encode(),
        salt=salt[0],
        iterations=iterations[0],
        dklen=32
    )
    correct_hash = base64.b64encode(create_hash).decode()
    CURSOR.execute("UPDATE meta set hash = ? WHERE flag = 1", (correct_hash,))
    CONN.commit()
    return True

def check_hash(password):
    global FERNET
    global MASTER_PASSWORD
    MASTER_PASSWORD = master_key(password)
    FERNET = Fernet(MASTER_PASSWORD)
    salt = create_salt()
    CURSOR.execute("SELECT iterations FROM meta WHERE flag = 1")
    iterations = CURSOR.fetchone()
    CURSOR.execute("SELECT hash FROM meta WHERE flag = 1")
    correct_hash = CURSOR.fetchone()[0]
    create_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=str(password).encode(),
        salt=salt[0],
        iterations=iterations[0],
        dklen=32
    )
    return base64.b64encode(create_hash).decode() == correct_hash

def salt_exists():
    CURSOR.execute("SELECT name FROM sqlite_master"
                   " WHERE type='table' AND name='meta'")
    result = bool(CURSOR.fetchone())
    return result

def create_salt():
    if not salt_exists():
        CURSOR.execute("""CREATE TABLE IF NOT EXISTS meta (flag INTEGER,salt BLOB,
                        hash TEXT, iterations INTEGER)
                       """)
        CONN.commit()
        salt = os.urandom(16)
        CURSOR.execute("INSERT INTO meta (flag,salt, iterations)"
                       " VALUES (?,?,?)", (1, salt, 1200000))
        CONN.commit()
    result = CURSOR.execute("SELECT salt FROM meta").fetchall()
    return result[0]

def master_key(password):
    salt = str(create_salt()).encode()
    CURSOR.execute("SELECT iterations FROM meta WHERE flag = 1")
    iterations = CURSOR.fetchone()
    kdf = PBKDF2HMAC (
        salt=salt,
        iterations=iterations[0],
        length=32,
        algorithm=hashes.SHA256(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def db_close():
    CONN.close()

def generate_password (amount = 10, lower_case = False,
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
    return result_list
