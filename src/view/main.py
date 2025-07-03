from src.controller.server import app
from src.controller.token import TokenController
from src.controller.consult import ConsultController, ConsultControllerProps
from src.model.document import Document
from src.utils.settings import settings

# Responsável por gerar e manter o cache de um token
token_controller = TokenController(
    auth_url=settings.auth_url,
    cert_path=settings.cert_path,
    cert_password=settings.cert_pass,
)

# Responsável por fazer consultas ao CPF ou CNS
consult_controller = ConsultController(ConsultControllerProps(
    url_consult=settings.url_consult,
    cert_path=settings.cert_path,
    cert_password=settings.cert_pass,
    token_controller=token_controller
))

@app.post('/consult')
def consult(document: Document):
    return consult_controller.handle_consult(document)
