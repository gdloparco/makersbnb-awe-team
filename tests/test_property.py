from lib.property import Property

def test_property_values():
    property = Property(1, 'London', 'Castle', 200, 2)
    assert property.id == 1
    assert property.name == 'London'
    assert property.description == 'Castle'
    assert property.cost_per_night == 200
    assert property.user_id == 2

def test_property_values_are_equal():
    property_1 = Property(1, 'London', 'Castle', 200, 2)
    property_2 = Property(1, 'London', 'Castle', 200, 2)
    print(type(property_1))
    assert property_1 == property_2

def test_property_formats_appropriately():
    property = Property(1, 'London', 'Castle', 200, 2)
    assert property.__repr__() == 'Property(1, London, Castle, 200, 2)'