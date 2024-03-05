from lib.user import User
# from lib.property import Property

class userRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all users - do we need all users?
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["id"], row["username"], row["email"], row["password"], row["phone"])
            users.append(item)
        return users
    
    # Retrieve a specific user
    def find(self, username):
        rows = self._connection.execute('SELECT * FROM users WHERE username=%s', [username])
        row = rows[0]
        return User(row["id"], row["username"], row["email"], row["password"], row["phone"])
    


    # Create a new user
    def create(self, new_user):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["id"], row["username"], row["email"], row["password"], row["phone"])
            users.append(item)
        
        for user in users:
            if new_user.username == user.username:
                raise Exception("User already exists. Choose a new username.")
        
        if not self.password_manager(new_user.password):
            raise Exception("Password is not valid: password must be minimum 8 characters long and contain one of the following: '!@$%&'")

        self._connection.execute("INSERT INTO users (username, email, password, phone) VALUES (%s,%s,%s,%s)",[new_user.username, new_user.email, new_user.password, new_user.phone])
        return None
    

    # Delete an existing user
    def delete(self, username):
        rows = self._connection.execute("DELETE FROM users WHERE username=%s",[username])
        return None
    
    def password_manager(self, password):
        return len(password) >= 8 and any(char in password for char in '!@$%&')


"""
   
    # Find a single user, along with their properties
    # Needs to be reviewed once Property Class is finished
    # Review SQL
    def find_properties_by_user_id(self, user_id):
        rows = self._connection.execute(
            "SELECT users.id AS user_id, users.username, users.starting_date, properties.id AS propertie_id, properties.username, properties.user_id " \
            "FROM users JOIN properties ON users.id = properties.user_id " \
            "WHERE users.id = %s", [user_id])
        properties = []
        for row in rows:
            property = Property(row["properties_id"], row["name"], row["description"], row["cost_per_night"])
            properties.append(property)

        # Each row has the same id, username, and email, , and email, , so we just use the first
        return User(rows[0]["user_id"], rows[0]["user_username"], rows[0]["user_email"], rows[0]["user_password"], rows[0]["user_phone"], properties)
    
    """