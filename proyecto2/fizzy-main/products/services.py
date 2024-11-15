import requests

class CurrencyService:
    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

    @staticmethod
    def obtener_tasa_cambio(moneda_destino):
        """Obtiene la tasa de cambio para la moneda destino."""
        try:
            response = requests.get(CurrencyService.API_URL)
            if response.status_code == 200:
                tasas = response.json()['rates']
                return tasas.get(moneda_destino, None)  # Devuelve la tasa de cambio si existe
            else:
                return None
        except requests.RequestException as e:
            print(f"Error al conectar con la API de tasas: {e}")
            return None
