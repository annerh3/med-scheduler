from datetime import datetime
import json
import locale
from os import system
import time
import pytz
from classes.appointment import Appointment
from constants.constants import APPOINTMENTS_DATA_FILE, ROLE_DOCTOR
from utils.json_utils import JsonUtils
from tabulate import tabulate

def ScheduleAppointment(patient):
    from constants.constants import EMPLOYEES_DATA_FILE
    while True:
        employees = JsonUtils.load_file(EMPLOYEES_DATA_FILE)
        print("Lista de Doctores")
 
        doctors = list(filter(lambda doctor: doctor['role'] == ROLE_DOCTOR, employees))# buscando a los empleados doctores 
        
        # Aqui se le da formato lejible a la dat que hay en 'doctores'. se uso la dependencia 'tabulate'
        tabla_doctores = []
        for idx, doc in enumerate(doctors, start=1):  
            fila_coloreada = [f"{CYAN}{idx}{RESET}", doc['name'], doc['specialty'], doc['office']] 
            tabla_doctores.append(fila_coloreada)
        headers = [f"{MAGENTA}#{RESET}", f"{MAGENTA}Nombre{RESET}", f"{MAGENTA}Especialidad{RESET}", f"{MAGENTA}Oficina{RESET}"]
        print(tabulate(tabla_doctores, headers=headers, tablefmt="grid"))
        while True:
            patient_input = input("Seleccione el número del doctor: ")
                        
            try:
                selection = int(patient_input) - 1
                if 0 <= selection < len(doctors):  # Validar que esté en el rango
                    selectedDoctor =  doctors[selection]  # Retorna el índice original y el contacto
                    break
                else:
                    print("Selección no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")
        if not selectedDoctor:
            print(" !! Hubo un problema para seleccionar el doctor."); time.sleep(3)

        honduras_tz = pytz.timezone('America/Tegucigalpa') # establecer zona horaria
        locale.setlocale(locale.LC_TIME, 'es_HN.UTF-8')  # configurar la localización a español

        print("\nFechas disponibles para la próxima semana:")
        available_appointments = selectedDoctor['appointments']

        # Formatear y mostrar las citas de manera legible
        for appointment in available_appointments:

            # convertir date y fecha a objeto datetime
            appointment_time = datetime.fromisoformat(appointment['date_time']) 
            
            # Convertir a la zona horaria de Honduras
            appointment_time_honduras = appointment_time.astimezone(honduras_tz) 
            
            # Formatear la fecha y hora a un formato más legible en español
            formatted_time = appointment_time.strftime('%A, %d de %B de %Y, %I:%M')
            
            print(f"- {formatted_time}")
       
            while True:
                appointment_selected = input("Seleccione el número de cita a agendar: ");
                            
                try:
                    selection = int(appointment_selected) - 1
                    if 0 <= selection < len(available_appointments): 
                        appointment_captured = available_appointments[selection]

                        appointment_time = datetime.fromisoformat(appointment_captured['date_time'])  # Convertir a datetime

                        # Establecer la zona horaria de Honduras
                        honduras_tz = pytz.timezone('America/Tegucigalpa')
                        appointment_time_honduras = appointment_time.astimezone(honduras_tz)  # Convertir a la zona horaria de Honduras

                        # Formatear la fecha y la hora en un formato legible
                        formatted_date = appointment_time_honduras.strftime('%A, %d de %B de %Y')  # Ejemplo: Lunes, 05 de Junio de 2023
                        formatted_time = appointment_time_honduras.strftime('%I:%M %p')  # Ejemplo: 02:30 PM

                        # Confirmación
                        print("\nResumen de la cita:")
                        print(f"Paciente: {patient['name']}")
                        print(f"Doctor: {selectedDoctor['name']}")
                        print(f"Fecha: {formatted_date}")       
                        print(f"Hora: {formatted_time}")
                        confirm = input("¿Desea confirmar esta cita? (s/n): ")

                        if confirm.lower() != 's':
                            return print("Cita no agendada.")

                        del available_appointments[selection] # Eliminar la cita disponibles del array de citas del doctor   
                        JsonUtils.save_file(EMPLOYEES_DATA_FILE, employees)  # Actualizar el JSON de empleados
                        break
                    else:
                        print("Selección no válida. Intente de nuevo.")
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese un número.")

        # Agregar la cita a otro JSON
        new_appointment = Appointment(
                            patient['name'],
                            selectedDoctor['name'],
                            appointment_captured,
                            selectedDoctor['specialty'],
                            selectedDoctor['office']
             )
        
        try:
            appointments_data = JsonUtils.load_file(APPOINTMENTS_DATA_FILE)
        except json.decoder.JSONDecodeError:
            # Si el archivo está vacío o malformado, inicializa una lista vacía
            appointments_data = []

        # Agregar la nueva cita
        appointments_data.append(new_appointment.to_dict())

        # Guardar las citas agendadas
        JsonUtils.save_file(APPOINTMENTS_DATA_FILE, appointments_data)
        input("Cita agendada con éxito. Presione para volver al Men de Paciente . . .")
        system("cls")
        break
     


# Códigos de color ANSI
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"