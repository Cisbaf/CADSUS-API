from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.logger import logger
from src.utils.settings import settings

app = FastAPI()

def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host  # ou request.remote_addr no Flask
    return ip

@app.middleware("http")
async def restrict_ip_middleware(request: Request, call_next):
    client_ip = get_client_ip(request)
    # lê o corpo da requisição para log
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")

    # define uma função async para reconstituir o corpo no Request
    async def receive():
        return {"type": "http.request", "body": body_bytes}

    request = Request(request.scope, receive=receive)

    if client_ip not in settings.allowed_ips and settings.deploy:
        response = JSONResponse(status_code=403, content={"detail": "IP não autorizado"})
    else:
        response = await call_next(request)

    logger.info(f"IP: {client_ip} | Body: {body_str} | Status Code: {response.status_code}")

    return response
