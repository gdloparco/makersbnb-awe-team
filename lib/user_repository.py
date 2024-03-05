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
    
    # Retrieve a specific user
    def find(self, username):
        rows = self._connection.execute('SELECT * FROM users WHERE username=%s', [username])
        row = rows[0]
        return User(row["id"], row["username"], row["email"], row["password"], row["phone"])
    
    # Create a new user
    def create(self, user):
        rows = self._connection.execute("INSERT INTO users (username, email, password, phone) VALUES (%s,%s,%s,%s)",[user.username, user.email, user.password, user.phone])
        return None
    
    # Delete an existing user
    def delete(self, username):
        rows = self._connection.execute("DELETE FROM users WHERE username=%s",[username])
        return None
    
    # Find all properties from a single user, it might make more sense to have as a location rather than user?? 
    # What do you guys think?
    def find_properties_by_username(self, username):
        rows = self._connection.execute(
    "SELECT users.id AS user_id, users.username, users.email, users.password, users.phone, properties.id AS property_id, properties.name, properties.description, properties.cost_per_night "
    "FROM users JOIN properties ON users.id = properties.user_id "
    "WHERE users.username = %s", [username])
        
        properties = []
        
        for row in rows:
            property = Property(row["property_id"], row["name"], row["description"], row["cost_per_night"],row["user_id"] )
            properties.append(property)

        # Each row has the same id, username, and email, , and email, , so we just use the first
        return User(rows[0]["user_id"], rows[0]["username"], rows[0]["email"], rows[0]["password"], rows[0]["phone"], properties)
    
