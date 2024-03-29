from lib.property import Property

class PropertyRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from properties ORDER BY id') #order by helps to sort changes made by update that was changing the order of the properties once updates were made.
        properties = [Property(row['id'],row['name'], row['description'], row['cost_per_night'], row['image_data'], row['user_id']) for row in rows]
        return properties
    
    def create(self, property):
        self._connection.execute('INSERT INTO properties (name, description, cost_per_night, image_data, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING id', [property.name, property.description, property.cost_per_night, property.image_data, property.user_id])
        return None

    # Retrieve a specific property
    def find(self, id):
        rows = self._connection.execute('SELECT * FROM properties WHERE id=%s', [id])
        row = rows[0]
        return Property(row["id"], row["name"], row["description"], row["cost_per_night"], row['image_data'], row["user_id"])

    def update_property(self, property_id, name=None, description=None, cost_per_night=None):
        # Construct the SET clause based on provided values to be updated
        set_clause = []
        if name is not None:
            set_clause.append(f"name = '{name}'")
        if description is not None:
            set_clause.append(f"description = '{description}'")
        if cost_per_night is not None:
            set_clause.append(f"cost_per_night = {cost_per_night}")

        # Check if any fields were provided for update
        if not set_clause:
            raise ValueError("At least one field (name, description, or cost_per_night) must be provided for updating.")

        # Construct and execute the update query for any changes made
        query = f"""
            UPDATE properties 
            SET {', '.join(set_clause)}
            WHERE id = {property_id}
        """
        self._connection.execute(query)