from lib.booking_repository import *
from lib.booking import *
from datetime import datetime


def test_find_bookings_by_property_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    booking_from_property = booking_repo.find_bookings_by_property_id(2)

    assert booking_from_property == Property(2, 'Paris', 'Chateau', 150, 2, [Booking(1, '2024-05-04', '2024-05-04', 3, 2)])

    # [Booking(1, '2024-05-04', '2024-05-04', 3, 2)]

def test_find_booking_by_property_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    booking_from_user = booking_repo.find_bookings_by_user(3)

    assert booking_from_user == [
        Booking(1, datetime(2024, 5, 4).date(),datetime(2024, 5, 4).date(), 3, 2),
        Booking(2, datetime(2024, 5, 4).date(), datetime(2024, 5, 9).date(), 3, 3),
        Booking(3, datetime(2024, 5, 10).date(), datetime(2024, 6, 10).date(), 3, 3)
    ]

def test_length_of_stay(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    length_of_stay = booking_repo.length_of_stay(3)

    assert length_of_stay == 31

def test_total_cost_reservation(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    total_cost_reservation = booking_repo.total_cost(3)

    assert total_cost_reservation == 13950