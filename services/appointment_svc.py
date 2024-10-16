from datetime import datetime

import json
import locale
from os import system
import time
import pytz
from classes.appointment import Appointment


from utils.json_utils import JsonUtils
from tabulate import tabulate

# Códigos de color ANSI
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def ScheduleAppointment(patient):
    from constants.constants import EMPLOYEES_DATA_FILE
    from constants.constants import APPOINTMENTS_DATA_FILE
    from constants.constants import ROLE_DOCTOR
    while True:
        employees = JsonUtils.load_file(EMPLOYEES_DATA_FILE)
        print("Lista de Doctores")
 
        doctors = list(filter(lambda doctor: doctor['role'] == ROLE_DOCTOR and len(doctor['appointments']) > 0, employees))# buscando a los empleados doctores  (que ademas tegas citas disponibles)
        
        # Aqui se le da formato lejible a la dat que hay en 'doctores'. se uso la dependencia 'tabulate'
        tabla_doctores = []
        for idx, doc in enumerate(doctors, start=1):  
            fila_coloreada = [f"{CYAN}{idx}{RESET}", doc['name'], doc['specialty'], doc['office']] 
            tabla_doctores.append(fila_coloreada)
        headers = [f"{MAGENTA}#{RESET}", f"{MAGENTA}Nombre{RESET}", f"{MAGENTA}Especialidad{RESET}", f"{MAGENTA}Oficina{RESET}"]
        print(tabulate(tabla_doctores, headers=headers, tablefmt="grid"))
        while True:
            patient_input = input("Seleccione el número del doctor (o escribe 'salir' para regresar): ")
            if patient_input.lower() == 'salir':
                print("Saliendo del registro de cita..."); time.sleep(1)
                system("cls")
                return
                        
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
                        formatted_date, formatted_time = format_datetime(appointment_time)

                        # Confirmación
                        print("\nResumen de la cita:")
                        print(f"Paciente: {patient['name']}")
                        print(f"Doctor: {selectedDoctor['name']}")
                        print(f"Fecha: {formatted_date}")       
                        print(f"Hora: {formatted_time}")
                        confirm = input("¿Desea confirmar esta cita? (s/n): ")
                        
                        
                        if confirm.lower() != 's':
                            return print("Cita no agendad.")
                            

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
     

def getAppointmentListOfPatient (patient):
    while True:
        from constants.constants import APPOINTMENTS_DATA_FILE
   
        appointmentsFile = JsonUtils.load_file(APPOINTMENTS_DATA_FILE)
 
        appointments = list(filter(lambda appoint: appoint['patient_name'] == patient['name'], appointmentsFile))# buscando las citas del paciente
        
        # Aqui se le da formato lejible a la dat que hay en 'doctores'. se uso la dependencia 'tabulate'
        appointments_table = []
        for idx, appoint in enumerate(appointments, start=1):  

            # Acceder al campo date_time
            date_time_appoint = appoint['appointment_time']['date_time']
            # Convertir la cadena a datetime
            appointment_time = datetime.fromisoformat(date_time_appoint)
            formatted_date, formatted_time = format_datetime(appointment_time)

      
            
            fila_coloreada = [f"{CYAN}{idx}{RESET}", appoint['doctor_name'], appoint['specialty'], appoint['office'], formatted_date, formatted_time] 
            appointments_table.append(fila_coloreada)
        headers = [f"{MAGENTA}#{RESET}", f"{MAGENTA}Médico{RESET}", f"{MAGENTA}Especialidad{RESET}", f"{MAGENTA}Oficina{RESET}", f"{MAGENTA}Fecha{RESET}", f"{MAGENTA}Hora{RESET}"]
        print(tabulate(appointments_table, headers=headers, tablefmt="grid"))
        
        input("OKASSSS...")
        break

def cancelAppointment(patient):
    while True:
        from constants.constants import EMPLOYEES_DATA_FILE
        from constants.constants import APPOINTMENTS_DATA_FILE
        # Cargar los datos de las citas
        appointments_file = JsonUtils.load_file(APPOINTMENTS_DATA_FILE)

        # Filtrar las citas del paciente
        patient_appointments = list(filter(lambda appoint: appoint['patient_name'] == patient['name'], appointments_file))

        if not patient_appointments:
            print("No tienes citas agendadas.")
            input("Presiona cualquier tecla para regresar al menú.")
            return
        
        # Formatear y mostrar las citas de manera legible
        appointments_table = []
        for idx, appoint in enumerate(patient_appointments, start=1):  
            # Acceder al campo date_time
            date_time_appoint = appoint['appointment_time']['date_time']
            appointment_time = datetime.fromisoformat(date_time_appoint)
            formatted_date, formatted_time = format_datetime(appointment_time)
            fila_coloreada = [f"{CYAN}{idx}{RESET}", appoint['doctor_name'], appoint['specialty'], appoint['office'], formatted_date, formatted_time] 
            appointments_table.append(fila_coloreada)
        
        headers = [f"{MAGENTA}#{RESET}", f"{MAGENTA}Médico{RESET}", f"{MAGENTA}Especialidad{RESET}", f"{MAGENTA}Oficina{RESET}", f"{MAGENTA}Fecha{RESET}", f"{MAGENTA}Hora{RESET}"]
        print(tabulate(appointments_table, headers=headers, tablefmt="grid"))

        while True:
            appointment_selected = input("Seleccione el número de cita a cancelar: ")
            try:
                selection = int(appointment_selected) - 1
                if 0 <= selection < len(patient_appointments):
                    appointment_captured = patient_appointments[selection]
                    appointment_time = datetime.fromisoformat(appointment_captured['appointment_time']['date_time'])

                    # Confirmación de cancelación
                    print("\nResumen de la cita a cancelar:")
                    print(f"Paciente: {patient['name']}")
                    print(f"Doctor: {appointment_captured['doctor_name']}")
                    formatted_date, formatted_time = format_datetime(appointment_time)
                    print(f"Fecha: {formatted_date}")
                    print(f"Hora: {formatted_time}")
                    confirm = input("¿Desea confirmar la cancelación de esta cita? (s/n): ")
                    
                    if confirm.lower() != 's':
                        return print("Cancelación de cita abortada.")

                    # Eliminar la cita del listado de citas del paciente
                    appointments_file.remove(appointment_captured)  # Eliminar de las citas del paciente

                    # Agregar la cita de nuevo a las citas del doctor
                    employees = JsonUtils.load_file(EMPLOYEES_DATA_FILE)
                    for doctor in employees:
                        if doctor['name'] == appointment_captured['doctor_name']:
                            doctor['appointments'].append({"date_time": appointment_captured['appointment_time']['date_time']})
                            break

                    # Guardar los cambios en los archivos JSON
                    JsonUtils.save_file(APPOINTMENTS_DATA_FILE, appointments_file)
                    JsonUtils.save_file(EMPLOYEES_DATA_FILE, employees)  # Guarda los cambios en los doctores
                    print("Cita cancelada y añadida de nuevo a la lista del doctor.")
                    input("Presione cualquier tecla para regresar al menú.")
                    return
                else:
                    print("Selección no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")




def format_datetime(datetime): # dejaré esta funcion aqui, estuve peleando con las importaciones fooooo
    # Establecer la zona horaria de Honduras
    honduras_tz = pytz.timezone('America/Tegucigalpa')
    appointment_time_honduras = datetime.astimezone(honduras_tz)  # Convertir a la zona horaria de Honduras

    # Formatear la fecha y la hora en un formato legible
    formatted_date = appointment_time_honduras.strftime('%A, %d de %B de %Y')  
    formatted_time = appointment_time_honduras.strftime('%I:%M %p')  

    return formatted_date, formatted_time