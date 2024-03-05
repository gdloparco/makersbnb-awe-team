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


def test_update_property(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = PropertyRepository(db_connection)

    # Update the name and cost_per_night of an existing property
    repository.update_property(property_id=1, name='Updated London', cost_per_night=250)

    # Check if the update is reflected in the repository
    updated_properties = repository.all()

    # Assert that the property has been updated
    assert updated_properties == [
        Property(1, 'Updated London', 'Castle', 250, 2),
        Property(2, 'Paris', 'Chateau', 150, 2),
        Property(3, 'Astana', 'Yurt', 450, 1)
    ]

