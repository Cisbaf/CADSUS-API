from typing import Literal
from pydantic import BaseModel, field_validator
from src.utils.valid_cpf import is_valid_cpf, normalize_cpf_format
from src.utils.valid_cns import is_valid_cns

class Document(BaseModel):
    type_consult: Literal["cpf", "cns"]
    value: str

    @field_validator('value', mode='before')
    @classmethod
    def clean_and_validate_document(cls, v, values):
        type_consult = values.data.get('type_consult')

        if type_consult == 'cpf':
            v = normalize_cpf_format(v)
            if not is_valid_cpf(v):
                raise ValueError('CPF inválido')

        elif type_consult == 'cns':
            v = ''.join(filter(str.isdigit, v))  # Remove tudo que não for número
            if not is_valid_cns(v):
                raise ValueError('CNS inválido')

        return v