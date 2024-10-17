import json
class JsonUtils:
    @staticmethod
    def load_file (path):
        with open(path, 'r', encoding='utf-8') as file: 
            return json.load(file) 
    
    @staticmethod
    def save_register(path, registeR):
        try:
            with open(path, 'r+', encoding='utf-8') as file:
                registers = json.load(file)
                # Usar la función register para guardar los datos del objeto como un diccionario
                registers.append(registeR.register())
                file.seek(0)  # para ubicar el cursor al inicio del archivo
                # ya que el cursor está al inicio del archivo, se podrá sobreescribir el archivo. Asi, se evita duplicar la info
                json.dump(registers, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            with open(path, 'w', encoding='utf-8') as file:  # crea json sino existe
                json.dump([registeR.register()], file,
                          indent=4, ensure_ascii=False)
                
    @staticmethod
    def save_file(path, data):
        try:
            # Abre el archivo en modo escritura ('w') para sobrescribir el archivo completo
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
