from datetime import datetime
import json
import locale
from os import system
import time
import pytz
from classes.appointment import Appointment

from utils.json_utils import JsonUtils
from tabulate import tabulate

# Códigos de color ANSI para la consola
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def ScheduleAppointment(patient):
    from constants.constants import EMPLOYEES_DATA_FILE, APPOINTMENTS_DATA_FILE, ROLE_DOCTOR

    while True:
        # Cargar empleados desde el archivo JSON
        employees = JsonUtils.load_file(EMPLOYEES_DATA_FILE)
        print("\033[93m\nLista de Doctores\033[0m")

        # Filtrar los doctores que tienen citas disponibles
        doctors = list(filter(lambda doctor: doctor['role'] == ROLE_DOCTOR and len(doctor['appointments']) > 0, employees))

        # Formatear la lista de doctores para mostrar
        doctors_table = []
        for idx, doc in enumerate(doctors, start=1):
            colored_row = [f"{CYAN}{idx}{RESET}", doc['name'], doc['specialty'], doc['office']]
            doctors_table.append(colored_row)

        # Definir encabezados para la tabla
        headers = [f"{MAGENTA}#{RESET}", f"{MAGENTA}Nombre{RESET}", f"{MAGENTA}Especialidad{RESET}", f"{MAGENTA}Oficina{RESET}"]
        # Mostrar tabla
        print(tabulate(doctors_table, headers=headers, tablefmt="grid"))

        # Selección del doctor por parte del paciente
        while True:
            patient_input = input("Seleccione el número del doctor (o escribe 'salir' para regresar): ")
            if patient_input.lower() == 'salir':
                print("Saliendo del registro de cita..."); time.sleep(1)
                system("cls")
                return 
            
            try:
                selection = int(patient_input) - 1
                if 0 <= selection < len(doctors):
                    selectedDoctor = doctors[selection]
                    break
                else:
                    print("Selección no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        # Establecer zona horaria y localización
        honduras_tz = pytz.timezone('America/Tegucigalpa')
        locale.setlocale(locale.LC_TIME, 'es_HN.UTF-8')

        print("\033[95m" + "Fechas disponibles:" + "\033[0m")  # Magenta

        available_appointments = selectedDoctor['appointments']

        # Formatear y mostrar las citas disponibles
        for idx, appointment in enumerate(available_appointments):
            appointment_time = datetime.fromisoformat(appointment['date_time'])
            appointment_time_honduras = appointment_time.astimezone(honduras_tz)

            # Usar la función format_datetime para formatear la fecha y hora
            formatted_date, formatted_time = format_datetime(appointment_time_honduras)

            # Imprimir la cita formateada
            print(f"{idx+1}. {formatted_date}, {formatted_time}")

        # Selección de la cita a agendar
        while True:
            appointment_selected = input("Seleccione el número de cita a agendar: ")
            try:
                selection = int(appointment_selected) - 1
                if 0 <= selection < len(available_appointments):
                    appointment_captured = available_appointments[selection] # Cita a agendar
                    
                    appointment_time = datetime.fromisoformat(appointment_captured['date_time'])
                    formatted_date, formatted_time = format_datetime(appointment_time)

                    # Confirmación de la cita
                    print("\033[38;5;214m\nResumen de la cita:\033[0m")
                    print(f"Paciente: {patient['name']}")
                    print(f"Doctor: {selectedDoctor['name']}")
                    print(f"Fecha: {formatted_date}")
                    print(f"Hora: {formatted_time}")
                    confirm = input("\033[38;5;208m¿Desea confirmar esta cita? (s/n): \033[0m")  # Naranja claro

                    if confirm.lower() != 's':
                        return print("Cita no agendada.")

                    # Eliminar la cita seleccionada del array de citas del doctor
                    del available_appointments[selection]
                    # Actualizar el archivo JSON de empleados
                    JsonUtils.save_file(EMPLOYEES_DATA_FILE, employees)
                    input("\033[92m" + "Cita agendada correctamente. Presione para volver al Menú Anterior . . ." + "\033[0m")  # Verde

                    break
                else:
                    print("\033[31mSelección no válida. Intente de nuevo.\033[0m")
            except ValueError:
                print("\033[31mEntrada no válida. Por favor, ingrese un número.\033[0m")

        # Crear una nueva cita utilizando la clase Appointment
        new_appointment = Appointment(
            patient['name'],
            selectedDoctor['name'],
            appointment_captured,
            selectedDoctor['specialty'],
            selectedDoctor['office']
        )

        # Cargar las citas existentes y agregar la nueva cita
        try:
            appointments_data = JsonUtils.load_file(APPOINTMENTS_DATA_FILE)
        except json.decoder.JSONDecodeError:
            appointments_data = []  # Inicializar lista vacía si el archivo está vacío o malformado

        # Agregar la nueva cita a la lista de citas y guardar en el archivo
        appointments_data.append(new_appointment.to_dict()) # Convierte la instancia de Appointment a un diccionario.
        JsonUtils.save_file(APPOINTMENTS_DATA_FILE, appointments_data)
        print("\033[94m\nCita agendada con éxito. Presione para volver al Menú de Paciente . . .\033[0m")
        system("cls")
        break

def show_appointments(user):
    # Mostrar citas según si el usuario es doctor o paciente
    if 'appointments' in user:  # Si el diccionario tiene 'appointments', se asume que es un doctor
        appointments_file = JsonUtils.load_file('data/appointments.json')

        # Filtrar las citas del doctor
        doctor_appointments = list(filter(lambda appoint: appoint['doctor_name'] == user['name'], appointments_file))
        if not doctor_appointments:
            input("\033[38;5;33m !! No tienes citas agendadas. Presiona para volver al  Menú anterior . . .\033[0m")  # Azul oscuro
            return

        print(f"\033[94m*-*-*-*-*- Citas agendadas para el Dr./Dra. {user['name']} -*-*-*-*-*-*-*\033[0m")
        
        # Formatear y mostrar las citas del doctor
        appointments_table = []
        for idx, appointment in enumerate(doctor_appointments, start=1):
            appointment_time = datetime.fromisoformat(appointment['appointment_time']['date_time'])
            formatted_date, formatted_time = format_datetime(appointment_time)
            fila_coloreada = [f"{idx}", user['office'], formatted_date, formatted_time]
            appointments_table.append(fila_coloreada)

        headers = ["#", "Oficina", "Fecha", "Hora"]
        print(tabulate(appointments_table, headers=headers, tablefmt="grid"))
        input("Presione para volver al Menú anterior . . .")
    
    else:  # Si no tiene 'appointments', se asume que es un paciente
        appointments_file = JsonUtils.load_file('data/appointments.json')

        # Filtrar las citas del paciente
        doctor_appointments = list(filter(lambda appoint: appoint['patient_name'] == user['name'], appointments_file))
        
        if not doctor_appointments:
            input("\033[38;5;33m !! No tienes citas agendadas. Presiona para volver al  Menú anterior . . .\033[0m")  # Azul oscuro
            return

        # Formatear y mostrar las citas del paciente
        appointments_table = []
        for idx, appoint in enumerate(doctor_appointments, start=1):
            appointment_time = datetime.fromisoformat(appoint['appointment_time']['date_time'])
            formatted_date, formatted_time = format_datetime(appointment_time)
            fila_coloreada = [f"{idx}", appoint['doctor_name'], appoint['specialty'], appoint['office'], formatted_date, formatted_time]
            appointments_table.append(fila_coloreada)

        headers = ["#", "Médico", "Especialidad", "Oficina", "Fecha", "Hora"]
        print(tabulate(appointments_table, headers=headers, tablefmt="grid"))
        input("\nPresione para volver al Menú anterior . . .")
        return

def cancelAppointment(user):
    while True:  
            
        if 'appointments' in user:  # Si el usuario es un doctor
            appointments_file = JsonUtils.load_file('data/appointments.json')
             
            # Filtrar las citas del doctor
            doctor_appointments = list(filter(lambda employee: employee['doctor_name'] == user['name'], appointments_file))
            if not doctor_appointments:
                input("\033[38;5;33m !! No tienes citas agendadas. Presiona para volver al  Menú anterior . . .\033[0m")
                return

            # Formatear y mostrar las citas del doctor
            appointments_table = []
            for idx, appointment in enumerate(doctor_appointments, start=1):
                appointment_time = datetime.fromisoformat(appointment['appointment_time']['date_time'])
                formatted_date, formatted_time = format_datetime(appointment_time)
                colored_row = [f"{idx}", appointment['patient_name'], formatted_date, formatted_time]
                appointments_table.append(colored_row)

            headers = ["#", "Paciente", "Fecha", "Hora"]
            print(tabulate(appointments_table, headers=headers, tablefmt="grid"))

            # Selección de la cita a cancelar
            while True:
                appointment_selected = input("Seleccione el número de cita a cancelar: ")
                try:
                    selection = int(appointment_selected) - 1
                    if 0 <= selection < len(doctor_appointments):
                        appointment_captured = doctor_appointments[selection]
                        confirm = input(f"¿Está seguro de que desea cancelar la cita con {appointment_captured['patient_name']}? (s/n): ")
                        if confirm.lower() == 's':
                            # Eliminar la cita seleccionada del archivo
                            appointments_file.remove(appointment_captured)
                            JsonUtils.save_file('data/appointments.json', appointments_file)
                            print("\033[38;5;37mCita cancelada con éxito. Presione para volver al Menú anterior . . .\033[0m") # Gris
                            return
                        else:
                            print("Cancelación de cita cancelada.")
                            return
                    else:
                        print("\033[31mSelección no válida. Intente de nuevo.\033[0m")
                except ValueError:
                    print("\033[31mEntrada no válida. Por favor, ingrese un número.\033[0m")
            
        else:  # Si el usuario es un paciente
            appointments_file = JsonUtils.load_file('data/appointments.json')
            employees_file = JsonUtils.load_file('data/employees.json')

            # Filtrar las citas del paciente
            patient_appointments = list(filter(lambda employee: employee['patient_name'] == user['name'], appointments_file))
            if not patient_appointments:
                input("\033[38;5;33m !! No tienes citas agendadas. Presiona para volver al  Menú anterior . . .\033[0m")
                return
            
            # Formatear y mostrar las citas del paciente
            appointments_table = []
            for idx, appointment in enumerate(patient_appointments, start=1):
                appointment_time = datetime.fromisoformat(appointment['appointment_time']['date_time'])
                formatted_date, formatted_time = format_datetime(appointment_time)
                colored_row = [f"{idx}", appointment['doctor_name'], formatted_date, formatted_time]
                appointments_table.append(colored_row)

            headers = ["#", "Médico", "Fecha", "Hora"]
            print(tabulate(appointments_table, headers=headers, tablefmt="grid"))

            # Selección de la cita a cancelar
            while True:
                appointment_selected = input("\nSeleccione el número de cita a cancelar: ")
                try:
                    selection = int(appointment_selected) - 1
                    if 0 <= selection < len(patient_appointments):
                        appointment_to_cancel = patient_appointments[selection]
                        appointment_time = datetime.fromisoformat(appointment_to_cancel['appointment_time']['date_time'])

                        # Confirmación de cancelación
                        print("\033[38;5;214mResumen de la cita:\033[0m")
                        print(f"Paciente: {user['name']}")
                        print(f"Médico: {appointment_to_cancel['doctor_name']}")
                        formatted_date, formatted_time = format_datetime(appointment_time)
                        print(f"Fecha: {formatted_date}")
                        print(f"Hora: {formatted_time}")
                        confirm = input("\033[38;5;208m¿Desea cancelar esta cita? (s/n): \033[0m")

                        if confirm.lower() == 's':
                            # Volver a poner la cita en la lista de citas disponibles del doctor
                            doctor_name = appointment_to_cancel['doctor_name']
                            # Buscar al doctor correspondiente
                            doctor = next((emp for emp in employees_file if emp['name'] == doctor_name), None)
                            
                            if doctor:
                                # Agregar la fecha de la cita cancelada al array de "appointments" del doctor
                                doctor['appointments'].append(appointment_to_cancel['appointment_time'])
                                
                                # Eliminar el paciente de la cita, dejándola disponible
                                appointments_file.remove(appointment_to_cancel)
                                
                                # Guardar los cambios
                                JsonUtils.save_file('data/employees.json', employees_file)
                                JsonUtils.save_file('data/appointments.json', appointments_file )
                                input("\033[93mLa cita ha sido cancelada. Presione para volver al menú de Paciente . . .\033[0m")
                                return
                            else:
                                input("\033[31mError: Doctor no encontrado. Presione para volver.\033[0m")
                            break
                        else:
                            input("\n\t->Cita no cancelada. Presione para volver al menú de Paciente . . .")
                            break
                    else:
                        print("\033[31mSelección no válida. Intente de nuevo.\033[0m")
                except ValueError:
                    print("\033[31mEntrada no válida. Por favor, ingrese un número.\033[0m")
        break

def format_datetime(date):
    """Formatea la fecha y hora a un formato legible."""
    formatted_date = date.strftime("%A, %d de %B de %Y")
    formatted_time = date.strftime("%I:%M %p")  # Formato de 12 horas
    return formatted_date, formatted_time