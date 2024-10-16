from os import system
import time
from constants.constants import EMPLOYEES_DATA_FILE, PATIENTS_DATA_FILE
from services.user_svc import UserService

def main_menu():
    while True:
        print("\033[95m" + "\n*-*-*-*-*- MedScheduler | Centro Médico -*-*-*-*-*-*-*\n" + "\033[0m") 
        print("1. Registrarse como Paciente")
        print("2. Iniciar sesión como Paciente")
        print("3. Iniciar sesión como Empleado")
        print("4. Salir del programa")
        option = input("Por favor, ingrese su elección: ")

        # Usar match para manejar las opciones del menú
        match option:
            case '1':
                system("cls")      
                UserService.create_patient() 
            case '2':
                system("cls")
                print("*-*-*-*-*- Inicio de Sesión de Paciente -*-*-*-*-*-*-*")
                UserService.login_user(PATIENTS_DATA_FILE)
            case '3':
                print("Iniciando Sesión como Empleado")
                system("cls")
                print("*-*-*-*-*- Inicio de Sesión de Empleado -*-*-*-*-*-*-*")
                UserService.login_user(EMPLOYEES_DATA_FILE)
            case '4':
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            case _:
                print("\033[91m" + "\n\t !! Opción inválida. Por favor, intente de nuevo." + "\033[0m"); time.sleep(1)
                system("cls")