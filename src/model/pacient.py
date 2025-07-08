from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Address(BaseModel):
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city_code: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None

class PatientInfo(BaseModel):
    full_name: str
    social_name: Optional[str] = None
    birth_date: str
    gender: str
    cpf: Optional[str] = None
    cns: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Address
    mother_name: Optional[str] = None
    father_name: Optional[str] = None
    marital_status: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    deceased: bool = False
    deceased_date: Optional[str] = None
    birth_place_city_code: Optional[str] = None
    birth_place_country_code: Optional[str] = None
    rg: Optional[str] = None
    ctps: Optional[str] = None
    cnh: Optional[str] = None
    voter_id: Optional[str] = None
    nis: Optional[str] = None
    passport: Optional[str] = None
    ric: Optional[str] = None
    dnv: Optional[str] = None
    local_id: Optional[str] = None
    vip: bool = False
    other_ids: List[str] = Field(default_factory=list)
    additional_info: Dict[str, Any] = Field(default_factory=dict)