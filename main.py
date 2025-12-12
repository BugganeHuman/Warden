import operations
import logics
import customtkinter


def main():
    app = customtkinter.CTk()
    app.geometry("1000x800")
    app.title("Warden")
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")
    app.resizable(False, False)
    frame_start = customtkinter.CTkFrame(app)
    frame_vault = customtkinter.CTkFrame(app)
#___________________________________________________________________

    check_entry = customtkinter.CTkEntry(frame_start, placeholder_text="Enter Password",
                            width=500, height=50, font=("Verdana", 44), show="*" )

    check_btn = customtkinter.CTkButton(frame_start,text="Enter",command=lambda :
        start(check_entry.get()), width=50, height=50, font=("Verdana", 34))

    check_label = customtkinter.CTkLabel(frame_start, text="", width=300,
                    height=50, font=("Verdana", 44))
    check_entry.bind("<Return>", lambda event : start(check_entry.get()))
    check_entry.place(x=220, y=350)
    check_btn.place(x=730, y=352)
    check_label.place(x=270, y=420)



    #______________________________________________________________
    generate_password_btn = customtkinter.CTkButton(frame_vault,
            text="generate\npassword", width=150, height=50, font=("Verdana", 30),
                                    fg_color="forestgreen", text_color="ivory" )
    generate_password_btn.place(x=700, y=10)

    elements_frame = customtkinter.CTkScrollableFrame(frame_vault, width=1000, height=900)

    index = 0
    row = 0
    for element in operations.show_elements():
        index_label = customtkinter.CTkLabel(elements_frame, text=str(index), font= ("Verdana", 25), text_color="ivory")
        index_label.grid(row=row, column=0)
        link_label = customtkinter.CTkLabel(elements_frame, text=element[0], font= ("Verdana", 25), text_color="ivory")
        link_label.grid(row=row, column=1, padx=10)
        login_label = customtkinter.CTkLabel(elements_frame, text='*' * len(element[1]), font= ("Verdana", 25), text_color="ivory")
        login_label.grid(row=row, column=2, padx=10)
        password_label = customtkinter.CTkLabel(elements_frame, text='*' * len(element[2]), font= ("Verdana", 25), text_color="ivory" )
        password_label.grid(row=row, column=3, padx=10)
        row += 1
        index += 1
    #______________________________________________________________
    def start(password):
        nonlocal check_label
        nonlocal check_entry
        check_entry.delete(0, "end")
        if logics.start(password):
            check_label.configure(text="Enter permitted")
            show_vault_frame()
        else:
            check_label.configure(text="Incorrect password")

    def show_start_frame(): # можно добавить функцию просмотра пароля,
                    # пока нажата кнопка, а когда отпукаешь все блюрется
        frame_start.pack(fill="both", expand=True)
        # так же можно добавить функцию смены темы


    def show_vault_frame(): # надо будет заполнить его
        frame_start.pack_forget()
        frame_vault.pack(fill="both", expand=True)
        elements_frame.place(x=0, y=100)
    show_start_frame()

    app.mainloop()

#_____________________________________________________________________

if __name__ == "__main__":
    main()
    logics.db_close()
