from typing import Literal
from pydantic import BaseModel, field_validator
from src.utils.valid_cpf import is_valid_cpf, normalize_cpf_format

class Document(BaseModel):
    type_consult: Literal["cpf", "cns"]
    value: str
    
    @field_validator('value', mode='before')
    @classmethod
    def clean_and_validate_cpf(cls, v, values):
        if values.data.get('type_consult') == 'cpf':
            v = normalize_cpf_format(v)
            if not is_valid_cpf(v):
                raise ValueError('CPF inválido')
        return v