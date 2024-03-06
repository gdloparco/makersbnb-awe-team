class PropertyParametersValidator:

    def __init__(self, name, description, cost_per_night):
        self.name = name
        self.description = description
        self.cost_per_night = cost_per_night

    def is_valid(self):
        return self._is_name_valid() and self._is_description_valid() and self._is_cost_per_night_valid()
    
    def generate_errors(self):
        errors = []
        if not self._is_name_valid():
            errors.append("name must not be blank")
        if not self._is_description_valid():
            errors.append("description must not be blank")
        if not self._is_cost_per_night_valid():
            errors.append("cost per night must not be blank")
        errors = ", ".join(errors)
        return errors
    
    def get_valid_name(self):
        if not self._is_name_valid():
            raise ValueError("Cannot get valid name")
        return self.name

    def get_valid_description(self):
        if not self._is_description_valid():
            raise ValueError("Cannot get valid description")
        return self.description
    
    def get_valid_cost_per_night(self):
        if not self._is_cost_per_night_valid():
            raise ValueError("Cannot get valid cost per night")
        return self.cost_per_night


    def _is_name_valid(self):
        if self.name is None:
            return False
        if self.name == "":
            return False
        return True
    
    def _is_description_valid(self):
        if self.description is None:
            return False
        if self.description == "":
            return False
        return True
    
    def _is_cost_per_night_valid(self):
        if self.cost_per_night is None:
            return False
        if self.cost_per_night == "":
            return False
        return True