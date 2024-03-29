import os, psycopg
from flask import g
from psycopg.rows import dict_row


# This class helps us interact with the database.
# It wraps the underlying psycopg library that we are using.

# If the below seems too complex right now, that's OK.
# That's why we have provided it!
class DatabaseConnection:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode

    # This method connects to PostgreSQL using the psycopg library. We connect
    # to localhost and select the database name given in argument.
    def connect(self):
        try:
            # Retrieve database connection details from environment variables
            host = os.environ.get("DB_HOST")
            database = os.environ.get("DB_NAME")
            user = os.environ.get("DB_USER")
            password = os.environ.get("DB_PASSWORD")

            # Check if any of the required environment variables are missing
            if None in (host, database, user, password):
                raise Exception("One or more environment variables are not set.")

            # Establish the database connection
            self.connection = psycopg.connect(
                dbname=database,
                host=host,
                port="5432",
                user=user,
                password=password,
                row_factory=dict_row
            )

        except psycopg.OperationalError as e:
            raise Exception(f"Couldn't connect to the database! Error: {e}")

    # This method seeds the database with the given SQL file.
    # We use it to set up our database ready for our tests or application.
    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    # This method executes an SQL query on the database.
    # It allows you to set some parameters too. You'll learn about this later.
    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'

    # This private method checks that we're connected to the database.
    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)
        
    def initial_seed_properties(self):
        cursor = self.connection.cursor()
        # Check if the properties table is empty
        cursor.execute("SELECT COUNT(*) FROM properties")
        result = cursor.fetchone()
        num_properties = result['count']

        # If the properties table is empty, seed the properties
        if num_properties == 0:
            images_dir = os.path.join(os.getcwd(), "static/img")
            # List of property data
            property_data = [
                ("London", "Castle", 200, 2),
                ("Paris", "Chateau", 150, 2),
                ("Astana", "Yurt", 450, 1),
                ("Jupiter", "Space station", 1000, 4)
            ]
            # Iterate over property data
            for property_values in property_data:
                property_name, property_description, property_cost, user_id = property_values
                
                # Construct the full path to the image file
                filename = property_name + ".png"
                image_path = os.path.join(images_dir, filename)
                
                # Open the image file and read its content
                with open(image_path, "rb") as file:
                    image_data = file.read()
                    
                    # Execute the insertion query
                    cursor.execute("INSERT INTO properties (name, description, cost_per_night, image_data, user_id) VALUES (%s, %s, %s, %s, %s)",
                                    (property_name, property_description, property_cost, psycopg.Binary(image_data), user_id))
            # Commit the transaction
            self.connection.commit()
            print('Database seeded successfully!')


# This function integrates with Flask to create one database connection that
# Flask request can use. To see how to use it, look at example_routes.py
def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = DatabaseConnection(
            test_mode=os.getenv('APP_ENV') == 'test')
        g.flask_database_connection.connect()
    return g.flask_database_connection
