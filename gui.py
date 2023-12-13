# gui.py

import tkinter as tk
from practice2 import register, login, login_attempts

class LoginGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login System")

        tk.Button(self, text="Sign Up", command=self.register_window).pack(pady=20)
        tk.Button(self, text="Login", command=self.login_window).pack(pady=20)

    def register_window(self):
        register()

    def login_window(self):
        login_count = 2

        login_window = tk.Toplevel(self)
        login_window.title("Login")

        tk.Label(login_window, text="ID:").grid(row=0, column=0)
        tk.Label(login_window, text="Password:").grid(row=1, column=0)

        id_entry = tk.Entry(login_window)
        password_entry = tk.Entry(login_window, show="*")

        id_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)

        def handle_login_attempt():
            user_id = id_entry.get()
            user_password = password_entry.get()

            if login(user_id, user_password, login_count):
                tk.Label(login_window, text=f'Login successful! Welcome, {user_id}.').grid(row=3, column=1)
                login_window.destroy()
            else:
                tk.Label(login_window, text='Login failed. Check your ID and password.').grid(row=3, column=1)

        tk.Button(login_window, text="Login", command=handle_login_attempt).grid(row=2, column=1)

if __name__ == '__main__':
    app = LoginGUI()
    app.mainloop()
