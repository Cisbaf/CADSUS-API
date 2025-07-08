# Documentação da API de Consulta ao Cadastro do SUS (CadSUS)

## Visão Geral
Esta API permite consultar dados de cidadãos cadastrados no sistema **CadSUS** do Sistema Único de Saúde brasileiro. Através de uma requisição **POST**, é possível obter informações básicas e de contato de pacientes usando **CPF** ou **CNS** (Cartão Nacional de Saúde).

- **Endpoint Base:** `http://cadsusapi.cisbaf.org.br/`
- **Método:** `POST`
- **Autenticação:** Restrita a IPs autorizados

---

## Estrutura da Requisição

### Corpo da Requisição (JSON)

```json
{
  "type_consult": "cpf",
  "value": "123.456.789-09"
}
```

| Campo        | Tipo   | Valores Aceitos | Descrição                              |
|--------------|--------|------------------|----------------------------------------|
| type_consult | string | cpf ou cns       | Tipo de documento para consulta        |
| value        | string | -                | Número do documento (com ou sem formatação) |

### Validações Automáticas:

**CPF:**
- Será normalizado (removida pontuação)
- Validado pelo algoritmo oficial de CPF
- Exemplo válido: `123.456.789-09` → `12345678909`

**CNS:**
- Será normalizado (apenas dígitos numéricos)
- Validado pelo algoritmo oficial de CNS
- Exemplo válido: `123 4567 8901 2345` → `123456789012345`

---

## Respostas da API

### Sucesso (200 OK)

```json
{
  "full_name": "ANA JULIA SANTOS DA SILVA",
  "birth_date": "20230613000000",
  "gender": "F",
  "cpf": "23412236721",
  "phone": "+55-21-976239245",
  "address": {
    "street": "CARLOS MAGNO DA SILVA",
    "number": "39",
    "complement": "",
    "neighborhood": "CERAMICA",
    "city_code": "330350",
    "state": "",
    "postal_code": "",
    "country_code": "010"
  },
  "mother_name": "JULIA COLITRE DOS SANTOS PINTO",
  "father_name": "WEVERTON SOUSA DA SILVA",
  "marital_status": null,
  "race": "03",
  "other_ids": [
    "898006330361527",
    "P",
    "706000343458946",
    "D",
    "23412236721",
    "30913635369"
  ]
}
```

### Observações da Resposta

| Campo           | Tipo              | Descrição                                                                 |
|------------------|-------------------|--------------------------------------------------------------------------|
| full_name       | string            | Nome completo                                                            |
| birth_date      | string (ISO ou AAAAMMDDhhmmss) | Data de nascimento                                                       |
| gender          | string            | Gênero (M/F)                                                             |
| cpf             | string            | CPF (apenas dígitos)                                                     |
| phone           | string            | Telefone com código de país (ex: `+55-21-99999-0000`)                    |
| address         | objeto            | Dados do endereço                                                        |
| mother_name     | string            | Nome da mãe                                                              |
| father_name     | string            | Nome do pai                                                              |
| marital_status  | string/null       | Estado civil (pode ser nulo)                                             |
| race            | string            | Código da raça (ex: `"03"` = Parda)                                      |
| other_ids       | string[]          | Outros identificadores (CNS, CPF duplicado, tipo de documento, etc.)     |

### Estrutura do Endereço (`address`)

| Campo        | Tipo   | Descrição                         |
|--------------|--------|-----------------------------------|
| street       | string | Nome da rua                       |
| number       | string | Número                            |
| complement   | string | Complemento                       |
| neighborhood | string | Bairro                            |
| city_code    | string | Código IBGE da cidade             |
| state        | string | UF (pode estar em branco)         |
| postal_code  | string | CEP (pode estar em branco)        |
| country_code | string | Código do país (ex: `"010"`)      |

---

## Erros Comuns

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
- IP não autorizado para acesso à API

### 400 Bad Request
- Estrutura da requisição inválida ou campos obrigatórios ausentes

---

## Exemplos de Uso

### Requisição com CPF válido

```json
{
  "type_consult": "cpf",
  "value": "23412236721"
}
```

### Requisição com CNS válido

```json
{
  "type_consult": "cns",
  "value": "898006330361527"
}
```

---

## Exemplo em Python (`requests`)

```python
import requests

url = "http://cadsusapi.cisbaf.org.br/"
payload = {
    "type_consult": "cpf",
    "value": "23412236721"
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    print("Nome:", data["full_name"])
    print("CPF:", data["cpf"])
    print("Nascimento:", data["birth_date"])
    print("Endereço:", data["address"]["street"], data["address"]["number"])
except requests.exceptions.HTTPError as err:
    if response.status_code == 422:
        print("Erro de validação:", response.json())
    else:
        print("Erro HTTP:", err)
```

---

## Observações Importantes

- A API **só aceita requisições de IPs previamente autorizados**
- Todos os documentos são **validados antes da consulta**
- Campos marcados como "opcional" podem retornar `null`, string vazia ou não aparecer
- A data de nascimento pode vir no formato **`YYYYMMDDhhmmss`**, e deve ser convertida para um formato mais legível conforme necessário
- O campo `race` pode vir como código numérico (`01` a `06`), seguindo padrão do CadSUS

---

> Para solicitar acesso ou suporte técnico, entre em contato com a administração do sistema.
