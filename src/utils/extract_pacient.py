import xml.etree.ElementTree as ET
from src.model.pacient import PatientInfo, Address


def extract_patient_info(xml_string: str) -> PatientInfo:
    ns = {
        'soap': 'http://www.w3.org/2003/05/soap-envelope',
        'hl7': 'urn:hl7-org:v3'
    }

    root = ET.fromstring(xml_string)

    patient = root.find('.//hl7:patient', ns)
    person = patient.find('hl7:patientPerson', ns)

    # Nome
    name_elem = person.find('hl7:name/hl7:given', ns)
    name = name_elem.text if name_elem is not None else ''

    # Sexo
    gender = person.find('hl7:administrativeGenderCode', ns).attrib.get('code', '')

    # Data de nascimento
    birth = person.find('hl7:birthTime', ns).attrib.get('value', '')

    # Telefone
    phone_elem = person.find('hl7:telecom', ns)
    phone = phone_elem.attrib.get('value') if phone_elem is not None else None

    # Endereço
    addr_elem = person.find('hl7:addr', ns)
    address = Address(
        street=addr_elem.findtext('hl7:streetName', default='', namespaces=ns),
        number=addr_elem.findtext('hl7:houseNumber', default='', namespaces=ns),
        complement=addr_elem.findtext('hl7:unitID', default='', namespaces=ns),
        neighborhood=addr_elem.findtext('hl7:additionalLocator', default='', namespaces=ns),
        city_code=addr_elem.findtext('hl7:city', default='', namespaces=ns),
        state=addr_elem.findtext('hl7:state', default='', namespaces=ns),
        postal_code=addr_elem.findtext('hl7:postalCode', default='', namespaces=ns),
        country_code=addr_elem.findtext('hl7:country', default='', namespaces=ns),
    )

    # CPF
    cpf = ''
    for id_elem in patient.findall('hl7:id', ns):
        if id_elem.attrib.get('assigningAuthorityName') == 'CARGA-RFB':
            cpf = id_elem.attrib.get('extension')
            break

    # Estado civil
    marital = person.find('hl7:maritalStatusCode', ns)
    marital_status = marital.attrib.get('code') if marital is not None else None

    # Raça
    race_elem = person.find('hl7:raceCode', ns)
    race = race_elem.attrib.get('code') if race_elem is not None else None

    # Relacionamentos
    relationships = person.findall('hl7:personalRelationship', ns)
    mother = father = None
    for rel in relationships:
        code = rel.find('hl7:code', ns).attrib.get('code')
        name_info = rel.find('.//hl7:given', ns).text
        if code == 'PRN':
            mother = name_info
        elif code == 'NPRN':
            father = name_info

    # Outros IDs
    other_ids = []
    for role in person.findall('hl7:asOtherIDs', ns):
        for id_elem in role.findall('hl7:id', ns):
            other_ids.append(id_elem.attrib.get('extension', ''))

    return PatientInfo(
        full_name=name,
        birth_date=birth,
        gender=gender,
        cpf=cpf,
        phone=phone,
        address=address,
        mother_name=mother,
        father_name=father,
        marital_status=marital_status,
        race=race,
        other_ids=other_ids
    )
