import os
import httpx

RISK_API_URL = os.getenv(
    "RISK_API_URL",
    "http://risk-api:8001"
)

def calcular_risco(
    temperatura: float,
    chuva: float,
    vento: float
):
    payload = {
        "temperatura": temperatura,
        "chuva": chuva,
        "vento": vento
    }

    response = httpx.post(
        f"{RISK_API_URL}/calcular-risco",
        json=payload,
        timeout=5.0
    )

    response.raise_for_status()

    return response.json()