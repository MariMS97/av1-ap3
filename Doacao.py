# Importação da classe datetime para validação da data da doação
from datetime import datetime

# Classe que representa uma doação
class Doacao:
    # Construtor da classe, recebe id, data da doação e status
    def __init__(self, id: int, data_doacao: str, status: str):
        self.id = id                        # Atribuição com validação
        self.data_doacao = data_doacao      # Valida a data
        self.status = status                # Valida o status

    # Propriedade id com validação: deve ser um número inteiro
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int):
            raise ValueError("ID deve ser inteiro.")  # Lança exceção se não for inteiro
        self.__id = valor

    # Propriedade data_doacao com validação de formato DD/MM/AAAA
    @property
    def data_doacao(self):
        return self.__data_doacao

    @data_doacao.setter
    def data_doacao(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")  # Verifica se a data está no formato correto
            self.__data_doacao = valor
        except ValueError:
            raise ValueError("Data da doação inválida.")  # Erro se formato inválido

    # Propriedade status com validação de valor permitido
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in ['Realizada', 'Pendente', 'Cancelada']:  # Valida contra lista de opções permitidas
            raise ValueError("Status inválido.")  # Lança erro se status for inválido
        self.__status = valor

    # Método simples para indicar que uma doação foi registrada
    def registrar_doacao(self):
        print("Doação registrada com sucesso.")
