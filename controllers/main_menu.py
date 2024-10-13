from os import system
import time
from services.user_management_svc import UserService

def main_menu():
    while True:
        print("\033[95m" + "\n*-*-*-*-*- MedScheduler | Centro Médico -*-*-*-*-*-*-*\n" + "\033[0m") 
        print("1. Registrarse como Paciente")
        print("2. Iniciar sesión como Paciente")
        print("3. Iniciar sesión como Administrador")
        print("4. Salir del programa")
        option = input("Por favor, ingrese su elección: ")

        # Usar match para manejar las opciones del menú
        match option:
            case '1':
                system("cls")
                
                UserService.create_patient()
              
            case '2':
                system("cls")
                UserService.login_patient()
            case '3':
                print("Iniciando Sesión como Administrador")
                # login_administrator()
                break
            case '4':
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            case _:
                print("\033[91m" + "\n\t !! Opción inválida. Por favor, intente de nuevo." + "\033[0m"); time.sleep(1)
                system("cls")