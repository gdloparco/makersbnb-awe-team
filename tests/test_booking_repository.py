from lib.booking_repository import *
from lib.booking import *


def test_find_bookings_by_property_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    booking_repo = BookingRepository(db_connection)

    booking_from_property = booking_repo.find_bookings_by_property_id(2)

    assert booking_from_property == Property(2, 'Paris', 'Chateau', 150, 2, [Booking(1, '2024-05-04', '2024-05-04', 3, 2)])

    # [Booking(1, '2024-05-04', '2024-05-04', 3, 2)]