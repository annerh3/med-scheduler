


from controllers.admin_menu import admin_menu
from controllers.doctor_menu import doctor_menu
from controllers.patients_menu import patients_menu

# Mensajes
LOGIN_FAILED_MESSAGE = "Inicio de sesión fallido. Intente nuevamente."


# Archivos de datos
PATIENTS_DATA_FILE = "data/patients.json"
EMPLOYEES_DATA_FILE = "data/employees.json"
APPOINTMENTS_DATA_FILE = "data/appointments.json"


# Roles de usuarios
ROLE_ADMIN = "Administrativo"
ROLE_DOCTOR = "Doctor"
ROLE_PATIENT = "Paciente"

# Diccionario de Menús
ROLE_MENU_MAPPING = {
    ROLE_PATIENT: patients_menu,
    ROLE_DOCTOR: doctor_menu,
    ROLE_ADMIN: admin_menu
}