import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

class OpenMeteoIndisponivel(Exception):
    pass

def consultar_clima(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:
        response = httpx.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10.0
        )

        response.raise_for_status()
    except httpx.HTTPStatusError as erro:
        raise OpenMeteoIndisponivel(
            "A Open-Meteo respondeu com erro."
        ) from erro
    except httpx.RequestError as erro:
        raise OpenMeteoIndisponivel(
            "A Open-Meteo está indisponível."
        ) from erro

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