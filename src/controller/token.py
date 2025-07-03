from src.model.token import Token
from datetime import datetime
from requests_pkcs12 import get, post


class TokenController:

    def __init__(self, auth_url: str, cert_path: str, cert_password: str):
        self._auth_url = auth_url
        self._cert_path = cert_path
        self._cert_password = cert_password
        self._token: Token = None
        self._last_generation: datetime = None
    
    def _generate_token_(self) -> Token:
        response = get(
            self._auth_url,
            pkcs12_filename=self._cert_path,
            pkcs12_password=self._cert_password
        )
        token_json = response.json()
        if response.status_code == 200:
            return Token(**token_json)
        else:
            raise Exception("Não foi possivel gerar um token!")
        
    def refresh_token(self) -> Token:
        self._token = self._generate_token_()
        self._last_generation = datetime.now()
        return self._token
    
    def get_token(self) -> Token:
        now = datetime.now()
        if (
            not self._last_generation # Caso não tenha uma ultima geração de token
            or not self._token # Caso não exista um token instanciado
            or (self._last_generation 
                and (now - self._last_generation).total_seconds() > self._token.expires_in
            ) # Caso o token já tenha expirado
        ):
            self._token = self._generate_token_()
            self._last_generation = datetime.now()
        return self._token