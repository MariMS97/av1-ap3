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


def gerar_id_simples(caminho_arquivo):
    dados_existentes = carregar_dados_json(caminho_arquivo)
    
    if not dados_existentes:
        return 1
    
    try:
        # Obtendo o maior ID existente
        max_id = max(int(receptor["dados"]["id"]) for receptor in dados_existentes)
        return max_id + 1
    except KeyError as e:
        print(f"Chave não encontrada: {e}")
        return 1
    except ValueError:
        print("Erro de valor ao tentar gerar um novo ID.")
        return 1

    

def carregar_dados_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            # Verifica se é uma lista, se não for, inicializa como lista
            if not isinstance(dados, list):
                dados = []
            return dados
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON do arquivo {caminho_arquivo}.")
        return []