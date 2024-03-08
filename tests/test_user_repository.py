from lib.user import *
import pytest
from lib.user_repository import *

# test all user function - Do we want to see all users?
def test_all(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = UserRepository(db_connection)

    result = user_repo.all()

    assert result == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136")
    ]
# test find user by username function
def test_find(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = UserRepository(db_connection)

    result = user_repo.find('Venera')

    assert result == User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536")

#  test creating a new user
def test_create(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = UserRepository(db_connection)

    user_repo.create(User(4, 'Dom', 'dom@gmail.com', 'gaojgeoag!123', "07463648537"))

    assert user_repo.all() == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136"),
        User(4, 'Dom', 'dom@gmail.com', 'gaojgeoag!123', "07463648537")
    ]

#  test creating a new user
def test_delete(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = UserRepository(db_connection)

    user_repo.delete("Dom")

    assert user_repo.all() == [
        User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536"),
        User(2, 'Andre', 'andre@gmail.com', 'andre123', "07463228136"),
        User(3, 'Booker', 'booker@gmail.com', 'booker123', "01163228136")
    ] 

#  test find all properties from user
#  it might make more sense to have as a location rather than user?? 
    
def test_find_properties_by_username(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    user_repo = UserRepository(db_connection)

    property_from_user = user_repo.find_properties_by_username("Venera")

    assert property_from_user == User(1, 'Venera', 'venera@gmail.com', 'venera123', "07463648536",[Property(3, 'Astana', 'Yurt', 450, 1)])