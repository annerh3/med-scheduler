from os import system

def doctor_menu(doctor):
    while True:
        from services.appointment_svc import cancelAppointment, show_appointments
        # Azul
        print("\033[94m" + f"*-*-*-*-*- Menú de {doctor['name']} -*-*-*-*-*-*-*" + "\033[0m")
        print("\nSeleccione una opción:")
        print("1. Ver mis citas agendadas")
        print("2. Cancelar cita")
        print("3. Salir")
        opction = input("\nIngrese el número de opción: ")

        match opction:
            case "1":
                system("cls") 
                show_appointments(doctor)
                system("cls")
            case "2":
                system("cls") 
                cancelAppointment(doctor)
                system("cls")
            case "3":
                print("Saliendo del menú de doctor...")
                break
            case _:
                print(
                    "\033[91m" + "Opción no válida. Intente nuevamente." + "\033[0m")
                system("cls")
