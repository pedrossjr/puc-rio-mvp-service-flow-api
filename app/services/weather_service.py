import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def consultar_clima(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto"
    }

    response = httpx.get(
        OPEN_METEO_URL,
        params=params,
        timeout=10.0
    )

    response.raise_for_status()

    dados = response.json()

    temperatura = dados["current"]["temperature_2m"]
    vento = dados["current"]["wind_speed_10m"]

    probabilidades = dados["hourly"]["precipitation_probability"]
    chuva = probabilidades[0]

    return {
        "temperatura": temperatura,
        "chuva": chuva,
        "vento": vento
    }