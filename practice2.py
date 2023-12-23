import bcrypt
import hashlib

password='solji'

'''
encrpyt_pw=hashlib.sha256(password.encode()).hexdigest()

login_pw=input("Password: ")
login_encrypt=hashlib.sha256(login_pw.encode()).hexdigest()

if encrpyt_pw==login_encrypt:
  print("Stored: ",encrpyt_pw)
  print("Input: ", login_encrypt)
  print("Success")

else:
  print("Stored: ",encrpyt_pw)
  print("Input: ", login_encrypt)
  print("Fail")
'''
input_password=input("Password: ")

# 솔트 생성
new_salt=bcrypt.gensalt()
print(new_salt)
print(type(new_salt))

# 입력받은 비밀번호를 바이트형으로 변환
new_password=password.encode('utf-8')
print(new_password)

# 솔트와 함께 바이트로 변환한 새 비밀번호 해싱한 후 저장
hashed_password=bcrypt.hashpw(new_password,new_salt)
print(hashed_password)

# 저장하기 위해 바이트형을 문자열로 변환 (오직 저장 위함)
decode_hash_pw=hashed_password.decode('utf-8')
print(decode_hash_pw)
print(type(decode_hash_pw))

# 둘 다 바이트형으로 바꿔야 함. 바꾼 뒤 비교
bytes_input_pw=input_password.encode('utf-8')
print(bytes_input_pw)

decode_db_pw=decode_hash_pw.encode('utf-8')
print(decode_db_pw)

print(bcrypt.checkpw(bytes_input_pw,decode_db_pw))



'''
import bcrypt
password='soljipassword'

password=password.encode('utf-8')

hashedPassword=bcrypt.hashpw(password,bcrypt.gensalt())
print(hashedPassword)


import bcrypt

password=str(input("input password: "))
password=password.encode('utf-8')
hashed=bcrypt.hashpw(password,bcrypt.gensalt(10))

check=str(input("check password: "))

check=check.encode('utf-8')

if bcrypt.checkpw(check, hashed):
  print("Login successful")
else:
  print("Password invalid")
  '''