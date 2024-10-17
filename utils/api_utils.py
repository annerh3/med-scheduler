import requests
API_KEY = 'gbBwB4x/TWXjxAXAwj0xfg==tmZiFlD59x10LZ0M'
LENGTH_PASSWORD = '16'
API_URL = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'
length = '16'

def getPassword():
    api_url = API_URL.format(LENGTH_PASSWORD)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})

    if response.status_code == requests.codes.ok:
        data = response.json() # pasar a diccionario
        random_password = data.get("random_password") # extrae el string de la contraseñá
        
        if random_password:
            return random_password
        else:
            return None
    else:
        return None