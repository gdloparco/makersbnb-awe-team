class User:

    #__init__ takes properties = [] in order to be able to list out all properties from 1 specific owner
    def __init__(self, id, username, email, password, phone, properties = []):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password}, {self.phone})"