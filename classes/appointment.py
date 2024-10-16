from datetime import datetime

class Appointment:
    def __init__(self, patient_name, doctor_name, appointment_time, specialty, office):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.appointment_time = appointment_time  
        self.specialty = specialty
        self.office = office

    def to_dict(self):
        return {
            'patient_name': self.patient_name,
            'doctor_name': self.doctor_name,
            'appointment_time': self.appointment_time,
            'specialty': self.specialty,
            'office': self.office
        }