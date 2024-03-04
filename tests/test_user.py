from lib.user import User

# test if user constructs
def test_user_constructs():
    user = User(1, "Andregois", "andre@fmail.com", "andre123", "074747312")
    assert user.id == 1
    assert user.username == "Andregois"
    assert user.email == "andre@fmail.com"
    assert user.password == "andre123"
    assert user.phone == "074747312"

# test format
def test_users_format_nicely():
    user = User(1, "Andregois", "andre@fmail.com", "andre123", "074747312")
    assert str(user) == 'User(1, Andregois, andre@fmail.com, andre123, 074747312)'

# test if users are equal
def test_users_are_equal():
    user1 = User(1, "Andregois", "andre@fmail.com", "andre123", "074747312")
    user2 = User(1, "Andregois", "andre@fmail.com", "andre123", "074747312")
    assert user1 == user2


