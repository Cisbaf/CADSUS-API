from src.model.token import Token
from src.utils.logger import logger
from datetime import datetime
from threading import Lock
from requests import RequestException
from requests_pkcs12 import get
from pydantic import ValidationError


class TokenController:

    def __init__(self, auth_url: str, cert_path: str, cert_password: str):
        self._auth_url = auth_url
        self._cert_path = cert_path
        self._cert_password = cert_password
        self._token: Token = None
        self._last_generation: datetime = None
        # A rota é síncrona, então o FastAPI a executa no threadpool: sem lock,
        # requisições concorrentes disparam renovações simultâneas e uma
        # sobrescreve o token/timestamp da outra.
        self._lock = Lock()

    def _generate_token(self) -> Token:
        try:
            response = get(
                self._auth_url,
                pkcs12_filename=self._cert_path,
                pkcs12_password=self._cert_password
            )
        except ValueError as e:
            # requests_pkcs12 valida o .pfx antes de qualquer chamada de rede:
            # certificado expirado, senha incorreta ou arquivo corrompido caem aqui.
            logger.error(f"TOKEN | Falha no certificado cliente '{self._cert_path}': {e}")
            raise Exception(f"Falha no certificado cliente: {e}")
        except RequestException as e:
            logger.error(
                f"TOKEN | Falha de comunicação com {self._auth_url}: {type(e).__name__}: {e}"
            )
            raise Exception(f"Falha de comunicação com o servidor de autenticação: {e}")

        if response.status_code != 200:
            body = response.text[:500]
            logger.error(
                f"TOKEN | {self._auth_url} respondeu {response.status_code} "
                f"| content-type: {response.headers.get('content-type')} | body: {body}"
            )
            raise Exception(f"Erro ao gerar token: {response.status_code} - {body}")

        try:
            token_json = response.json()
        except ValueError as e:
            logger.error(
                f"TOKEN | Resposta 200 não é um JSON válido "
                f"| content-type: {response.headers.get('content-type')} | body: {response.text[:500]}"
            )
            raise Exception(f"Resposta do servidor de autenticação não é um JSON válido: {e}")

        if not isinstance(token_json, dict):
            logger.error(f"TOKEN | JSON de sucesso não é um objeto: {type(token_json).__name__}")
            raise Exception("Resposta do servidor de autenticação não tem o formato esperado de token.")

        try:
            return Token(**token_json)
        except ValidationError as e:
            # Só os nomes dos campos e os erros: o corpo de sucesso contém o access_token.
            logger.error(
                f"TOKEN | JSON de sucesso não bate com o schema Token "
                f"| campos recebidos: {sorted(token_json)} "
                f"| erros: {e.errors(include_url=False, include_context=False, include_input=False)}"
            )
            raise Exception("Resposta do servidor de autenticação não tem o formato esperado de token.")

    def _is_expired(self) -> bool:
        if not self._last_generation or not self._token:
            return True
        return (datetime.now() - self._last_generation).total_seconds() > self._token.expires_in

    def _refresh(self) -> Token:
        """Renova o token. Só deve ser chamado com o lock já adquirido."""
        self._token = self._generate_token()
        self._last_generation = datetime.now()
        logger.info(f"TOKEN | Token renovado com sucesso (expires_in={self._token.expires_in}s)")
        return self._token

    def refresh_token(self) -> Token:
        with self._lock:
            return self._refresh()

    def get_token(self) -> Token:
        if not self._is_expired():
            return self._token

        with self._lock:
            # Outra thread pode ter renovado enquanto esperávamos pelo lock.
            if self._is_expired():
                self._refresh()
            return self._token
