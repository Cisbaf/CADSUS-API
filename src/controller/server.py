from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.settings import settings
app = FastAPI()

@app.middleware("http")
async def restrict_ip_middleware(request: Request, call_next):
    client_host = request.client.host
    if client_host not in settings.allowed_ips and settings.deploy:
        return JSONResponse(status_code=403, content={"detail": "IP não autorizado"})
    response = await call_next(request)
    return response
