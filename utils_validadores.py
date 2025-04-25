import re
import json
import os

# Validação de CPF (simplificada para o exemplo)
def validar_cpf(cpf: str) -> bool:
    """
    Função para validar CPF.
    Para fins deste sistema, estamos validando apenas o formato.
    Um CPF válido tem 11 dígitos numéricos.
    """
    if len(cpf) == 11 and cpf.isdigit():
        return True
    return False

# Validação de E-mail
def validar_email(email: str) -> bool:
    """
    Função para validar e-mail no formato básico.
    Exemplo: nome@dominio.com
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    return False

# Validação de Idade (a idade precisa ser um número inteiro positivo)
def validar_idade(idade: int) -> bool:
    """
    Função para validar a idade.
    A idade deve ser maior que 0.
    """
    if isinstance(idade, int) and idade > 0:
        return True
    return False

# Validação de Tipo Sanguíneo
def validar_tipo_sanguineo(tipo: str) -> bool:
    """
    Função para validar o tipo sanguíneo.
    Aceita os tipos comuns (A+, A-, B+, B-, AB+, AB-, O+, O-).
    """
    tipos_validos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if tipo in tipos_validos:
        return True
    return False

#Validar e gerar ID simples
def gerar_id_simples(arquivo_json):
    if not os.path.exists(arquivo_json):
        return 1
    with open(arquivo_json, 'r') as f:
        try:
            dados = json.load(f)
            if not dados:
                return 1
            ultimos_ids = [int(item['id']) for item in dados if 'id' in item and item['id'].isdigit()]
            return max(ultimos_ids) + 1 if ultimos_ids else 1
        except json.JSONDecodeError:
            return 1