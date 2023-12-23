import time
import re
from twilio.rest import Client
import bcrypt
from datetime import date
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox

# Set environment variables for your credentials
account_sid = "AC6c645edb15a53e478aa49c8a8d13886f"
auth_token = "b49bf34d7a8007e819ef2e22bdc26026"
verify_sid = "VA4a0c085fb0b4b1b05e762e2f6d9878ae"
verified_number = "+821065868791"

member_text_db={
    'admin':'1234',
    'user1':'asdf1234',
    'user2':'qwer1234',
    'user3':'iloveyou'}

member_encrypt_db={
    'admin':'',
    'user1':'',
    'user2':'',
    'user3':''}

pw_hint={
    'admin':5,
    'user1':8,
    'user2':1,
    'user3':6
}

register_date={
    'admin':'2012-5-11',
    'user1':'2015-6-24',
    'user2':'2022-12-9',
    'user3':'2020-12-25'
}


hint_list={
    1:'좋아하는 동물',
    2:'최근에 읽은 책의 주인공',
    3:'좋아하는 음식',
    4:'자주 가는 여행지',
    5:'좋아하는 가수와 그 가수의 데뷔년도',
    6:'좋아하는 영화',
    7:'자주 사용하는 앱',
    8:'좋아하는 운동과 그 운동을 시작한 년도',
    9:'좋아하는 색깔',
    10:'좋아하는 계절',
    11:'좋아하는 과일',
    12:'좋아하는 꽃',
    13:'가장 기억에 남는 여행지',
    14:'좋아하는 향수',
    15:'가장 인상 깊었던 꿈의 장소',
    16:'가장 좋아하는 작가',
    17:'좋아하는 음악 장르',
    18:'첫 애완동물의 이름',
    19:'좋아하는 과학 분야',
    20:'좋아하는 휴일'
}


login_count=2

client = Client(account_sid, auth_token)

today = date.today()


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


def password_check(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        return True
    else:
        return False

def encrypt_password():
    for id in member_text_db:
        new_salt=bcrypt.gensalt()
        new_password=member_text_db[id].encode('utf-8')
        hashed_password=bcrypt.hashpw(new_password,new_salt)
        decode_hash_pw=hashed_password.decode('utf-8')
        member_encrypt_db[id]=decode_hash_pw



def register():
    while True:
        id = input('Please enter your ID: ')
        if id in member_text_db:
            print('ID already exists. Please try another ID.')
        else:
            print("Here's some hints for making passwords\n",print_member(hint_list))
            while True:
                hint_num=input("Choose one number or you can say 'n'\n")
                pw_hint[id]=int(hint_num)
                register_date[id]=str(today)
                print(register_date)
                password = input('Please enter your password: ')
                if password_check(password):
                    member_text_db[id] = password
                    member_encrypt_db[id] = encrypt_password()
                    print('Registration successful!')
                    return
                else:
                    print('Password must contain at least one uppercase letter, one digit, and one special character.')

def login_text(id,password):
    decode_db_pw=member_encrypt_db[id].encode('utf-8')
    result=bcrypt.checkpw(password,decode_db_pw)
    return result

def print_member(member):
    for id in member:
        print(id, member[id],sep=': ')
    print('----------------------------------')

def phone_approve(client):
    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")

    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=otp_code)
    return(verification_check.status)

def login(login_count):
    print('Welcome to the login system!')

    print_member(member_text_db)
    encrypt_password()
    id=input('ID: ')

    while True:
        if id in member_text_db:
            while login_count >=0:
                input_password=input('Password: ')
                bytes_input_pw=input_password.encode('utf-8')
                login_result=login_text(id,bytes_input_pw)

                if login_result:
                    print('Welcome!')
                    break
                else:
                    print('Wrong password. Try again.')
                    login_count-=1
                    if login_count==0:
                        print('Wait for 5 minutes. Or if you want to do a phone verification to try again quickly, you can response "y".')
                        response_y_or_n=input()
                        if response_y_or_n=='y':
                            start_time = time.time()
                            while True:
                                phone_status = phone_approve(client)
                                if phone_status == 'approved':
                                    login_count = 2
                                    print('Phone verification successful. You can try to login again.')
                                    print("Here's your hint of password you choosed : ",hint_list[pw_hint[id]])
                                    print("Here's the date you registered.",register_date[id])
                                    break
                                elif time.time() - start_time >= 300: # 5 minutes has passed
                                    print('Phone verification failed or time out. Please try again.')
                                    break
                                else:
                                    continue
                        elif response_y_or_n=='n':
                            print('Count down started')
                            start_time = time.time()
                            while time.time() - start_time < 300: # 5 minutes count down
                                time.sleep(1) # wait for 1 second
                            print('You can try to login again.')
                            login_count = 1
                    continue
            break
        else:
            print('Wrong ID. Try again.')
            id=input('ID: ')
            continue



if __name__=='__main__':
    response_signup=input('Do you want to sign up? If you want, response "y"\n')
    if response_signup =='y':
        register()
        response_login=input('Do you want to login now? If you want, reponse "y"\n')
        if response_login=='y':
            login(login_count)
        else:
            exit()

    else:
        login(login_count)