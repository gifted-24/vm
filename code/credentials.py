from collections import defaultdict
import json
import bcrypt

class Credential:
    def __init__(self, credential):
        self.credential = credential
        self.__usernames = credential.keys()

    def authenticate(self, entered_username, entered_password):
        if entered_username in self.__usernames:
            credential_password = self.credential[entered_username][1]
            if decode_password(credential_password, entered_password):
                print('ACCESS GRANTED!')
            else:
                print("WRONG PASSWORD. TRY AGAIN!")
        else:
            print("USERNAME DOES NOT EXIST!")

    def passwords(self):
        _passwords = f"passwords -> {[self.credential[username][1] for username in self.__usernames]}"
        return _passwords
    
    def usernames(self):
        _usernames = f"usernames -> {list(self.__usernames)}"
        return _usernames
    
    def usernames_and_passwords(self):
        _usernames_and_passwords = f"credentials -> {[(f'username:  {username}', f'password: {self.credential[username][1]}') for username in self.__usernames]}"
        return _usernames_and_passwords

def encrypt_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def decode_password(entered_password, credential_password):
    return bcrypt.checkpw(entered_password.encode(), credential_password)

def get_credentials(credentials):
    if credentials.exists():
        with credentials.open('r', encoding='utf-8') as file:
            my_credential = json.load(file)
            return my_credential
    else:
        print(f"Credential file does not exist. check -> '{credentials.name}'")
        credentials.touch(exist_ok=True)
        create_credentials(credentials)
        get_credentials(credentials)
    
def create_credentials(credentials):
    credential = defaultdict(list)
    real_name = str(input("Enter user's fullname: ")).lower().strip()
    username = str(input('Create New username: ')).strip().lower()
    password = str(input('Create New password: ')).strip().lower()
    encrypted_password = encrypt_password(password)
    credential[username].extend([real_name, encrypted_password])
    with credentials.open('a', encoding='utf-8') as file:
        json.dump(credential, file, ensure_ascii=False, indent=4)
    
def username_entry():
    user_name = str(input("Enter username: ")).lower().strip()
    return user_name
    
def password_entry():
     pass_word = str(input("Enter password: ")).lower().strip()
     return pass_word


