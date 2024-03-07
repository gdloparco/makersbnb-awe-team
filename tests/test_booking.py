from lib.booking import Booking

# test if booking constructs
def test_booking_constructs():
    booking = Booking(1, "2024-05-05", "2024-05-10", 2, 2)
    assert booking.id == 1
    assert booking.start_date == "2024-05-05"
    assert booking.end_date == "2024-05-10"
    assert booking.user_id == 2
    assert booking.property_id == 2

# test format
def test_bookings_format_nicely():
    booking = Booking(1, "2024-05-05", "2024-05-10", 2, 2)
    assert str(booking) == 'Booking(1, 2024-05-05, 2024-05-10, 2, 2)'

# test if bookings are equal
def test_bookings_are_equal():
    booking1 = Booking(1, "2024-05-05", "2024-05-10", 2, 2)
    booking2 = Booking(1, "2024-05-05", "2024-05-10", 2, 2)
    assert booking1 == booking2
