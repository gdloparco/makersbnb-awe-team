from lib.property import Property

class PropertyRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from properties')
        properties = [Property(row['name'], row['description'], row['cost_per_night'], row['user_id']) for row in rows]
        return properties
    
    def create(self, property):
        rows = self._connection.execute('INSERT INTO properties (name, description, cost_per_night, user_id) VALUES (%s, %s, %s, %s) RETURNING id', [property.name, property.description, property.cost_per_night, property.user_id])
        row = rows[0]
        property.id = row['id']
        return property