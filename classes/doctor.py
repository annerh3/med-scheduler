
from classes.employee import Employee
from constants.constants import ROLE_DOCTOR


class Doctor(Employee):
    def __init__(self, name, email, password, specialty, work_schedule, office, role=f"{ROLE_DOCTOR}"):
        super().__init__(name, email, password, role)  
        self.specialty = specialty
        self.work_schedule = work_schedule
        self.office = office

    def __str__(self):
        base_info = super().__str__() 
        return (f"{base_info}, Especialidad: {self.specialty}, "
                f"Horario: {self.work_schedule}, Consultorio: {self.office}, Rol: {self.role}")
