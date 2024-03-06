class UserParametersValidator:

    def __init__(self, username, email, password, phone):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone

    def is_valid(self):
        return self._is_username_valid() and  self._is_email_valid() and self._is_password_valid() and self._is_phone_valid()
    
    def generate_errors(self):
        errors = []
        if not self._is_username_valid():
            errors.append("username must not be blank")
        if not self._is_email_valid():
            errors.append("email must not be blank")
        if not self._is_password_valid():
            errors.append("password must not be blank")
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
        if self.username is None:
            return False
        if self.username == "":
            return False
        return True
    
    def _is_email_valid(self):
        if self.email is None:
            return False
        if self.email == "":
            return False
        return True
    
    def _is_password_valid(self):
        if self.password is None:
            return False
        if self.password == "":
            return False
        return True
    
    def _is_phone_valid(self):
        if self.phone is None:
            return False
        if self.phone == "":
            return False
        return True