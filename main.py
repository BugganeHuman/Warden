import logics
import customtkinter

def main():
    master_key_input = input("write master key: ")
    logics.start(master_key_input)
    index = 0
    for element in logics.show_elements():
        if index == 0:
            index += 1
            continue
        print(f"{index} link = {element[0]} | login = {"*" * len(element[1])} | password =  {"*" * len(element[2])}")
        index += 1

if __name__ == "__main__":
    main()

