import logics
import customtkinter
from pathlib import Path

def main():
    master_key_input = None
    if not Path("salt.key").exists():
        master_key_input = input("Write password for create your master key, "
                            "minimum 10 chapters\n: ")
    else:
       master_key_input = input("write master key: ")
    logics.start(master_key_input)
    index = 0
    for element in logics.show_elements():
        if index == 0:
            index += 1
            continue
        print(f"{index} link = {element[0]} | login = {"*" * len(element[1])} | password =  {"*" * len(element[2])}")
        index += 1
    choice_element = input("\nwrite number of element to watch full: ")
    list_of_element = logics.show_element_secret_data(int(choice_element))
    print(f"link ={list_of_element[0]} | login = {list_of_element[1]} | password = {list_of_element[2]}")

if __name__ == "__main__":
    main()
    logics.db_close()
