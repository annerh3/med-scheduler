import json
import time
from os import system
from classes.patient import Patient
from constants.constants import PATIENTS_DATA_FILE, ROLE_DOCTOR, ROLE_MENU_MAPPING, ROLE_PATIENT
from controllers import doctor_menu
from controllers.patients_menu import patients_menu
from utils.json_utils import JsonUtils


class UserService:

    @staticmethod
    def create_patient():
        while True:
            print("*-*-*-*-*- Registro de Paciente -*-*-*-*-*-*-*")
            # Cyan
            print(
                "\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")
            name = input(
                "\nIngrese su Nombre (o escribe 'salir' para regresar):")

            if name.lower() == 'salir':
                print("Saliendo del registro de paciente..."); time.sleep(1)
                system("cls")
                break

            email = input("Correo: ")

            while True:
                password = input("Contraseña: ")
                password_confirmation = input(
                    "Ingrese su contraseña nuevamente: ")

                if password == password_confirmation:
                    break
                else:
                    print("\n\t->Las contraseñas no coinciden. Intente nuevamente...\n")

            medical_history = input(
                "Historial médico (separado por comas, o deja vacío para omitir): ")

            if medical_history:
                medical_history = medical_history.split(',')
            else:
                medical_history = []

            new_patient = Patient(name, email, password, medical_history)

            JsonUtils.save_register(PATIENTS_DATA_FILE, new_patient)

            print("\033[92m" + f"\n\t->El paciente {name} ha sido registrado con éxito.\n" + "\033[0m")  # Verde claro

            input("Presiona cualquier tecla para volver al Menú Principal . . .")
            system("cls")
            break

    @staticmethod
    def login_user(path):
        while True:
            users = JsonUtils.load_file(path)

            print( "\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")
            email = input("\nIngrese su E-mail (o escribe 'salir' para regresar): ")

            if email.lower() == 'salir':
                print("Saliendo del inicio de sesión..."); time.sleep(1)
                system("cls")
                break  # Salimos del bucle

            # verificar si el correo existe
            authenticatedUser = None
            for user in users:
                if email.lower() == user['email'].lower():
                    authenticatedUser = user  # el usuario existe. guardar usuario encontrado en una variable
                    break

            if authenticatedUser is None:
                input(
                    "\033[93m" + " !! Usuario no encontrado. Intente nuevamente . . ." + "\033[0m")
                system("cls")
                continue  # volver al inicio del bucle while

            password = input("Ingrese su contraseña: ")

            # Verificar la contraseña
            if password == authenticatedUser['password']:
                print("\033[92m" + "\nACCESO CONCEDIDO." + "\033[0m" +
                      f" Bienvenido, {authenticatedUser['name']}");
                time.sleep(1); system("cls");
                
                system("cls")
                
                # llamar a la funcion usando el diccionario y pasando el usuario como prametro
                if authenticatedUser['role'] in ROLE_MENU_MAPPING:
                    print("Este es un Emplead/Doctor")
                    ROLE_MENU_MAPPING[authenticatedUser['role']](authenticatedUser)  # Llama a la función pasando authenticatedUser
                    break
                else:
                     print("\033[91m" + "Rol no reconocido." + "\033[0m")
                     
                if not hasattr(authenticatedUser, 'role'): # Verificar si 'role' no está en el objeto
                    print("Este es un Paciente")
                    patients_menu(authenticatedUser) # menu de paciente
                    break
                    
                

                
                    

                break  # volver a menu principal 
            else:
                input("\033[91m" + " !! Contraseña incorrecta. Intente nuevamente . . ." + "\033[0m")  # Rojo
                system("cls")
                continue
   