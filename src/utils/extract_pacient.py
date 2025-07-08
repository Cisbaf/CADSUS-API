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

    # Nome completo e social
    full_name_elem = person.find('hl7:name[@use="L"]/hl7:given', ns)
    full_name = full_name_elem.text if full_name_elem is not None else ''
    
    social_name_elem = person.find('hl7:name[@use="ASGN"]/hl7:given', ns)
    social_name = social_name_elem.text if social_name_elem is not None else None

    # Sexo
    gender_elem = person.find('hl7:administrativeGenderCode', ns)
    gender = gender_elem.attrib.get('code', '') if gender_elem is not None else ''

    # Data de nascimento
    birth_elem = person.find('hl7:birthTime', ns)
    birth_date = birth_elem.attrib.get('value', '') if birth_elem is not None else ''

    # Óbito
    deceased_elem = person.find('hl7:deceasedInd', ns)
    deceased = deceased_elem.attrib.get('value', 'false') == 'true' if deceased_elem is not None else False
    
    deceased_date = None
    if deceased:
        deceased_time = person.find('hl7:deceasedTime', ns)
        deceased_date = deceased_time.attrib.get('value') if deceased_time is not None else None

    # Telefone e email
    phone_elem = person.find('hl7:telecom[@use="PRN"]', ns)
    phone = phone_elem.attrib.get('value') if phone_elem is not None else None
    
    email_elem = person.find('hl7:telecom[@use="NET"]', ns)
    email = email_elem.attrib.get('value') if email_elem is not None else None

    # Endereço
    addr_elem = person.find('hl7:addr[@use="H"]', ns)
    address = Address()
    if addr_elem is not None:
        address = Address(
            street=addr_elem.findtext('hl7:streetName', default=None, namespaces=ns),
            number=addr_elem.findtext('hl7:houseNumber', default=None, namespaces=ns),
            complement=addr_elem.findtext('hl7:unitID', default=None, namespaces=ns),
            neighborhood=addr_elem.findtext('hl7:additionalLocator', default=None, namespaces=ns),
            city_code=addr_elem.findtext('hl7:city', default=None, namespaces=ns),
            state=addr_elem.findtext('hl7:state', default=None, namespaces=ns),
            postal_code=addr_elem.findtext('hl7:postalCode', default=None, namespaces=ns),
            country_code=addr_elem.findtext('hl7:country', default=None, namespaces=ns),
        )

    # Local de nascimento
    birth_place = person.find('hl7:birthPlace/hl7:addr', ns)
    birth_place_city = None
    birth_place_country = None
    if birth_place is not None:
        birth_place_city = birth_place.findtext('hl7:city', default=None, namespaces=ns)
        birth_place_country = birth_place.findtext('hl7:country', default=None, namespaces=ns)

    # Documentos (IDs)
    id_mapping = {
        '2.16.840.1.113883.13.236': 'cns',          # CNS
        '2.16.840.1.113883.13.237': 'cpf',          # CPF
        '2.16.840.1.113883.13.243': 'rg',           # RG
        '2.16.840.1.113883.13.244': 'ctps',         # CTPS
        '2.16.840.1.113883.13.238': 'cnh',          # CNH
        '2.16.840.1.113883.13.239': 'voter_id',     # Título de Eleitor
        '2.16.840.1.113883.13.240': 'nis',          # NIS
        '2.16.840.1.113883.3.3024': 'ric',          # RIC
        '2.16.840.1.113883.13.242': 'dnv',          # DNV
        '2.16.840.1.113883.4.330': 'passport',      # Passaporte
    }
    
    ids = {k: None for k in id_mapping.values()}
    other_ids = []
    
    # Processar asOtherIDs
    for other_id in person.findall('hl7:asOtherIDs', ns):
        for id_elem in other_id.findall('hl7:id', ns):
            root_val = id_elem.attrib.get('root')
            ext_val = id_elem.attrib.get('extension')
            if root_val in id_mapping:
                ids[id_mapping[root_val]] = ext_val
            elif ext_val:
                other_ids.append(ext_val)
    
    # Processar asCitizen (passaporte)
    citizen = person.find('hl7:asCitizen', ns)
    if citizen is not None:
        passport_elem = citizen.find('hl7:id[@root="2.16.840.1.113883.4.330"]', ns)
        if passport_elem is not None:
            ids['passport'] = passport_elem.attrib.get('extension')

    # Identificador local
    local_id_elem = person.find('hl7:id[@assigningAuthorityName]', ns)
    local_id = local_id_elem.attrib.get('extension') if local_id_elem is not None else None

    # Status VIP
    vip_elem = person.find('hl7:veryImportantPersonCode[@code="VIP"]', ns)
    vip = vip_elem is not None

    # Raça e etnia
    race_elem = person.find('hl7:raceCode', ns)
    race = race_elem.attrib.get('code') if race_elem is not None else None
    
    ethnicity_elem = person.find('hl7:ethnicGroupCode', ns)
    ethnicity = ethnicity_elem.attrib.get('code') if ethnicity_elem is not None else None

    # Estado civil
    marital_elem = person.find('hl7:maritalStatusCode', ns)
    marital_status = marital_elem.attrib.get('code') if marital_elem is not None else None

    # Relacionamentos (mãe/pai)
    relationships = person.findall('hl7:personalRelationship', ns)
    mother_name = None
    father_name = None
    
    for rel in relationships:
        code_elem = rel.find('hl7:code', ns)
        if code_elem is not None:
            code = code_elem.attrib.get('code')
            name_elem = rel.find('hl7:relationshipHolder1/hl7:name/hl7:given', ns)
            if name_elem is not None:
                if code == 'PRN':    # Mãe
                    mother_name = name_elem.text
                elif code == 'NPRN':  # Pai
                    father_name = name_elem.text

    return PatientInfo(
        full_name=full_name,
        social_name=social_name,
        birth_date=birth_date,
        gender=gender,
        cpf=ids['cpf'],
        cns=ids['cns'],
        phone=phone,
        email=email,
        address=address,
        mother_name=mother_name,
        father_name=father_name,
        marital_status=marital_status,
        race=race,
        ethnicity=ethnicity,
        deceased=deceased,
        deceased_date=deceased_date,
        birth_place_city_code=birth_place_city,
        birth_place_country_code=birth_place_country,
        rg=ids['rg'],
        ctps=ids['ctps'],
        cnh=ids['cnh'],
        voter_id=ids['voter_id'],
        nis=ids['nis'],
        passport=ids['passport'],
        ric=ids['ric'],
        dnv=ids['dnv'],
        local_id=local_id,
        vip=vip,
        other_ids=other_ids
    )