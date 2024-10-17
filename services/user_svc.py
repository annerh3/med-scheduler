import time
from os import system
from classes.patient import Patient
from constants.constants import PATIENTS_DATA_FILE, ROLE_MENU_MAPPING
from controllers import doctor_menu
from controllers.patients_menu import patients_menu
from utils.json_utils import JsonUtils


class UserService:

    @staticmethod
    def create_patient():
        """Método para registrar un nuevo paciente."""
        while True:
            print("*-*-*-*-*- Registro de Paciente -*-*-*-*-*-*-*")
            print("\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")
            name = input("\nIngrese su Nombre (o escribe 'salir' para regresar): ")

            # Opción de salida
            if name.lower() == 'salir':
                print("Saliendo del registro de paciente..."); time.sleep(1)
                system("cls")
                break

            email = input("Correo: ")

            # Validación de contraseña
            while True:
                password = input("Contraseña: ")
                password_confirmation = input("Ingrese su contraseña nuevamente: ")

                if password == password_confirmation:
                    break  # Las contraseñas coinciden
                else:
                    print("\n\t->Las contraseñas no coinciden. Intente nuevamente...\n")

            # Manejo del historial médico
            medical_history = input("Historial médico (separado por comas, o deja vacío para omitir): ")
            if medical_history:
                medical_history = medical_history.split(',')  # Separar en una lista
            else:
                medical_history = []

            # Crear una nueva instancia de Patient
            new_patient = Patient(name, email, password, medical_history)

            # Guardar el registro del paciente
            JsonUtils.save_register(PATIENTS_DATA_FILE, new_patient)

            print("\033[92m" + f"\n\t->El paciente {name} ha sido registrado con éxito.\n" + "\033[0m")  
            input("Presiona cualquier tecla para volver al Menú Principal . . .")
            system("cls")
            break

    @staticmethod
    def login_user(path):
        """Método para iniciar sesión de un usuario."""
        while True:
            # Cargar usuarios desde el archivo JSON
            users = JsonUtils.load_file(path)

            print("\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")
            email = input("\nIngrese su E-mail (o escribe 'salir' para regresar): ")

            # Opción de salida
            if email.lower() == 'salir':
                print("Saliendo del inicio de sesión..."); time.sleep(1)
                system("cls")
                break  # Salir del bucle

            # Verificar si el correo existe
            authenticatedUser = None
            for user in users:
                if email.lower() == user['email'].lower():
                    authenticatedUser = user  # Usuario encontrado
                    break

            # Mensaje si el usuario no existe
            if authenticatedUser is None:
                input("\033[93m" + " !! Usuario no encontrado. Intente nuevamente . . ." + "\033[0m")
                system("cls")
                continue  # Volver al inicio del bucle while

            # Verificar la contraseña
            password = input("Ingrese su contraseña: ")
            if password == authenticatedUser['password']:
                print("\033[92m" + "\nACCESO CONCEDIDO." + "\033[0m" +
                      f" Bienvenido, {authenticatedUser['name']}")
                time.sleep(1); system("cls")

                # Comprobar si el usuario tiene el campo 'role'
                if 'role' in authenticatedUser:
                    # Si el rol está mapeado a alguna función en ROLE_MENU_MAPPING
                    if authenticatedUser['role'] in ROLE_MENU_MAPPING:
                        print("Este es un Empleado/Doctor")
                        ROLE_MENU_MAPPING[authenticatedUser['role']](authenticatedUser)  # Llama a la función pasando authenticatedUser
                    else:
                        print("\033[91m" + "Rol no reconocido." + "\033[0m")
                else:
                    # Si no tiene 'role', es un paciente
                    patients_menu(authenticatedUser)  # Menú de paciente
                
                break  # Salir del bucle e ir al menú principal
            else:
                # Mensaje de contraseña incorrecta
                input("\033[91m" + " !! Contraseña incorrecta. Intente nuevamente . . ." + "\033[0m")  # Rojo
                system("cls")
                continue  # Volver al inicio del bucle