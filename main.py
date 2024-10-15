# Archivo principal que ejecuta el programa

from utilities.consoleUtilities import sClear, sExit, sPause


def exportar_base_datos():
   while True:
        # Mostrar el menu
        print("Menu :")
        print("1. Exportar en Excel")
        print("2. Exportar en JSON")
        print("3. Exportar en CVC")
        print("4. Salir")
        
        # Respuesta
        option = input("Selecciona una opcion (1-4): ")
        
        # Menu Principal
        match option:
            case '1':
                #Exportar en excel
                ''
            case '2':
                #Exportar en JSON
                ''
            case '3':
                #Exportar en CVC
                ''
            case '4':
                print("Saliendo del programa.")
                break  
            case other:
                print("Opcion invalida, Selecione una Opcion Verdadera")
        sClear()

def bases_de_datos():
    while True:
        # Mostrar el menu
        print("Menu :")
        print("1. Cargar Una Base de Datos")
        print("2. Eliminar Base de Datos")
        print("3. Crear Nueva Base de Datos")
        print("4. Cargar un seed de Datos")
        print("5. Salir")
        
        # Respuesta
        option = input("Selecciona una opcion (1-5): ")
        
        # Menu Principal
        match option:
            case '1':
                #Cargar una base de Datos
                ''
            case '2':
                #Eliminar Base de Datos
                ''
            case '3':
                #Crear base de Datos
                ''
            case '4':
                #cargar seed de Datos
                ''
            case '5':
                print("Saliendo del programa.")
                break  
            case other:
                print("Opcion invalida, Selecione una Opcion Verdadera")
        sClear()

def aplicativo():
    print("Iniciando el Aplicativo...")

def main():

    #Cargar el archivo de configuracion 
        #Contine la Ruta de la base de datos en este lugar
        #los Usuarios y contraseñas de administracion Encriptada
        # La paginacion en Usuarios y Paginacion en Registros 
        # Configuracion del inicio en el sedd de datos carga del seed
    # Carga de el seedeer de Datos si hay 

    #Vista de un administrador Todo, eliminar , crear , exportar y editar
    #Vista de un empleado solo podria ingresar a la de crear un registro y ver o listar registros
    #Vista de Supervisor , puede ver los usuarios y todo el contenido pero no puede eliminar ni crear pero puede exportar datos
    
    while True:
        # Mostrar el menu
        print("Menú:")
        print("1. Exportar base de datos")
        print("2. Bases de Datos")
        print("3. Aplicativo")
        print("4. Exit")
        
        # Respuesta
        option = input("Selecciona una opcion (1-4): ")
        
        # Menu Principal
        match option:
            case '1':
                sClear()
                exportar_base_datos()
            case '2':
                sClear()
                bases_de_datos()
            case '3':
                sClear()
                aplicativo()
            case '4':
                sClear()
                print("Saliendo del programa.")
                sPause()
                sExit()  
            case other:
                print("Opcion invalida, Selecione una Opcion Verdadera")
        sClear()


main()
