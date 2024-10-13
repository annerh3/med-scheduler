import json, time
from os import system
from classes.patient import Patient
from controllers.patients_menu import patients_menu

class UserService:

    @staticmethod
    def create_patient():
        while True:
            print("*-*-*-*-*- Registro de Paciente -*-*-*-*-*-*-*")
            print("\033[96m" + "Escribe 'salir' para regresar al Menú Principal" + "\033[0m")  # Cyan
            name = input("\nIngrese su Nombre (o escribe 'salir' para regresar):")

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

            UserService.save_patient(new_patient)

            print(f"\n\t->El paciente {name} ha sido registrado con éxito.\n")
            input("Presiona cualquier tecla para volver al Menú Principal . . .")
            system("cls")
            break

    @staticmethod
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
                break  # Salimos del bucle

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


        
    @staticmethod
    def save_patient(patient):
        try:
            with open('data/patients.json', 'r+', encoding='utf-8') as file:
                patients = json.load(file)
                # Usar la función register para guardar los datos del objeto como un diccionario
                patients.append(patient.register())
                file.seek(0)  # para ubicar el cursor al inicio del archivo
                # ya que el cursor está al inicio del archivo, se podrá sobreescribir el archivo. Asi, se evita duplicar la info
                json.dump(patients, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            with open('data/patients.json', 'w', encoding='utf-8') as file:  # crea json sino existe
                json.dump([patient.register()], file,
                          indent=4, ensure_ascii=False)

    @staticmethod
    def read_file (path):
        with open(path, 'r', encoding='utf-8') as file: 
            return json.load(file) 