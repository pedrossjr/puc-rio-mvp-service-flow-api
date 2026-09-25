# ServiceFlow API

API REST principal do **ServiceFlow**, um sistema distribuído para gerenciamento de chamados de serviços técnicos externos e avaliação de risco climático para a realização desses atendimentos.

A aplicação permite cadastrar, consultar, atualizar e excluir chamados técnicos, além de consultar as condições meteorológicas da localização do atendimento e obter uma classificação de risco por meio de uma API secundária especializada.

---

## 🎯 Objetivo

O ServiceFlow foi desenvolvido para auxiliar empresas que realizam atendimentos técnicos externos.

Antes de enviar um técnico para determinado atendimento, o sistema pode consultar as condições meteorológicas previstas para a localização do chamado e avaliar se existem condições climáticas que possam dificultar a execução do serviço.

A solução permite:

- Cadastrar chamados técnicos;
- Consultar chamados cadastrados;
- Atualizar informações dos chamados;
- Excluir chamados;
- Consultar condições meteorológicas;
- Avaliar o risco climático de um atendimento;
- Integrar diferentes componentes por meio de HTTP/REST;
- Persistir os chamados utilizando SQLite.

---

# 🏗️ Arquitetura

O ServiceFlow é composto por três componentes:

1. **ServiceFlow API** - API principal desenvolvida em FastAPI;
2. **ServiceFlow Risk API** - API secundária responsável pela classificação do risco;
3. **Open-Meteo** - API externa utilizada para obtenção dos dados meteorológicos.

A persistência dos chamados é realizada utilizando **SQLite**.

### Fluxo principal

```text
Cliente / Swagger
       │
       │ HTTP/REST
       ▼
┌─────────────────────────┐
│    ServiceFlow API      │
│         :8000           │
│                         │
│    FastAPI + SQLite     │
└───────┬─────────┬───────┘
        │         │
        │         │ HTTPS
        │         ▼
        │   ┌───────────────┐
        │   │  Open-Meteo   │
        │   │  API externa  │
        │   └───────────────┘
        │
        │ HTTP/REST
        ▼
┌─────────────────────────┐
│  ServiceFlow Risk API   │
│         :8001           │
│                         │
│    Cálculo do risco     │
└─────────────────────────┘
```

---

# 🔄 Fluxo de consulta de risco

Quando o cliente solicita:

```text
GET /chamados/{id}/risco
```

a ServiceFlow API executa o seguinte fluxo:

```text
1. Localiza o chamado no SQLite
              ↓
2. Obtém latitude e longitude
              ↓
3. Consulta a API Open-Meteo
              ↓
4. Obtém dados meteorológicos
              ↓
5. Envia os dados para a ServiceFlow Risk API
              ↓
6. A Risk API calcula o nível de risco
              ↓
7. A ServiceFlow API combina as informações
              ↓
8. Retorna o resultado ao cliente
```

Dessa forma, o cliente não precisa acessar diretamente a API externa nem a API secundária.

---

# 🛠️ Tecnologias utilizadas

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- HTTPX
- SQLite
- Docker
- Open-Meteo API

---

# 🌦️ API externa - Open-Meteo

O ServiceFlow utiliza a **Open-Meteo** como serviço externo para obtenção de dados meteorológicos.

A Open-Meteo disponibiliza uma API de previsão meteorológica em formato JSON e permite utilização sem API Key para o uso gratuito não comercial.

## Endpoint utilizado

A aplicação utiliza o endpoint:

```text
GET https://api.open-meteo.com/v1/forecast
```

O endpoint recebe, entre outros parâmetros, latitude e longitude e permite solicitar variáveis meteorológicas específicas.

### Parâmetros utilizados pelo ServiceFlow

```text
latitude
longitude
current=temperature_2m,precipitation,wind_speed_10m
hourly=precipitation_probability
forecast_days=1
timezone=auto
```

A aplicação utiliza os seguintes dados:

| Dado                        | Utilização             |
| --------------------------- | ---------------------- |
| `temperature_2m`            | Temperatura atual      |
| `precipitation_probability` | Probabilidade de chuva |
| `wind_speed_10m`            | Velocidade do vento    |

A consulta é realizada e processados internamente pela aplicação e os dados retornados.

---

# 🐳 Execução com Docker

O projeto possui um `Dockerfile` próprio.

## Construindo a imagem

Clone o repositório

```bash
git clone https://github.com/pedrossjr/puc-rio-mvp-service-flow-api.git
```

Entre no diretório:

```bash
cd serviceflow-api
```

Na raiz do projeto:

```bash
docker build -t serviceflow-api .
```

## Criar a rede Docker

```bash
docker network create serviceflow-network
```

## Executar a ServiceFlow API

```bash
docker run -d --name serviceflow-api --network serviceflow-network -p 8000:8000 -e RISK_API_URL=http://serviceflow-risk-api:8001 serviceflow-api
```

---

## Verificar os containers

```bash
docker ps
```

O container deverá estar em execução:

```text
serviceflow-api
```

A API estará disponível em:

```text
http://localhost:8000
```

---

# 📚 Documentação da API

O FastAPI fornece documentação automática.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

O Swagger pode ser utilizado para testar todos os endpoints da aplicação.

---

# 🔌 Endpoints

A ServiceFlow API possui os seguintes endpoints:

| Método | Rota                   | Descrição                  |
| ------ | ---------------------- | -------------------------- |
| GET    | `/`                    | Verifica o status da API   |
| GET    | `/chamados`            | Lista os chamados          |
| GET    | `/chamados/{id}`       | Consulta um chamado        |
| POST   | `/chamados`            | Cria um chamado            |
| PUT    | `/chamados/{id}`       | Atualiza um chamado        |
| DELETE | `/chamados/{id}`       | Remove um chamado          |
| GET    | `/chamados/{id}/risco` | Consulta o risco climático |

A aplicação possui operações utilizando os métodos **GET, POST, PUT e DELETE**, atendendo ao requisito de implementação de uma API REST com os diferentes métodos HTTP.

---

### GET `/`

Verifica o status da aplicação.

### Resposta

```json
{
  "aplicacao": "ServiceFlow API",
  "status": "online"
}
```

---

### GET `/chamados`

Retorna todos os chamados cadastrados.

### Exemplo de resposta

```json
[
  {
    "id": 1,
    "cliente": "Empresa Alfa",
    "servico": "Manutenção de equipamento",
    "cidade": "Rio de Janeiro",
    "latitude": -22.9068,
    "longitude": -43.1729,
    "data_agendada": "2026-09-06",
    "status": "ABERTO",
    "created_at": "2026-09-06T12:00:00"
  }
]
```

---

### GET `/chamados/{id}`

Consulta um chamado específico.

Exemplo:

```text
GET /chamados/1
```

Caso o chamado não exista, a API retorna HTTP `404`.

---

### POST `/chamados`

Cria um novo chamado técnico.

### Requisição

```json
{
  "cliente": "Empresa Alfa",
  "servico": "Manutenção de equipamento",
  "cidade": "Rio de Janeiro",
  "latitude": -22.9068,
  "longitude": -43.1729,
  "data_agendada": "2026-09-06"
}
```

### Resposta

A API retorna o chamado criado, incluindo seu identificador, status e data de criação.

O status inicial é:

```text
ABERTO
```

---

### PUT `/chamados/{id}`

Atualiza as informações de um chamado.

Exemplo:

```text
PUT /chamados/1
```

### Requisição 1

```json
{
  "status": "EM_ATENDIMENTO"
}
```

### Requisição 2

```json
{
  "status": "CONCLUIDO"
}
```

Os campos enviados são atualizados no registro existente.

---

### DELETE `/chamados/{id}`

Remove um chamado.

Exemplo:

```text
DELETE /chamados/1
```

Quando o chamado existe, a operação retorna HTTP `204`.

Caso contrário, retorna HTTP `404`.

---

### GET `/chamados/{id}/risco`

Consulta o risco climático associado ao chamado.

Esse é o principal recurso adicional da aplicação além do CRUD.

Exemplo:

```text
GET /chamados/1/risco
```

A API consulta as coordenadas cadastradas no chamado e obtém os dados meteorológicos através da Open-Meteo.

Depois, os dados são enviados para a ServiceFlow Risk API para classificação.

### Exemplo de resposta

```json
{
  "chamado": 1,
  "cliente": "Empresa Alfa",
  "servico": "Manutenção de equipamento",
  "cidade": "Rio de Janeiro",
  "clima": {
    "temperatura": 25.4,
    "chuva": 40,
    "vento": 32.1
  },
  "risco": {
    "nivel_risco": "MEDIO",
    "motivo": "Condições climáticas que exigem atenção.",
    "recomendacao": "Manter o atendimento com atenção às condições locais."
  }
}
```

> **Observação:** A API principal depende da ServiceFlow Risk API para realizar o cálculo de risco.

---

# 🗄️ Persistência

A aplicação utiliza **SQLite** através do SQLAlchemy.

O banco é criado automaticamente pela aplicação utilizando:

```text
serviceflow.db
```

A estrutura da tabela principal é baseada no modelo `Chamado`.

Os dados persistidos incluem:

- Identificador;
- Cliente;
- Serviço;
- Cidade;
- Latitude;
- Longitude;
- Data agendada;
- Status;
- Data de criação.

# 👨‍💻 Autor

**Pedro Silva**

**PUC-Rio**  
**Pós-graduação:** Engenharia de Software  
**Disicplina:** Arquitetura de Software  
**MVP:** ServiceFlow API
