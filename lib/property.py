class Property():

    def __init__(self, id, name, description, cost_per_night, image_data, user_id, bookings = []):
        self.id = id
        self.name = name
        self.description = description
        self.cost_per_night = cost_per_night
        self.image_data = image_data
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f'Property({self.id}, {self.name}, {self.description}, {self.cost_per_night}, {self.image_data}, {self.user_id})'