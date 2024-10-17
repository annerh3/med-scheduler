# Archivo: models/patient.py
from classes.user import User

class Patient(User):
    def __init__(self, name, email, password, medical_history=None):
        super().__init__(name, email, password) # la funcion 'super()' llama al constructor de la clase base 'User', pasandole los argumento
        self.medical_history = medical_history if medical_history else [] # hist med es lista vacia si se omite (atributo adicional de la clase 'patient')

    # def __str__(self):
    #     return f"{super().__str__()}, Historial médico: {', '.join(self.medical_history) if self.medical_history else 'No disponible'}"  # formatea el objeto en un formato mas lejible cuando se quiera imprimir

    def register(self):
        #  convirtierte el objeto recibido en un diccionario (esto sirve para luego guardarlo en el JSON)
        patient_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "medical_history": self.medical_history
        }
        return patient_data
