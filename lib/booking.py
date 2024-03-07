from datetime import date

class Booking:
    def __init__(self, id, start_date, end_date, user_id, property_id, booking=[]):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.property_id = property_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'Booking({self.id}, {self.start_date}, {self.end_date}, {self.user_id}, {self.property_id})'

