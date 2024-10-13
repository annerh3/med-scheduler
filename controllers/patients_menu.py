from os import system
import time


def patients_menu(patient):
    print("\033[94m" + f"*-*-*-*-*- Menú de {patient['name']} -*-*-*-*-*-*-*" + "\033[0m")  # Azul
    print("1. Agendar una nueva cita\n2. Ver mis citas\n3. Cancelar una cita\n4. Cerrar sesión")
    option = input("Por favor, ingrese su elección: ")

    while True:
        match option:
                case '1':
                    print("TODO")
                    break
                case '2':
                    print("TODO")
                    break
                case '3':
                    print("TODO")
                    break
                case '4':
                    print("\033[96m" + "Cerrando Sesión... Volviendo a Menú Principal..." + "\033[0m"); time.sleep(2)
                    break
                case _:
                    print("\033[91m" + "\n\t !! Opción inválida. Por favor, intente de nuevo." + "\033[0m"); time.sleep(1)
                    system("cls")