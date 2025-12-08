import logics
import sqlite3
from logics import CURSOR, CONN


def create_element(link, login, password):
    link_binary = logics.FERNET.encrypt(link.encode())
    login_binary = logics.FERNET.encrypt(login.encode())
    password_binary = logics.FERNET.encrypt(password.encode())
    for element in show_elements():
        if link in element and login in element and password in element:
            print("This element already added")
            return
    logics.CURSOR.execute("INSERT INTO vault (link, login, password) VALUES (?,?,?)",
                (sqlite3.Binary(link_binary),
                            sqlite3.Binary(login_binary),
                            sqlite3.Binary(password_binary)))
    logics.CONN.commit()

def show_elements (decrypt = True):
    elements = CURSOR.execute("SELECT * FROM vault").fetchall()
    elements_decrypt = []
    index = 0
    for record in elements:
        elements_decrypt.append([])
        for element in record:
            if decrypt:
                elements_decrypt[index].append(logics.FERNET.decrypt(element).decode())
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
                    logics.FERNET.encrypt(new_link.encode()),
                    logics.FERNET.encrypt(new_login.encode()),
                    logics.FERNET.encrypt(new_password.encode()),
                    show_element_secret_data(index, False)[0],
                    show_element_secret_data(index, False)[1],
                    show_element_secret_data(index, False)[2]
    ))
    CONN.commit()
    print("done")

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