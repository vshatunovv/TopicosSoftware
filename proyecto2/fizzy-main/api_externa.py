import requests

def obtener_tasa_cambio(base='USD', target='EUR'):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url)
    if response.status_code == 200:
        tasa = response.json()['rates'][target]
        return tasa
    return None

# Probar la función
tasa = obtener_tasa_cambio('USD', 'EUR')
if tasa:
    print(f"1 USD equivale a {tasa} EUR")
else:
    print("Error al obtener la tasa de cambio")
