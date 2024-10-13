from os import system
import time
from controllers.patients_menu import patients_menu
from services.user_management_svc import UserService


def login_patient():
    while True:
        path = "data/patients.json"
        patients = UserService.read_file(path)
        print("*-*-*-*-*- Inicio de Sesión de Paciente -*-*-*-*-*-*-*")
        print("\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")  # Cyan
        email = input("\nIngrese su E-mail (o escribe 'salir' para regresar): ")

        if email.lower() == 'salir':
            print("Saliendo del inicio de sesión..."); time.sleep(1)
            system("cls")
            break  # salimos del bucle

        # verificar si el correo existe
        authenticatedPatient = None
        for patient in patients:
            if email.lower() == patient['email'].lower():
                authenticatedPatient = patient  # guardar paciente encontrado en una variable
                break

        if authenticatedPatient is None:
            input("\033[93m" + " !! Paciente no encontrado. Intente nuevamente . . ." + "\033[0m")  # Amarillo
            system("cls")
            continue  # volver al inicio del bucle 

        # password = getpass.getpass("Ingrese su contraseña: ")
        password = input("Ingrese su contraseña: ")

        # Verificar la contraseña
        if password == authenticatedPatient['password']:
            print("\033[92m" + "\nACCESO CONCEDIDO." + "\033[0m" + f" Bienvenido, {authenticatedPatient['name']}");
            time.sleep(1); system("cls")
            patients_menu(authenticatedPatient)
            system("cls")
            break  # volver a menu principal --- TODO: dirigirse a nuevo menú
        else:
            input("\033[91m" + " !! Contraseña incorrecta. Intente nuevamente . . ." + "\033[0m")  # Rojo
            system("cls")
            continue