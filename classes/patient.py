# Archivo: models/patient.py
from classes.user import User

class Patient(User):
    def __init__(self, name, email, password, medical_history=None):
        super().__init__(name, email, password)
        self.medical_history = medical_history if medical_history else [] # hist med es lista vacia si se omite

    def __str__(self):
        return f"{super().__str__()}, Historial médico: {', '.join(self.medical_history) if self.medical_history else 'No disponible'}"

    def register(self):
        #  guardar el paciente en un archivo JSON convirtiendo el objeto en un diccionario
        patient_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "medical_history": self.medical_history
        }
        return patient_data
