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
    def create(self, user):
        rows = self._connection.execute("INSERT INTO users (username, email, password, phone) VALUES (%s,%s,%s,%s) RETURNING id",[user.username, user.email, user.password, user.phone])
        row = rows[0]
        user.id = row['id']
        return user
    
    # Delete an existing user
    def delete(self, username):
        rows = self._connection.execute("DELETE FROM users WHERE username=%s",[username])
        return None
    

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