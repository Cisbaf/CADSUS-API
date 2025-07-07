from src.utils.xml_cpf import soap_body_cpf
from src.utils.xml_cns import soap_body_cns
from requests_pkcs12 import post
from src.utils.extract_pacient import extract_patient_info
from src.model.document import Document
from src.controller.token import TokenController
from dataclasses import dataclass
from typing import Dict, Tuple
from threading import Lock

@dataclass
class ConsultControllerProps:
    url_consult: str
    cert_path: str
    cert_password: str
    token_controller: TokenController

class ConsultController:
    _cache: Dict[Tuple[str, str], dict] = {}  # (type_consult, value) -> resultado
    _lock = Lock()

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

    def handle_consult(self, document: Document, max_retries: int = 2):
        cache_key = (document.type_consult, document.value)

        # Verifica se está em cache
        with self._lock:
            if cache_key in self._cache:
                return self._cache[cache_key]

        for attempt in range(max_retries):
            token = self._token_controller.get_token()
            if document.type_consult == "cpf":
                data = soap_body_cpf.replace("{{cpf_input}}", document.value)
            elif document.type_consult == "cns":
                data = soap_body_cns.replace("{{cns_input}}", document.value)
            else:
                raise ValueError("Tipo de documento inválido")

            response = post(
                self._url_consult,
                data=data,
                headers=self._get_headers_(token.access_token),
                pkcs12_filename=self._cert_path,
                pkcs12_password=self._cert_password
            )

            if response.status_code == 200:
                patient_info = extract_patient_info(response.text)

                # Armazena no cache
                with self._lock:
                    self._cache[cache_key] = patient_info

                return patient_info

            if response.status_code == 401 and attempt == 0:
                self._token_controller.refresh_token()
                continue

            raise Exception(f"Erro ao consultar paciente. STATUS CODE: {response.status_code}")

        raise Exception("Não foi possível realizar a consulta após várias tentativas.")
