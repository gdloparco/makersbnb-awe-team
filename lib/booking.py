from datetime import datetime, date

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
    
    # == Methods for determining the length of stay and total cost
        # calculate length of stay
    def length_of_stay(self):
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        length_of_stay = (end_date - start_date).days
        return length_of_stay
    
    # calculate the total cost of reservation
    def total_cost(self, cost_per_night):
        length_of_stay = self.length_of_stay()
        # Calculate the total cost by multiplying length_of_stay and cost_per_night
        total_cost = length_of_stay * cost_per_night
        return total_cost