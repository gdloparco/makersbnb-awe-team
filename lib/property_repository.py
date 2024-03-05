from lib.property import Property

class PropertyRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from properties')
        properties = [Property(row['id'],row['name'], row['description'], row['cost_per_night'], row['user_id']) for row in rows]
        return properties
    
    def create(self, property):
        self._connection.execute('INSERT INTO properties (name, description, cost_per_night, user_id) VALUES (%s, %s, %s, %s) RETURNING id', [property.name, property.description, property.cost_per_night, property.user_id])
        return None
    
    def update(self, property):
        # Check if the property has a valid ID
        if not property.id:
            raise ValueError("Property must have a valid name for updating.")
        
        query = """
            UPDATE properties 
            SET 
                name = %s, 
                description = %s, 
                cost_per_night = %s
            WHERE name = %s
        """
        self._connection.execute(query, [property.name, property.description, property.cost_per_night, property.user_id])

"""
python

class BookRepository: # Existing methods... # Update a book by its id 

def update(self, book): self._connection.execute( 'UPDATE books SET title = %s, author_name = %s WHERE id = %s', \
    [ book.title, book.author_name, book.id]) 
return None

"""