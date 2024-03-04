from lib.property import Property
from lib.property_repository import PropertyRepository

def test_all(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
    assert repository.all() == [
        Property('London', 'Castle', 200, 2),
        Property('Paris', 'Chateau', 150, 2),
        Property('Astana', 'Yurt', 450, 1)
    ]

def test_create(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
    property = Property('New York', 'Apartment', 300, 1)
    repository.create(property)
    assert repository.all() == [
        Property('London', 'Castle', 200, 2),
        Property('Paris', 'Chateau', 150, 2),
        Property('Astana', 'Yurt', 450, 1),
        Property('New York', 'Apartment', 300, 1)
    ]