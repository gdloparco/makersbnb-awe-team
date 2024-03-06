import pytest
from lib.property_parameters_validator import PropertyParametersValidator


"""
With A valid name description and cost per night
It is valid
"""
def test_is_valid():
    validator = PropertyParametersValidator("London", "Ancient castle", 150)
    assert validator.is_valid() == True


"""
With A blank or None name
It is not valid
"""
def test_is_not_valid_with_invalid_name():
    validator_1 = PropertyParametersValidator("", "Ancient castle", 150)
    assert validator_1.is_valid() == False
    validator_2 = PropertyParametersValidator(None, "Ancient castle", 150)
    assert validator_2.is_valid() == False

"""
With A blank or None description
It is not valid
"""
def test_is_not_valid_with_invalid_description():
    validator_1 = PropertyParametersValidator("London", "", 150)
    assert validator_1.is_valid() == False
    validator_2 = PropertyParametersValidator("London", None, 150)
    assert validator_2.is_valid() == False

"""
With A blank or None cost_per_night
It is not valid
"""
def test_is_not_valid_with_invalid_cost_per_night():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", "")
    assert validator_1.is_valid() == False
    validator_2 = PropertyParametersValidator("London", "Ancient castle", None)
    assert validator_2.is_valid() == False


"""
With invalid parameters
Produces errors
"""
def test_generate_errors():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", "")
    assert validator_1.generate_errors() == "cost per night must not be blank"

    validator_2 = PropertyParametersValidator("", "", "")
    assert validator_2.generate_errors() == "name must not be blank, description must not be blank, cost per night must not be blank"
    
    validator_3 = PropertyParametersValidator("", "Ancient castle", 150)
    assert validator_3.generate_errors() == "name must not be blank"


def test_get_valid_name_if_name_valid():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", 150)
    assert validator_1.get_valid_name() == "London"

def test_get_valid_name_refuses_if_invalid():
    validator_1 = PropertyParametersValidator("", "Ancient castle", 150)
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_name()
    assert str(err.value) == "Cannot get valid name"


def test_get_valid_description_if_description_valid():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", 150)
    assert validator_1.get_valid_description() == "Ancient castle"

def test_get_valid_description_refuses_if_invalid():
    validator_1 = PropertyParametersValidator("London", "", 150)
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_description()
    assert str(err.value) == "Cannot get valid description"


def test_get_valid_cost_per_night_if_cost_per_night_valid():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", 150)
    assert validator_1.get_valid_cost_per_night() == 150

def test_get_valid_cost_per_night_refuses_if_invalid():
    validator_1 = PropertyParametersValidator("London", "Ancient castle", "")
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_cost_per_night()
    assert str(err.value) == "Cannot get valid cost per night"