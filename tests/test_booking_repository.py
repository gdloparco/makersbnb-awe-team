from lib.booking_repository import *
from lib.booking import *
from datetime import datetime
import pytest

def test_find_bookings_by_property_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    booking_from_property = booking_repo.find_bookings_by_property_id(2)

    assert booking_from_property == Property(2, 'Paris', 'Chateau', 150, 2, [Booking(1, '2024-05-04', '2024-05-04', 3, 2)])

    # [Booking(1, '2024-05-04', '2024-05-04', 3, 2)]


def test_find_booking_by_user_id(db_connection):
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


def test_all_method_retrieves_all_bookings(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repository = BookingRepository(db_connection)
    assert booking_repository.all() == [
        Booking(1, datetime(2024, 5, 4).date(), datetime(2024, 5, 4).date(), 3, 2),
        Booking(2, datetime(2024, 5, 4).date(), datetime(2024, 5, 9).date(), 3, 3),
        Booking(3, datetime(2024, 5, 10).date(), datetime(2024, 6, 10).date(), 3, 3)
    ]


def test_create_booking_on_available_dates(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repository = BookingRepository(db_connection)
    booking = Booking(None,'2024-10-10', '2024-10-15', 1, 2)
    booking_repository.create(booking)
    assert booking_repository.all() == [
        Booking(1, datetime(2024, 5, 4).date(), datetime(2024, 5, 4).date(), 3, 2),
        Booking(2, datetime(2024, 5, 4).date(), datetime(2024, 5, 9).date(), 3, 3),
        Booking(3, datetime(2024, 5, 10).date(), datetime(2024, 6, 10).date(), 3, 3),
        Booking(4, datetime(2024, 10, 10).date(), datetime(2024, 10, 15).date(), 1, 2)
    ]


def test_create_booking_on_unavailable_dates(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repository = BookingRepository(db_connection)
    booking = Booking(None,'2024-05-05', '2024-05-05', 1, 3)
    with pytest.raises(Exception) as e:
        booking_repository.create(booking)
    error_message = str(e.value)
    assert error_message == "Selected period for booking unavailable, try other dates."


def test_create_booking_on_unavailable_dates_at_edge_of_existing_booking_period(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repository = BookingRepository(db_connection)
    booking_1 = Booking(None,'2024-10-10', '2024-10-15', 1, 1)
    booking_repository.create(booking_1)
    booking_2 = Booking(None,'2024-10-10', '2024-10-11', 1, 1)
    with pytest.raises(Exception) as e:
        booking_repository.create(booking_2)
    error_message = str(e.value)
    assert error_message == "Selected period for booking unavailable, try other dates."


def test_create_booking_on_available_dates_at_edge_of_existing_booking_period(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repository = BookingRepository(db_connection)
    booking = Booking(None,'2024-05-09', '2024-05-10', 3, 3)
    booking_repository.create(booking)
    assert booking_repository.all() == [
        Booking(1, datetime(2024, 5, 4).date(), datetime(2024, 5, 4).date(), 3, 2),
        Booking(2, datetime(2024, 5, 4).date(), datetime(2024, 5, 9).date(), 3, 3),
        Booking(3, datetime(2024, 5, 10).date(), datetime(2024, 6, 10).date(), 3, 3),
        Booking(4, datetime(2024, 5, 9).date(), datetime(2024, 5, 10).date(), 3, 3)
    ]

