import hashlib

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

login_count=3

def encrypt_password():
    for id in member_text_db:
        member_encrypt_db[id]=hashlib.sha256(member_text_db[id].encode()).hexdigest()  

def login_text(id, password):
    if member_encrypt_db[id]==password:
        print("Stored   Password : ",member_encrypt_db[id])
        print("Input    Password : ",password)

        return True
    else:
        return False

def print_member(member):
    for id in member:
        print(id, member[id],sep=': ')

    print('----------------------------------')

if __name__=='__main__':
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
                    continue

            if login_count==0:
                break

            break

        else:
            print('Wrong ID. Try again.')
            id=input('ID: ')
            continue