from classes.user import User

class Employee(User):
    def __init__(self, name, email, password, role):
        super().__init__(name, email, password)
        self.role = role