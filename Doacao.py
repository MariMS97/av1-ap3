from datetime import datetime
class Doacao:
    def __init__(self, id: int, data_doacao: str, status: str):
        self.id = id
        self.data_doacao = data_doacao
        self.status = status

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int):
            raise ValueError("ID deve ser inteiro.")
        self.__id = valor

    @property
    def data_doacao(self):
        return self.__data_doacao

    @data_doacao.setter
    def data_doacao(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_doacao = valor
        except ValueError:
            raise ValueError("Data da doação inválida.")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in ['Realizada', 'Pendente', 'Cancelada']:
            raise ValueError("Status inválido.")
        self.__status = valor

    def registrar_doacao(self):
        print("Doação registrada com sucesso.")