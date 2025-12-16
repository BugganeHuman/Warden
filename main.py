import operations
import logics
import customtkinter
from pathlib import Path
import time

def main():
    app = customtkinter.CTk()
    app.geometry("1000x800")
    app.title("Warden")
    if Path("icon.ico").exists():
        app.iconbitmap("icon.ico")
    theme = ""
    try:
        with open("GUE_config.txt", 'r') as file:
            theme = file.read()
            if len(theme) < 3:
                theme = "dark"
    except Exception as error:
        with open("GUE_config.txt", 'w+') as file:
            file.write("light")
        theme = "light"

    customtkinter.set_appearance_mode(theme)
    customtkinter.set_default_color_theme("green")
    app.resizable(False, False)
    frame_start = customtkinter.CTkFrame(app)
    frame_vault = customtkinter.CTkFrame(app)
    elements_frame = customtkinter.CTkScrollableFrame(frame_vault,
        width=1000, height=688)

    time_for_close = 3 * 60
    last_activity = time.time()

    def track_last_activity():
        nonlocal last_activity
        last_activity = time.time()

    def check_activity():
        print(time.time() - last_activity)
        if time.time() - last_activity >= time_for_close:
            app.destroy()
            return
        app.after(1000, check_activity)

    for event in ("<Motion>", "<Button>", "<Key>", "<MouseWheel>"):
        app.bind_all(event, lambda event: track_last_activity())

    check_activity()
#___________________________________________________________________
    if not logics.salt_exists():

        welcome_label = customtkinter.CTkLabel(frame_start,
            text="Welcome to Warden", font=("Verdana", 45))
        welcome_label.place(y = 200, x = 250)

        password_entry_first = customtkinter.CTkEntry(frame_start,
            placeholder_text="write new password", font=("Verdana", 40),
                show="*", width=500, height=50)
        password_entry_first.place(x = 230, y = 280)
        password_entry_first.bind("<Control-v>", "break")
        password_entry_first.bind("<Command-v>", "break")
        password_entry_first.bind("<Button-3>", "break")

        password_entry_second = customtkinter.CTkEntry(frame_start,
            placeholder_text="write password again", font=("Verdana", 40),
                show="*", width=500, height=50)
        password_entry_second.place(x=230, y=350)
        password_entry_second.bind("<Return>", lambda event: registration())
        password_entry_second.bind("<Control-v>", "break")
        password_entry_second.bind("<Command-v>", "break")
        password_entry_second.bind("<Button-3>", "break")

        signup_btn = customtkinter.CTkButton(frame_start, text="sign up",
            font=("Verdana", 35 ), height= 60, width=60, fg_color="forest green",
                command= lambda: registration())
        signup_btn.place(x = 410, y=430)

        def registration():
            if len(password_entry_first.get()) < 10:
                welcome_label.configure(text="minimal length 10", text_color="red")
                password_entry_first.delete(0, "end")
                password_entry_second.delete(0, "end" )
                password_entry_first.configure(show="*")
                password_entry_second.configure(show="*")
            if password_entry_first.get() == password_entry_second.get():
                try:
                    start(password_entry_second.get())
                except Exception as e:
                    make_error(e)
            else:
                welcome_label.configure(text="the passwords don't match",
                    text_color="red")
                password_entry_first.delete(0, "end")
                password_entry_second.delete(0, "end" )
                password_entry_first.configure(show="*")
                password_entry_second.configure(show="*")

    else:
        check_entry = customtkinter.CTkEntry(frame_start,
            placeholder_text="Enter Password", width=500, height=50,
                font=("Verdana", 44), show="*" )

        check_btn_start = customtkinter.CTkButton(frame_start,text="Enter",
            command=lambda :log_in(), width=50, height=50,
                font=("Verdana", 34),fg_color="forest green")

        check_label = customtkinter.CTkLabel(frame_start, text="", width=300,
            height=50, font=("Verdana", 44))
        check_entry.bind("<Return>", lambda event : log_in())
        check_entry.bind("<Control-v>", "break")
        check_entry.bind("<Command-v>", "break")
        check_entry.bind("<Button-3>", "break")
        check_entry.place(x=220, y=350)
        check_btn_start.place(x=730, y=352)
        check_label.place(x=270, y=420)

        def log_in():
            try:
                if start(check_entry.get()):
                    check_label.configure(text="Enter permitted")
                else:
                    check_label.configure(text="Incorrect password")
                check_entry.delete(0, "end")
            except Exception as e:
                make_error(e)


    #______________________________________________________________
    def creat_vault_widgets():
        generate_password_btn = customtkinter.CTkButton(frame_vault,
            text="generate\npassword", width=150, height=50, font=("Verdana", 30),
                fg_color="forestgreen", text_color="ivory",
                    command= lambda : generate_password())
        generate_password_btn.place(x=670, y=10)

        add_link_entry = customtkinter.CTkEntry(frame_vault,
            placeholder_text="new link", width=180, height=80, font=("Verdana", 25))
        add_link_entry.place(x = 5, y = 10)

        add_login_entry = customtkinter.CTkEntry(frame_vault,
            placeholder_text="new login", width=180, height=80, font=("Verdana", 25))
        add_login_entry.place(x=195, y = 10)

        add_password_entry = customtkinter.CTkEntry(frame_vault,
            placeholder_text="new pass", width=180, height=80, font=("Verdana", 25))
        add_password_entry.place(x = 385, y = 10)
        add_password_entry.bind("<Return>", lambda event : add_element())

        add_btn = customtkinter.CTkButton(frame_vault, text="ADD", width=80,
            height=80,font=("Verdana", 30), fg_color="medium slate blue",
                hover_color="dodger blue", command= lambda : add_element())
        add_btn.place(x = 575, y = 10)


        find = customtkinter.CTkButton(frame_vault, text="🔍", font=("Verdana", 60),
                width=50, height=50, fg_color="transparent", text_color= "SteelBlue",
                    hover_color=app.cget("fg_color"), command=lambda : search())
        find.place(x = 835, y = 0)

        theme_chapter = ""
        if customtkinter.get_appearance_mode().lower() == "dark":
            theme_chapter = "🔆"
        else:
            theme_chapter = "🌙"
        change_theme_btn = customtkinter.CTkButton(frame_vault, text=theme_chapter,
            font=("Arial", 60),anchor="center", width=50, height=50,
                text_color=("#55606D", "#BFC4CA"), hover_color=app.cget("fg_color"),
                    fg_color="transparent", command= lambda : change_theme())
        change_theme_btn.place(x=920, y = 5)


        def add_element():
            if add_link_entry.get() and add_login_entry and add_password_entry:
                operations.create_element(add_link_entry.get(),
                    add_login_entry.get(), add_password_entry.get())
                add_link_entry.delete(0, "end")
                add_login_entry.delete(0, "end")
                add_password_entry.delete(0, "end")
                show_elements()

        def change_theme():
            if change_theme_btn.cget("text") == "🔆":
                customtkinter.set_appearance_mode("light")
                change_theme_btn.configure(text="🌙")
                with open("GUE_config.txt", 'w+') as file:
                    file.write("light")
            elif change_theme_btn.cget("text") == "🌙":
                customtkinter.set_appearance_mode("dark")
                change_theme_btn.configure(text="🔆")
                with open("GUE_config.txt", 'w+') as file:
                    file.write("dark")

        def show_elements():
            for widget in elements_frame.winfo_children():
                widget.destroy()
            row = 0
            for element in operations.show_elements():
                link_label_text = element[0]
                if len(link_label_text) > 15:
                    link_label_text = link_label_text[:15] + "..."
                link_label = customtkinter.CTkLabel(elements_frame,
                    text=link_label_text, font= ("Verdana", 30),
                        text_color=("black","ivory"))
                link_label.grid(row=row, column=1, padx=10, pady=10)

                login_label = customtkinter.CTkLabel(elements_frame,
                    text='*******' , font= ("Verdana", 30),
                        text_color=("black","ivory"))
                login_label.grid(row=row, column=2, padx=10, pady=10)

                password_label = customtkinter.CTkLabel(elements_frame,
                    text='*******' , font= ("Verdana", 30),
                        text_color=("black","ivory") )
                password_label.grid(row=row, column=3, padx=10, pady=10)

                check_btn = customtkinter.CTkButton(elements_frame, text="check",
                    font=("Verdana", 20), width=75, height=30, text_color="ivory",
                    fg_color="orange", hover_color= "sienna")
                check_btn.grid(row=row, column=4,  pady=10, padx=20)
                check_btn.configure(command= lambda b=check_btn:
                    check_element(b.grid_info()["row"]))

                delete_btn = customtkinter.CTkButton(elements_frame, text="delete",
                    font=("Verdana", 20), width=75, height=30, text_color="ivory",
                        fg_color="red", hover_color="dark red" )
                delete_btn.grid(row=row, column=5,  pady=10, padx=20 )
                delete_btn.configure(command= lambda b=delete_btn:
                    delete_element(b.grid_info()["row"]))

                update_btn = customtkinter.CTkButton(elements_frame, text="update",
                    font=("Verdana", 20), width=75, height=30, text_color="ivory",
                        fg_color="royal blue", hover_color ="slate blue" )
                update_btn.grid(row=row, column=6,padx=20, pady=10 )
                update_btn.configure(command= lambda b=update_btn:
                    update_element(b.grid_info()["row"]))

                row += 1

        def copy(element):
            app.clipboard_clear()
            app.clipboard_append(element.cget("text"))
            correct_text = element.cget("text")
            element.configure(text="copied")
            app.after(1000, lambda: element.configure(text=correct_text))
            app.after(15000, lambda: (app.clipboard_clear(),
                            app.clipboard_append("")))

        def check_element(index):

            check_modal = customtkinter.CTkToplevel(app)
            check_modal.title("check")
            check_modal.geometry("600x200")
            check_modal.grab_set()
            link = customtkinter.CTkLabel(check_modal,
                text=operations.show_element_secret_data(index)[0],
                    font=("Verdana", 30))
            link.bind("<Button-1>", lambda event: copy(link))
            link.pack(pady=15)
            login = customtkinter.CTkLabel(check_modal,
                text=operations.show_element_secret_data(index)[1],
                    font=("Verdana", 30))
            login.pack(pady=15)
            login.bind("<Button-1>", lambda event: copy(login))
            password = customtkinter.CTkLabel(check_modal,
                text=operations.show_element_secret_data(index)[2],
                    font=("Verdana", 30))
            password.pack(pady=15)
            password.bind("<Button-1>", lambda event: copy(password))

        def delete_element(index):

            delete_modal = customtkinter.CTkToplevel(app)
            delete_modal.title("deleting")
            delete_modal.geometry("400x200")
            delete_modal.grab_set()

            def delete():
                operations.delete_element(index)
                show_elements()
                delete_modal.destroy()

            label = customtkinter.CTkLabel(delete_modal, text="Are you sure?",
                font=("Verdana", 40) )
            label.pack(anchor="center", pady=10)

            yes_btn = customtkinter.CTkButton(delete_modal, text="YES",
                font=("Verdana", 40), width=40, height=40,fg_color="lime green",
                    command= delete)
            yes_btn.pack(side="right", padx=(0, 20))

            no_btn = customtkinter.CTkButton(delete_modal, text="NO",
                font=("Verdana", 40), width=40, height=40, fg_color="red",
                    command=delete_modal.destroy)
            no_btn.pack(side = "left", padx = (20, 0))

        def update_element(index):
            modal_update = customtkinter.CTkToplevel(app)
            modal_update.geometry("500x400")
            modal_update.title("update")
            modal_update.grab_set()

            new_link_entry = customtkinter.CTkEntry(modal_update,
                placeholder_text="write new link", font=("Verdana", 40), width=450,
                    height=50)
            new_link_entry.pack(anchor="center", pady=10)

            new_login_entry = customtkinter.CTkEntry(modal_update,
                placeholder_text="write new login", font=("Verdana", 40), width=450,
                    height=50)
            new_login_entry.pack(anchor="center", pady=10)

            new_password_entry = customtkinter.CTkEntry(modal_update,
                placeholder_text="write new password", font=("Verdana", 40), width=450,
                    height=50)
            new_password_entry.pack(anchor="center", pady=10)

            btn_update = customtkinter.CTkButton(modal_update, text="UPDATE",
                font=("Verdana", 40), width=160, height=60, fg_color="#28A745",
                    command=lambda : update())
            btn_update.pack(anchor="center", pady=30)

            def update():
                if (new_link_entry.get() != "" and
                    new_login_entry.get() != "" and
                    new_password_entry.get() != ""
                    ):
                    operations.update_element(index, new_link_entry.get(),
                        new_login_entry.get(),new_password_entry.get() )
                    show_elements()
                    modal_update.destroy()

        def generate_password():
            modal_gp = customtkinter.CTkToplevel(app)
            modal_gp.geometry("600x600")
            modal_gp.title("generate password")
            modal_gp.grab_set()
            modal_gp.resizable(True, False)

            label_amount = customtkinter.CTkLabel(modal_gp, text="amount chapters - ",
                font=("Verdana", 30))
            label_amount.place(x=60, y=15)

            amount_entry = customtkinter.CTkEntry(modal_gp, font=("Verdana", 40),
                placeholder_text="...", width=130, height=50)
            amount_entry.place(x = 390, y = 10)

            lower_case_var = customtkinter.BooleanVar()
            upper_case_var = customtkinter.BooleanVar()
            numbers_var = customtkinter.BooleanVar()
            special_symbols_var = customtkinter.BooleanVar()

            lower_case_cb = customtkinter.CTkCheckBox(modal_gp, font=("Verdana", 20),
                text="lower case (abc)", variable=lower_case_var,
                    fg_color= "forestgreen")
            lower_case_cb.place(x = 50, y = 90)

            upper_case_cb = customtkinter.CTkCheckBox(modal_gp, font=("Verdana", 20),
                text="upper case (ABC)", variable=upper_case_var,
                    fg_color= "forestgreen")
            upper_case_cb.place(x = 290, y = 90)

            numbers_cb = customtkinter.CTkCheckBox(modal_gp, font=("Verdana", 20),
                text="numbers (123)", variable=numbers_var, fg_color= "forestgreen")
            numbers_cb.place(x = 50, y = 150)

            special_symbols_cb = customtkinter.CTkCheckBox(modal_gp,
                font=("Verdana", 20),text = "special symbols (!?@$)",
                    variable=special_symbols_var, fg_color= "forestgreen")
            special_symbols_cb.place(x = 290, y = 150)

            generate_btn = customtkinter.CTkButton(modal_gp, text="GENERATE",
                fg_color= "forestgreen", font=("Verdana", 30), width=150,
                    height=60, command= lambda : generate())
            generate_btn.place(y = 230, x = 200)
            frame_passwords = customtkinter.CTkFrame(modal_gp,width=2000, height=300)
            frame_passwords.place(x=0, y = 300)

            def generate():
                if (amount_entry.get().isdigit() and lower_case_var.get() or
                    numbers_var.get() or upper_case_var.get() or
                    special_symbols_var.get()):
                    passwords = logics.generate_password(int(amount_entry.get()),
                        lower_case_var.get(), upper_case_var.get(), numbers_var.get(),
                            special_symbols_var.get())
                    for widget in frame_passwords.winfo_children():
                        widget.destroy()
                    y = 5
                    for password in passwords:
                        password = customtkinter.CTkLabel(frame_passwords, text=password,
                            font=("Verdana", 30))
                        password.bind("<Button-1>", lambda event,
                            pas=password: copy(pas))
                        password.place(x = 10, y = y)
                        y += 55

        def search():
            modal_search = customtkinter.CTkToplevel(app)
            modal_search.geometry("700x600")
            modal_search.title("search")
            modal_search.grab_set()

            search_entry = customtkinter.CTkEntry(modal_search, width=500,
                placeholder_text="write searching", height=70, font= ("Verdana", 35))
            search_entry.place(y = 10, x = 60)
            search_entry.bind("<Return>", lambda event: find_element())

            search_btn = customtkinter.CTkButton(modal_search, text="🔍",
                font=("Arial", 60), width=50, height=50, fg_color="transparent",
                    text_color= "SteelBlue", hover_color = "#5CACEE",
                        command= lambda : find_element())
            search_btn.place(y = 10, x = 570)

            frame_find_elements = customtkinter.CTkScrollableFrame(modal_search,
                width=700, height=500)
            frame_find_elements.place(y = 100, x = 0)

            def find_element():
                find_elements = []
                try:
                    find_elements = operations.find_element(search_entry.get())
                except Exception as e:
                    make_error(e)

                for widget in frame_find_elements.winfo_children():
                    widget.destroy()
                row = 0
                for element in find_elements:
                    find_element_label_text = element[0]
                    if len(find_element_label_text) > 15:
                        find_element_label_text = find_element_label_text[:15] + "..."
                    find_element_label = customtkinter.CTkLabel(frame_find_elements,
                        text=find_element_label_text, font=("Verdana", 40), )
                    find_element_label.grid(row = row, column = 0, pady=10, padx=30)

                    find_element_check_btn = customtkinter.CTkButton(frame_find_elements,
                        text="check", font=("Verdana", 20), width=75, height=30,
                            text_color="ivory", fg_color="orange", hover_color="sienna")
                    find_element_check_btn.grid(row = row, column = 1, pady=10, padx=30)
                    find_element_check_btn.configure(command= lambda b=element:
                        check_element(b[3]))

                    row += 1
        try:
            show_elements()
        except Exception as er:
            make_error(er)
    #______________________________________________________________
    def start(password):
        if logics.start(password):
            show_vault_frame()
            creat_vault_widgets()

    def show_start_frame():
        try:
            frame_start.pack(fill="both", expand=True)
        except Exception as e:
            make_error(e)

    def show_vault_frame():
        try:
            frame_start.pack_forget()
            frame_vault.pack(fill="both", expand=True)
            elements_frame.place(x=0, y=100)
        except Exception as e:
            make_error(e)

    def make_error(error):
        modal_error = customtkinter.CTkToplevel(app)
        modal_error.geometry("300x150")
        modal_error.title("error")
        label = customtkinter.CTkLabel(modal_error, text="ERROR",
            font=("Verdana", 30))
        label.pack(side="top", anchor="center")
        label_error = customtkinter.CTkLabel(modal_error, text=error,
            font=("Verdana", 25))
        label_error.pack( pady = 70)


    show_start_frame()
    app.mainloop()



#_____________________________________________________________________

if __name__ == "__main__":
    main()
    logics.db_close()
