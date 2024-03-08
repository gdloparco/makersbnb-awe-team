import pytest
from lib.user_parameters_validator import UserParametersValidator


"""
With A valid username email password and phone
It is valid
"""
def test_is_valid():
    validator = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "074747312")
    assert validator.is_valid() == True


"""
With A blank or None username
It is not valid
"""
def test_is_not_valid_with_invalid_username():
    validator_1 = UserParametersValidator("", "andre@fmail.com", "andre123", "074747312")
    assert validator_1.is_valid() == False
    validator_2 = UserParametersValidator(None, "andre@fmail.com", "andre123", "074747312")
    assert validator_2.is_valid() == False

"""
With A blank or None email
It is not valid
"""
def test_is_not_valid_with_invalid_email():
    validator_1 = UserParametersValidator("Andregois", "", "andre123", "074747312")
    assert validator_1.is_valid() == False
    validator_2 = UserParametersValidator("Andregois", None, "andre123", "074747312")
    assert validator_2.is_valid() == False

"""
With A blank or None password
It is not valid
"""
def test_is_not_valid_with_invalid_password():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "", "074747312")
    assert validator_1.is_password_valid() == False
    validator_2 = UserParametersValidator("Andregois", "andre@fmail.com", None, "074747312")
    assert validator_2.is_password_valid() == False

"""
With A blank or None phone
It is not valid
"""
def test_is_not_valid_with_invalid_phone():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "")
    assert validator_1.is_valid() == False
    validator_2 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", None)
    assert validator_2.is_valid() == False


"""
With invalid parameters
Produces errors
"""
def test_generate_errors():
    validator_1 = UserParametersValidator("", "", "andre123", "074747312")
    assert validator_1.generate_errors() == "username must not be blank, email must not be blank"
    assert validator_1.generate_password_errors() == "Password must be minimum 8 characters long and contain one of the following: '!@$%&'"

    validator_2 = UserParametersValidator("", "", "", "")
    assert validator_2.generate_errors() == "username must not be blank, email must not be blank, password must not be blank, phone must not be blank"
    assert validator_2.generate_password_errors() == "Password must be minimum 8 characters long and contain one of the following: '!@$%&'"
    
    validator_3 = UserParametersValidator("Andregois", "andre@fmail.com", "", "")
    assert validator_3.generate_errors() == "phone must not be blank"


def test_get_valid_username_if_username_valid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "0357297592")
    assert validator_1.get_valid_username() == "Andregois"

def test_get_valid_username_refuses_if_invalid():
    validator_1 = UserParametersValidator("", "andre@fmail.com", "andre123", "0357297592")
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_username()
    assert str(err.value) == "Cannot get valid username"


def test_get_valid_email_if_email_valid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "0357297592")
    assert validator_1.get_valid_email() == "andre@fmail.com"

def test_get_valid_email_refuses_if_invalid():
    validator_1 = UserParametersValidator("Andregois", "", "andre123", "0357297592")
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_email()
    assert str(err.value) == "Cannot get valid email"


def test_get_valid_password_if_password_valid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "0357297592")
    assert validator_1.get_valid_password() == "andre123"

def test_get_valid_password_refuses_if_invalid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "", "0357297592")
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_password()
    assert str(err.value) == "Cannot get valid password"


def test_get_valid_phone_if_phone_valid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "0357297592")
    assert validator_1.get_valid_phone() == "0357297592"

def test_get_valid_phone_refuses_if_invalid():
    validator_1 = UserParametersValidator("Andregois", "andre@fmail.com", "andre123", "")
    with pytest.raises(ValueError) as err:
        validator_1.get_valid_phone()
    assert str(err.value) == "Cannot get valid phone"
