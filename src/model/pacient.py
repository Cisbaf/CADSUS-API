from pydantic import BaseModel, Field
from typing import Optional, List


class Address(BaseModel):
    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    neighborhood: Optional[str]
    city_code: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]


class PatientInfo(BaseModel):
    full_name: str
    birth_date: str
    gender: str
    cpf: str
    phone: Optional[str]
    address: Address
    mother_name: Optional[str]
    father_name: Optional[str]
    marital_status: Optional[str]
    race: Optional[str]
    other_ids: List[str] = Field(default_factory=list)
