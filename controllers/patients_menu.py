from os import system
import time

from services.appointment_svc import cancelAppointment


def patients_menu(patient):
    from services.appointment_svc import ScheduleAppointment
    from services.appointment_svc import getAppointmentListOfPatient

    while True:  # Mueve el ciclo `while` aquí para capturar la opción en cada iteración
        print("\033[94m" + f"*-*-*-*-*- Menú de {patient['name']} -*-*-*-*-*-*-*" + "\033[0m")  
        print("1. Agendar una nueva cita\n2. Ver mis citas\n3. Cancelar una cita\n4. Cerrar sesión")
        option = input("Por favor, ingrese su elección: ")

        match option:
            case '1':
                system("cls")
                print("*-*-*-*-*- Agendar Cita -*-*-*-*-*-*-*")
                ScheduleAppointment(patient)
                system("cls") 
            case '2':
                system("cls")
                print( "\033[96m" + f"*-*-*-*-*- Lista de Citas de {patient['name']} -*-*-*-*-*-*-*" + "\033[0m")
                getAppointmentListOfPatient(patient)
                system("cls") 
            case '3':
                system("cls")
                print( "\033[96m" + f"*-*-*-*-*- Lista de Citas de {patient['name']} -*-*-*-*-*-*-*" + "\033[0m")
                cancelAppointment(patient)
                system("cls") 
            case '4':
                print("\033[96m" + "Cerrando Sesión... Volviendo a Menú Principal..." + "\033[0m")
                time.sleep(2)
                system("cls")
                break  # Termina el ciclo `while` y retorna al menú principal
            case _:
                print("\033[91m" + "\n\t !! Opción inválida. Por favor, intente de nuevo." + "\033[0m")
                time.sleep(1)
                system("cls")
