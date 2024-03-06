from datetime import date
from lib.booking import *
from lib.property import *

class BookingRepository:
    # read property(property booked details) and booking(all but password)

    def __init__(self, connection):
        self._connection = connection

    # Find all properties from a single booking, it might make more sense to have as a location rather than booking?? 
    # What do you guys think?
    def find_bookings_by_property_id(self, property_id):
            rows = self._connection.execute(
        "SELECT bookings.id AS booking_id, bookings.property_id AS booking_property_id, bookings.start_date, bookings.end_date, bookings.user_id AS booking_user_id, properties.id AS property_id, properties.name, properties.description, properties.cost_per_night, properties.user_id AS property_user_id "
        "FROM properties JOIN bookings ON properties.id = bookings.property_id "
        "WHERE bookings.property_id = %s", [property_id])
            
            bookings = []
            
            for row in rows:
                booking = Booking(row["booking_id"], row["start_date"], row["end_date"], row["booking_user_id"],row["property_id"] )
                bookings.append(booking)
            print(booking)
            # Each row has the same id, property_id, and email, , and email, , so we just use the first
            return Property(rows[0]["property_id"], rows[0]["name"], rows[0]["description"], rows[0]["cost_per_night"], rows[0]["property_user_id"], bookings)
        


"""`
# show available dates
    def show_availability(self, ):
        
# make reservation, adds reservation to the booking table if criteria of avalability and fields are met
    def make_reservation(self, ):

# confirmation to guest/(ideally to owner too)
    def booking_confirmation(self, ):
        
"""