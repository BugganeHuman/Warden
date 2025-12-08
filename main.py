import operations
import logics
import customtkinter

def main():
    while True:
        master_key_input = None
        if not logics.salt_exists():
            master_key_input = input("Write password for create your master key, "
                            "minimum 10 chapters\n: ")
        else:
            master_key_input = input("write master key: ")
        if logics.start(master_key_input):
            break

    def show():
        index = 0
        for element in operations.show_elements():
            print(f"\n{index} link = {element[0]} | login = {"*" * len(element[1])}"
                f" | password =  {"*" * len(element[2])}\n")
            index += 1
    while True:
        show()
        choice = input("\nwrite number:\n\n"
                       "0 - to exit\n\n"
                       "1 - watch full some element\n\n"
                       "2 - operations with elements\n\n"
                       "3 - generate password: ")

        if choice == "0":
            break
        elif choice == "1":
            choice_element = input("\nwrite number of element to watch full: ")
            list_of_element = operations.show_element_secret_data(int(choice_element))
            print(f"\n\nlink = {list_of_element[0]} | login = {list_of_element[1]}"
                f" | password = {list_of_element[2]}\n\n")
            input()
        elif choice == "2":
            while True:
                show()
                choice_operation = input("\nwrite number:\n\n"
                                     "0 - to return\n\n"
                                     "1 - to create new element\n\n"
                                     "2 - to update element\n\n"
                                     "3 - to delete element\n\n"
                                     "4 - to find element: ")
                if choice_operation == "0":
                    break

                elif choice_operation == "1":
                    operations.create_element(input("\nwrite link: "),
                                              input("\nwrite login: "),
                                              input("\nwrite password: "))
                    print("\ndone\n")
                elif choice_operation == "2":
                    operations.update_element(int(input
                                    ("\nwrite index of updating element: ")),
                                              input("\nwrite new link: "),
                                              input("\nwrite new login: "),
                                              input("\nwrite new password: "))
                    print("\ndone\n")
                elif choice_operation == "3":
                    try:
                        operations.delete_element(int(input(
                            "write index of deleting element: "
                        )))
                    except Exception as e:
                        print(e)
                elif choice_operation == "4":
                    result = operations.find_element(input("\nwrite text of link: "))
                    if result:
                        for element in result:
                            print(f"{element[3]} link = {element[0]} login = {'*' * len(element[1])} password = {'*' * len(element[2])}")
                    else:
                        print("nothing found")
                    input()
        elif choice == "3":
            print("\nTo refuse the condition,"
                  " don't write anything and just press Enter\n"
                  "To agree to use, enter any text")
            try:
                passwords =  logics.generate_password(int(input(
                                    "\namount chapters: ")),
                                     input("lower case(abc): "),
                                     input("upper case(ABC): "),
                                     input("numbers(123): "),
                                     input("special symbols(@#&-.,): "))
                for password in passwords:
                   print(f"\n{password}")
                input()
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
    logics.db_close()
