from src.utils.xml_cpf import soap_body_cpf
from requests_pkcs12 import post
from src.utils.extract_pacient import extract_patient_info
from src.model.document import Document
from src.controller.token import TokenController
from dataclasses import dataclass

@dataclass
class ConsultControllerProps:
    url_consult: str
    cert_path: str
    cert_password: str
    token_controller: TokenController

class ConsultController:

    def __init__(self, props: ConsultControllerProps):
        self._url_consult = props.url_consult
        self._cert_path = props.cert_path
        self._cert_password = props.cert_password
        self._token_controller = props.token_controller

    def _get_headers_(self, token: str):
        return {
            "Authorization": f"jwt {token}",
            "Content-Type": "application/soap+xml; charset=utf-8"
        }
    
    def handle_consult(self, document: Document):
        token = self._token_controller.get_token()
        data = None
        if document.type_consult == "cpf":
            data = soap_body_cpf.replace("{{cpf_input}}", document.value)
        elif document.type_consult == "cns":
            pass
        response = post(
            self._url_consult,
            data=data,
            headers=self._get_headers_(token.access_token),
            pkcs12_filename=self._cert_path,
            pkcs12_password=self._cert_password
        )
        if response.status_code == 401:
            return self.handle_consult(document)
        if response.status_code != 200:
            raise Exception(f"Não foi possível realizar a consulta! STAUTS CODE: {response.status_code}")
        return extract_patient_info(response.text)
