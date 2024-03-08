from lib.user_repository import UserRepository
from lib.database_connection import *
from flask import Flask

app = Flask(__name__)

class UserParametersValidator:

    def __init__(self, username, email, password, phone):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone

    def is_valid(self):
        return self._is_username_valid() and  self._is_email_valid() and self._is_phone_valid()
    

    def login_is_valid(self):
        return self._is_email_valid() and self._is_password_valid()
    

    def is_password_valid(self):
        return self._is_password_valid()
    
    def generate_password_errors(self):
        password_errors = []
        if not self._is_password_valid():
            password_errors.append("Password must be minimum 8 characters long and contain one of the following: '!@$%&'")
        password_errors = ", ".join(password_errors)
        return password_errors


    def generate_errors(self):
        errors = []
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)
        users = repository.all()
        if self.username in [user.username for user in users]:
            errors.append("username already exists")
        if not self._is_username_valid():
            errors.append("username must not be blank")
        if not self._is_email_valid():
            errors.append("email must not be blank")
        if not self._is_phone_valid():
            errors.append("phone must not be blank")
        errors = ", ".join(errors)
        return errors
    
    def get_valid_username(self):
        if not self._is_username_valid():
            raise ValueError("Cannot get valid username")
        return self.username

    def get_valid_email(self):
        if not self._is_email_valid():
            raise ValueError("Cannot get valid email")
        return self.email
    
    def get_valid_password(self):
        if not self._is_password_valid():
            raise ValueError("Cannot get valid password")
        return self.password
    

    def get_valid_phone(self):
        if not self._is_phone_valid():
            raise ValueError("Cannot get valid phone")
        return self.phone


    def _is_username_valid(self):
        if self.username is None or self.username == "":
            return False
        return True
    
    def _is_email_valid(self):
        if self.email is None:
            return False
        if self.email == "":
            return False
        return True
    
    def _is_password_valid(self):
        if self.password is None or self.password == "":
            return False
        if len(self.password) >= 8 and any(char in self.password for char in '!@$%&'):
            return False
        return True
    
    def _is_phone_valid(self):
        if self.phone is None:
            return False
        if self.phone == "":
            return False
        return True