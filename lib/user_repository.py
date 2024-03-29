from lib.user import User
from lib.property import Property

class UserRepository:

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
    
    # Retrieve a specific user by username
    def find(self, username):
        rows = self._connection.execute('SELECT * FROM users WHERE username=%s', [username])
        row = rows[0]
        return User(row["id"], row["username"], row["email"], row["password"], row["phone"])
    
        # Retrieve a specific user by their id
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * FROM users WHERE id=%s', [id])
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
        
        self._connection.execute("INSERT INTO users (username, email, password, phone) VALUES (%s,%s,%s,%s)",[new_user.username, new_user.email, new_user.password, new_user.phone])
        return new_user

    # Delete an existing user
    def delete(self, username):
        rows = self._connection.execute("DELETE FROM users WHERE username=%s",[username])
        return None

# Find all properties from a single user, it might make more sense to have as a location rather than user??
# What do you guys think?
    def find_properties_by_username(self, username):
        rows = self._connection.execute(
    "SELECT users.id AS user_id, users.username, users.email, users.password, users.phone, properties.id AS property_id, properties.name, properties.description, properties.cost_per_night, properties.image_data "
    "FROM users JOIN properties ON users.id = properties.user_id "
    "WHERE users.username = %s", [username])
        properties = []
        for row in rows:
            property = Property(row["property_id"], row["name"], row["description"], row["cost_per_night"],row ["image_data"], row["user_id"] )
            properties.append(property)
        # Each row has the same id, username, and email, , and email, , so we just use the first
        return properties

        # return User(rows[0]["user_id"], rows[0]["username"], rows[0]["email"], rows[0]["password"], rows[0]["phone"], properties)
    




        # Retrieve a specific user by username or email
    def find_by_email(self, identifier):
        # Check if the identifier is an email or username
        query = (
            "SELECT * FROM users WHERE username = %s OR email = %s"
        )
        rows = self._connection.execute(query, [identifier, identifier])
        if rows:
            row = rows[0]
            return User(row["id"], row["username"], row["email"], row["password"], row["phone"])
        return None