import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox
import security
import time


# 기본 윈도우 생성
window = tk.Tk()
window.title("Login System")
window.geometry("500x350")

# 사이 간격
empty_label=tk.Label(window)
empty_label.pack(pady=5)

# ID 입력 레이블과 엔트리
id_label = tk.Label(window, text="ID:", font=("Arial", 20))
id_label.pack()
id_entry = tk.Entry(window, font=("Arial", 20))
id_entry.pack()

# 사이 간격
empty_label=tk.Label(window)
empty_label.pack(pady=5)

# 비밀번호 입력 레이블과 엔트리
password_label = tk.Label(window, text="Password:", font=("Arial", 20))
password_label.pack()
password_entry = tk.Entry(window, show="*", font=("Arial", 20))
password_entry.pack()

# 로그인 버튼 클릭 시 실행되는 함수
def login():
    id = id_entry.get()
    password = password_entry.get()


# 로그인 버튼 클릭 시 실행되는 함수
def login():
    id = id_entry.get()
    password = password_entry.get()
    # 여기서는 아이디와 비밀번호 확인 절차를 생략하고, 항상 로그인 성공 메시지를 표시합니다.
    msgbox.showinfo("알림", "로그인 성공")

# 로그인 버튼
login_button = tk.Button(window, text="로그인", command=login, width=13, height=2)
login_button.pack(pady=20)

# 윈도우 실행
window.mainloop()