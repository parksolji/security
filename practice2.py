import hashlib
import os
import time
import re
from twilio.rest import Client

# Set environment variables for your credentials
account_sid = "AC6c645edb15a53e478aa49c8a8d13886f"
auth_token = "7a77fed8a05a7ae73aeebe309b64c591"
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

login_count=2

client = Client(account_sid, auth_token)

def password_check(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        return True
    else:
        return False

def encrypt_password():
    for id in member_text_db:
        member_encrypt_db[id]=hashlib.sha256(member_text_db[id].encode()).hexdigest()  


def register():
    while True:
        id = input('Please enter your ID: ')
        if id in member_text_db:
            print('ID already exists. Please try another ID.')
        else:
            while True:
                password = input('Please enter your password: ')
                if password_check(password):
                    member_text_db[id] = password
                    member_encrypt_db[id] = encrypt_password()
                    print('Registration successful!')
                    return
                else:
                    print('Password must contain at least one uppercase letter, one digit, and one special character.')

def login_text(id, password):
    if member_encrypt_db[id]==password:
        print("Stored Password : ",member_encrypt_db[id])
        print("Input Password : ",password)
        return True
    else:
        return False

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
                password=input('Password: ')
                password_encrypt=hashlib.sha256(password.encode()).hexdigest() 
                login_result=login_text(id,password_encrypt)

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
    response_signup=input('Would you want to sign up? If you want, response "y"\n')
    if response_signup =='y':
        register()
        response_login=input('Would you want to login now? If you want, reponse "y"')
        if response_login=='y':
            login(login_count)
        else:
            exit()

    else:
        login(login_count)