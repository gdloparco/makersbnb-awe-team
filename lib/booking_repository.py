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
        

    # Find all bookings from a specific user
    def find_bookings_by_user(self, user_id):
        rows = self._connection.execute(
        "SELECT bookings.id AS booking_id, bookings.property_id, bookings.start_date, bookings.end_date, bookings.user_id, "
        "properties.id AS property_id, properties.name, properties.description, properties.cost_per_night "
        "FROM bookings "
        "JOIN properties ON properties.id = bookings.property_id "
        "WHERE bookings.user_id = %s "
        "ORDER BY bookings.id", [user_id]
    )
        bookings = []

        for row in rows:
                booking = Booking(row["booking_id"], row["start_date"], row["end_date"], row["user_id"], row["property_id"])
                bookings.append(booking)
                print(bookings)
        return bookings
        
    # calculate length of stay based on booking_id
    def length_of_stay(self, booking_id):
        result = self._connection.execute(
            "SELECT start_date, end_date FROM bookings WHERE id = %s", [booking_id]
        )

        row = result[0]  # Assuming the result is a list with a single dictionary
        print(row)
        if row:
            start_date = row['start_date']
            end_date = row['end_date']
            length_of_stay = (end_date - start_date).days

            return length_of_stay

        return None
    
    # calculate the total cost of reservation based on booking_id and property_id (cost per night * length of stay)
    def total_cost(self, booking_id):
        length_of_stay = self.length_of_stay(booking_id)

        if length_of_stay is not None:
            property_id = self._connection.execute(
                "SELECT property_id FROM bookings WHERE id = %s", [booking_id]
            )[0].get('property_id', None)

            # Check if property_id is not None
            if property_id is not None:
                # Retrieve the cost_per_night for the associated property
                cost_per_night = self._connection.execute(
                    "SELECT cost_per_night FROM properties WHERE id = %s", [property_id]
                )[0].get('cost_per_night', None)
                # Check if cost_per_night is not None
                if cost_per_night is not None:
                    # Calculate the total cost by multiplying length_of_stay and cost_per_night
                    total_cost = length_of_stay * cost_per_night

                    return total_cost

        return None