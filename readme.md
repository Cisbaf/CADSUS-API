# 📄 Documentação da API de Consulta ao Cadastro do SUS (CadSUS) – Atualizada

## Visão Geral
Esta API permite consultar dados de cidadãos cadastrados no sistema **CadSUS** do Sistema Único de Saúde. Através de uma requisição **POST**, é possível obter informações pessoais, de contato e outros documentos associados ao cidadão, usando **CPF** ou **CNS**.

- **Endpoint Base:** `http://cadsusapi.cisbaf.org.br/`
- **Método:** `POST`
- **Autenticação:** Restrita a IPs autorizados

---

## 🔐 Requisição

### Corpo da Requisição (JSON)

```json
{
  "type_consult": "cpf",
  "value": "23412236721"
}
```

| Campo        | Tipo   | Valores Aceitos | Descrição                             |
|--------------|--------|------------------|---------------------------------------|
| type_consult | string | `cpf` ou `cns`   | Tipo de documento para consulta       |
| value        | string | -                | Número do documento (com ou sem máscara) |

---

## ✅ Resposta – Sucesso (200 OK)

### Exemplo

```json
{
  "full_name": "ANA JULIA SANTOS DA SILVA",
  "social_name": null,
  "birth_date": "20230613000000",
  "gender": "F",
  "cpf": "23412236721",
  "cns": "706000343458946",
  "phone": null,
  "email": null,
  "address": {
    "street": "CARLOS MAGNO DA SILVA",
    "number": "39",
    "complement": null,
    "neighborhood": "CERAMICA",
    "city_code": "330350",
    "state": null,
    "postal_code": null,
    "country_code": "010"
  },
  "mother_name": "JULIA COLITRE DOS SANTOS PINTO",
  "father_name": "WEVERTON SOUSA DA SILVA",
  "marital_status": null,
  "race": "03",
  "ethnicity": null,
  "deceased": false,
  "deceased_date": null,
  "birth_place_city_code": "330350",
  "birth_place_country_code": "010",
  "rg": null,
  "ctps": null,
  "cnh": null,
  "voter_id": null,
  "nis": null,
  "passport": null,
  "ric": null,
  "dnv": "30913635369",
  "local_id": null,
  "vip": false,
  "other_ids": ["P", "D"],
  "additional_info": {}
}
```

---

## 📌 Campos da Resposta

### Dados Pessoais

| Campo                    | Tipo     | Descrição                                        |
|--------------------------|----------|--------------------------------------------------|
| full_name               | string   | Nome completo do cidadão                         |
| social_name             | string/null | Nome social, se informado                        |
| birth_date              | string   | Data de nascimento no formato `YYYYMMDDhhmmss`   |
| gender                  | string   | Gênero (`M` ou `F`)                              |
| cpf                     | string/null | CPF (somente dígitos)                            |
| cns                     | string/null | Cartão Nacional de Saúde                         |
| phone                   | string/null | Número de telefone com DDD ou DDI                |
| email                   | string/null | E-mail                                           |
| mother_name             | string/null | Nome da mãe                                      |
| father_name             | string/null | Nome do pai                                      |
| marital_status          | string/null | Estado civil                                     |
| race                    | string/null | Código da raça (ex: `"03"` = Parda)              |
| ethnicity               | string/null | Etnia                                            |
| deceased                | boolean  | Indica se o paciente está falecido               |
| deceased_date           | string/null | Data do óbito (`YYYYMMDDhhmmss`)                |
| birth_place_city_code   | string/null | Código IBGE da cidade de nascimento              |
| birth_place_country_code| string/null | Código do país de nascimento                     |
| vip                     | boolean  | Indica se é um paciente VIP                      |

### Endereço (`address`)

| Campo        | Tipo   | Descrição                     |
|--------------|--------|-------------------------------|
| street       | string | Logradouro                    |
| number       | string | Número da residência           |
| complement   | string | Complemento do endereço        |
| neighborhood | string | Bairro                         |
| city_code    | string | Código IBGE da cidade          |
| state        | string | UF (estado)                    |
| postal_code  | string | CEP                            |
| country_code | string | Código do país (ex: `"010"`)   |

### Documentos Alternativos

| Campo     | Tipo       | Descrição                        |
|-----------|------------|----------------------------------|
| rg        | string/null| Registro Geral                   |
| ctps      | string/null| Carteira de Trabalho             |
| cnh       | string/null| Carteira Nacional de Habilitação|
| voter_id  | string/null| Título de Eleitor                |
| nis       | string/null| Número de Identificação Social   |
| passport  | string/null| Passaporte                       |
| ric       | string/null| Registro de Identidade Civil     |
| dnv       | string/null| Declaração de Nascido Vivo       |
| local_id  | string/null| Identificador local              |

### Outros

| Campo         | Tipo            | Descrição                                        |
|---------------|-----------------|--------------------------------------------------|
| other_ids     | array de string | Lista de identificadores complementares (ex: tipo de documento) |
| additional_info | objeto        | Informações adicionais customizadas (chave-valor) |

---

## ❌ Respostas de Erro

### 422 Unprocessable Entity – Erro de validação

```json
{
  "detail": [
    {
      "loc": ["body", "value"],
      "msg": "CPF inválido",
      "type": "value_error"
    }
  ]
}
```

### 403 Forbidden
- IP não autorizado

### 400 Bad Request
- Erro na estrutura da requisição ou campos inválidos

---

## 🧪 Exemplo de Código Python

```python
import requests

url = "http://cadsusapi.cisbaf.org.br/"
payload = {
    "type_consult": "cpf",
    "value": "23412236721"
}

response = requests.post(url, json=payload)
if response.ok:
    data = response.json()
    print("Nome:", data["full_name"])
    print("Data de nascimento:", data["birth_date"])
    print("Endereço:", data["address"]["street"], data["address"]["number"])
else:
    print("Erro:", response.status_code, response.json())
```

---

## ℹ️ Observações Finais

- A API **só aceita requisições de IPs autorizados**.
- Todos os documentos são **validados antes da consulta**.
- Campos podem vir como `null`, string vazia ou estar ausentes.
- A data pode vir no formato `YYYYMMDDhhmmss`, devendo ser convertida para algo legível (`dd/mm/aaaa`, por exemplo).
- O campo `race` segue os códigos do CadSUS (`01` a `06`).

---
