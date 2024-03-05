from lib.user import *
from lib.user_repo import *
import pytest

# test all user function - Do we want to see all users?
def test_all(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    result = user_repo.all()

    assert result == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136")
    ]
# test find user by username function
def test_find(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    result = user_repo.find('Venera')

    assert result == User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536")

#  test creating a new user
def test_create(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    user_repo.create(User(4, 'Dom', 'dom@gmail.com', 'osfhgoahfo!', "07463648537"))

    assert user_repo.all() == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136"),
        User(4, 'Dom', 'dom@gmail.com', 'osfhgoahfo!', "07463648537")
    ]

#  test creating a new user
def test_delete(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    user_repo.delete("Dom")

    assert user_repo.all() == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136")
    ]

def test_create_existsing_user_will_raise_error(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    with pytest.raises(Exception) as e:
        user_repo.create(User(None, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"))
    error_message = str(e.value)

    assert error_message == "User already exists. Choose a new username."
    

def test_password_is_valid_will_raise_error(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = userRepository(db_connection)

    with pytest.raises(Exception) as e:
        user_repo.create(User(None, 'Matt', 'venera@gmail.com', 'venera123', "07463648536"))
    error_message = str(e.value)

    assert error_message == "Password is not valid: password must be minimum 8 characters long and contain one of the following: '!@$%&'"