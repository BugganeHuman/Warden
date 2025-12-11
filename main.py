import operations
import logics
import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title()
        self.geometry("1000x800")
        """
    app = customtkinter.CTk()
    app.geometry("1000x800")
    app.title("Warden")
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")
    frame_start = customtkinter.CTkFrame(app)
    frame_vault = customtkinter.CTkFrame(app)

    check_entry = customtkinter.CTkEntry(frame_start, placeholder_text="Enter Password",
                            width=500, height=50, font=("Verdana", 44), show="*" )

    check_btn = customtkinter.CTkButton(frame_start,text="Enter",command=lambda :
        start(check_entry.get()), width=50, height=50, font=("Verdana", 34))

    check_label = customtkinter.CTkLabel(frame_start, text="", width=300,
                    height=50, font=("Verdana", 44))
    check_entry.bind("<Return>", lambda event : start(check_entry.get()))
    frame_start.grid_rowconfigure((0, 1), weight=1)
    frame_start.grid_columnconfigure((0, 1), weight=1)
    #frame_start.grid_rowconfigure(1, weight=0)
    #frame_start.grid_columnconfigure(1, weight=1)

    check_entry.grid(row=0, column=0, columnspan=2 ) # не работает нихуя
    check_btn.grid(row=0, column=1 )
    check_label.grid(row=1, column=0 )
    #check_btn.place(x=730, y=352)
    #check_label.place(x=320, y=420)

    #______________________________________________________________
    generate_password_btn = customtkinter.CTkButton(frame_vault,
            text="generate\npassword", width=150, height=50, font=("Verdana", 30),
                                    fg_color="forestgreen", text_color="ivory" )
    generate_password_btn.grid(row=1, column=20, padx=500, sticky="n")
    test_list = ["dog", "cat", "elephant", "squirrel", "bear"]
    index = 0
    row = 0
    for element in test_list:
        element_label = customtkinter.CTkLabel(frame_vault, text=element, font= ("Verdana", 25), text_color="ivory")
        index_label = customtkinter.CTkLabel(frame_vault, text=str(index),font= ("Verdana", 25), text_color="ivory" )
        element_label.grid(row=row, column=1)
        index_label.grid(row=row, column=2, padx=10)
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
    show_start_frame()

    app.mainloop()

#_____________________________________________________________________
"""
if __name__ == "__main__":
    app = App()
    app.mainloop()
    logics.db_close()
