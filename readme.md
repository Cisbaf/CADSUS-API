Documentação da API de Consulta ao Cadastro do SUS (CadSUS)
Visão Geral
Esta API permite consultar dados de cidadãos cadastrados no sistema CadSUS do Sistema Único de Saúde brasileiro. Através de uma requisição POST, é possível obter informações básicas e de contato de pacientes usando CPF ou CNS (Cartão Nacional de Saúde).

Endpoint Base:
http://cadsusapi.cisbaf.org.br/

Método: POST
Autenticação: Restrita a IPs autorizados

Estrutura da Requisição
Corpo da Requisição (JSON)
json
{
  "type_consult": "cpf",
  "value": "123.456.789-09"
}
Parâmetros:
Campo	Tipo	Valores Aceitos	Descrição
type_consult	string	cpf ou cns	Tipo de documento para consulta
value	string	-	Número do documento (com ou sem formatação)
Validações Automáticas:
CPF:

Será normalizado (removida pontuação)

Validado pelo algoritmo oficial de CPF

Exemplo válido: 123.456.789-09 → 12345678909

CNS:

Será normalizado (apenas dígitos numéricos)

Validado pelo algoritmo oficial de CNS

Exemplo válido: 123 4567 8901 2345 → 123456789012345

Respostas da API
Sucesso (200 OK)
json
{
  "full_name": "Maria da Silva",
  "birth_date": "1985-03-15",
  "gender": "F",
  "cpf": "12345678909",
  "phone": "(11) 99999-8888",
  "address": {
    "street": "Rua das Flores",
    "number": "123",
    "complement": "Apto 101",
    "neighborhood": "Centro",
    "city_code": "3550308",
    "state": "SP",
    "postal_code": "01000-000",
    "country_code": "BR"
  },
  "mother_name": "Ana Maria da Silva",
  "father_name": "José da Silva",
  "marital_status": "Casada",
  "race": "Parda",
  "other_ids": ["CNS:123456789012345"]
}
Estrutura de Resposta:
Campo	Tipo	Descrição
full_name	string	Nome completo
birth_date	string (ISO)	Data de nascimento (YYYY-MM-DD)
gender	string	Gênero (M/F)
cpf	string	CPF (apenas dígitos)
phone	string	Telefone (opcional)
address	Address	Objeto com dados de endereço
mother_name	string	Nome da mãe (opcional)
father_name	string	Nome do pai (opcional)
marital_status	string	Estado civil (opcional)
race	string	Raça/cor (opcional)
other_ids	string[]	Outros identificadores (opcional)
Estrutura do Endereço (Address):
Campo	Tipo	Descrição
street	string	Nome da rua (opcional)
number	string	Número (opcional)
complement	string	Complemento (opcional)
neighborhood	string	Bairro (opcional)
city_code	string	Código IBGE da cidade (opcional)
state	string	UF (opcional)
postal_code	string	CEP (opcional)
country_code	string	Código do país (opcional)
Erros Comuns:
422 Unprocessable Entity - Erro de validação:

json
{
  "detail": [
    {
      "loc": ["body", "value"],
      "msg": "CPF inválido",
      "type": "value_error"
    }
  ]
}
403 Forbidden
IP não autorizado para acesso à API

400 Bad Request
Estrutura da requisição inválida ou campos obrigatórios ausentes

Exemplos de Uso
Requisição com CPF válido
json
{
  "type_consult": "cpf",
  "value": "529.982.247-25"
}
Requisição com CNS válido
json
{
  "type_consult": "cns",
  "value": "898 0016 8403 0004"
}
Exemplo em Python (requests)
python
import requests

url = "http://cadsusapi.cisbaf.org.br/"
payload = {
    "type_consult": "cpf",
    "value": "52998224725"
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    print("Nome:", data["full_name"])
    print("CPF:", data["cpf"])
    print("Endereço:", data["address"]["street"], data["address"]["number"])
except requests.exceptions.HTTPError as err:
    if response.status_code == 422:
        print("Erro de validação:", response.json())
    else:
        print("Erro HTTP:", err)
Observações Importantes
A API só aceita requisições de IPs previamente autorizados

Todos os documentos são validados antes da consulta

Campos marcados como "opcional" podem retornar null ou estar ausentes

Formato de datas segue padrão ISO 8601 (YYYY-MM-DD)

Em caso de erro de validação, a mensagem indicará o problema específico:

CPF inválido

CNS inválido

type_consult deve ser 'cpf' ou 'cns'

Para solicitar acesso ou suporte técnico, entre em contato com a administração do sistema.

