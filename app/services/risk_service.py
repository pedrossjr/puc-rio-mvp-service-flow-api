import os
import httpx

RISK_API_URL = os.getenv(
    "RISK_API_URL",
    "http://serviceflow-risk-api:8001"
)

class RiskAPIIndisponivel(Exception):
    pass

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

    try:
        response = httpx.post(
            f"{RISK_API_URL}/calcular-risco",
            json=payload,
            timeout=5.0
        )

        response.raise_for_status()
    except httpx.HTTPStatusError as erro:
        raise RiskAPIIndisponivel(
            "A ServiceFlow Risk API respondeu com erro."
        ) from erro
    except httpx.RequestError as erro:
        raise RiskAPIIndisponivel(
            "A ServiceFlow Risk API está indisponível."
        ) from erro

    return response.json()