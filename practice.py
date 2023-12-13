import hashlib
import re
import tkinter as tk
from twilio.rest import Client

# Set environment variables for your credentials
account_sid = "AC6c645edb15a53e478aa49c8a8d13886f"
auth_token = "7a77fed8a05a7ae73aeebe309b64c591"
verify_sid = "VA4a0c085fb0b4b1b05e762e2f6d9878ae"
verified_number = "+821065868791"

member_text_db = {
    'admin': '1234',
    'user1': 'asdf1234',
    'user2': 'qwer1234',
    'user3': 'iloveyou'
}

member_encrypt_db = {
    'admin': '',
    'user1': '',
    'user2': '',
    'user3': ''
}

login_count = 2

client = Client(account_sid, auth_token)

def password_check(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        return True
    else:
        return False

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="ID:").grid(row=0, column=0)
    tk.Label(register_window, text="Password:").grid(row=1, column=0)

    id_entry = tk.Entry(register_window)
    password_entry = tk.Entry(register_window, show="*")

    id_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def register_user():
        new_id = id_entry.get()
        new_password = password_entry.get()

        if new_id in member_text_db:
            tk.Label(register_window, text='ID already exists. Try another ID.').grid(row=3, column=1)
        else:
            if password_check(new_password):
                member_text_db[new_id] = new_password
                member_encrypt_db[new_id] = encrypt_password(new_password)
                tk.Label(register_window, text='Registration successful!').grid(row=3, column=1)
                register_window.destroy()
            else:
                tk.Label(register_window, text='Invalid password format.').grid(row=3, column=1)

    tk.Button(register_window, text="Register", command=register_user).grid(row=2, column=1)

def login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="ID:").grid(row=0, column=0)
    tk.Label(login_window, text="Password:").grid(row=1, column=0)

    id_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")

    id_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def login_user():
        user_id = id_entry.get()
        user_password = password_entry.get()

        if user_id in member_text_db:
            if member_encrypt_db[user_id] == encrypt_password(user_password):
                tk.Label(login_window, text='Welcome!').grid(row=3, column=1)
                login_window.destroy()
            else:
                tk.Label(login_window, text='Wrong password. Try again.').grid(row=3, column=1)
        else:
            tk.Label(login_window, text='Wrong ID. Try again.').grid(row=3, column=1)

    tk.Button(login_window, text="Login", command=login_user).grid(row=2, column=1)

root = tk.Tk()
root.title("Login System")

tk.Button(root, text="Sign Up", command=register_window).pack(pady=20)
tk.Button(root, text="Login", command=login_window).pack(pady=20)

root.mainloop()
