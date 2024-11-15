import requests

# URL del endpoint de tu servicio web
API_URL = 'http://127.0.0.1:8000/api/productos-en-stock/'

def consumir_api_productos():
    # Realiza una solicitud GET al endpoint
    response = requests.get(API_URL)
    if response.status_code == 200:
        # Si la respuesta es exitosa, imprime los productos en JSON
        productos = response.json()
        print("Productos en stock:")
        for producto in productos:
            print(f"- {producto['name']}: ${producto['price']} (Stock: {producto['stock']})")
    else:
        print(f"Error al consumir la API: {response.status_code}")

if __name__ == '__main__':
    consumir_api_productos()
