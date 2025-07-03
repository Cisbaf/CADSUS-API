from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)

class Settings(BaseModel):
    auth_url: str
    url_consult: str
    cert_path: str
    cert_pass: str
    allowed_ips: List[str]
    deploy: bool

settings = Settings(
    auth_url=getenv("AUTH_URL"),
    url_consult=getenv("URL_CONSULT"),
    cert_path=getenv("CERT_PATH"),
    cert_pass=getenv("CERT_PASS"),
    allowed_ips=str(getenv("ALLOWED_IPS")).split(","),
    deploy=getenv("DEPLOY")
)
