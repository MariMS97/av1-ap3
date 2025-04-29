# Importação do módulo datetime para manipulação de datas
from datetime import datetime

# Classe IntencaoDoar que representa a intenção de doação
class IntencaoDoar:
    # Construtor que inicializa os atributos data_intencao e status
    def __init__(self, data_intencao: str, status: str):
        self.data_intencao = data_intencao  # Atribui a data da intenção
        self.status = status  # Atribui o status da intenção

    # Propriedade para data_intencao, com validação para garantir que a data esteja no formato correto
    @property
    def data_intencao(self):
        return self.__data_intencao  # Retorna o valor da data de intenção

    @data_intencao.setter
    def data_intencao(self, valor):
        try:
            # Tenta converter o valor para o formato de data DD/MM/AAAA
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_intencao = valor  # Se for válido, atribui o valor à variável interna
        except ValueError:
            # Se a data não for válida, lança um erro informando o formato esperado
            raise ValueError("Data de intenção deve estar no formato DD/MM/AAAA.")

    # Propriedade para o status da intenção de doação
    @property
    def status(self):
        return self.__status  # Retorna o valor do status

    @status.setter
    def status(self, valor):
        # Verifica se o status é um dos valores válidos ('Pendente', 'Confirmada', 'Cancelada')
        if valor not in ['Pendente', 'Confirmada', 'Cancelada']:
            raise ValueError("Status inválido.")  # Se não for válido, lança um erro
        self.__status = valor  # Se for válido, atribui o valor ao status

    # Método para registrar a intenção de doação, simula o processo
    def registrar_intencao_doar(self):
        print("Intenção de doação registrada.")  # Mensagem indicando que a intenção foi registrada

    # Método para atualizar a intenção de doação, mudando a data e o status
    def atualizar_intencao_doar(self, nova_data, novo_status):
        self.data_intencao = nova_data  # Atualiza a data de intenção
        self.status = novo_status  # Atualiza o status
