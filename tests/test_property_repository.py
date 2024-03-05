from lib.property import Property
from lib.property_repository import PropertyRepository

def test_all(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
    assert repository.all() == [
        Property(1, 'London', 'Castle', 200, 2),
        Property(2, 'Paris', 'Chateau', 150, 2),
        Property(3, 'Astana', 'Yurt', 450, 1)
    ]

def test_create(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
    property = Property(None,'New York', 'Apartment', 300, 1)
    repository.create(property)
    assert repository.all() == [
        Property(1, 'London', 'Castle', 200, 2),
        Property(2, 'Paris', 'Chateau', 150, 2),
        Property(3, 'Astana', 'Yurt', 450, 1),
        Property(4, 'New York', 'Apartment', 300, 1)
    ]
def test_update_name(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)

    # Get an existing property from the database
    existing_property = repository.all()[0]

    # Update the property name
    existing_property.name = 'Updated London'
    repository.update(existing_property)

    # Check if the update is reflected in the repository
    updated_properties = repository.all()

    # Assert that the name has been updated
    assert updated_properties == [
        Property(1, 'Updated London', 'Castle', 200, 2),
        Property(2, 'Paris', 'Chateau', 150, 2),
        Property(3, 'Astana', 'Yurt', 450, 1)]
"""
def test_update_description(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
    
def test_update_cost_per_night(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)
"""