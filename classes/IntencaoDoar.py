from datetime import datetime

class IntencaoDoar:
    def __init__(self, data_intencao: str, status: str):
        self.data_intencao = data_intencao
        self.status = status

    @property
    def data_intencao(self):
        return self.__data_intencao

    @data_intencao.setter
    def data_intencao(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_intencao = valor
        except ValueError:
            raise ValueError("Data inválida (DD/MM/AAAA).")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in ['Pendente', 'Confirmada', 'Cancelada']:
            raise ValueError("Status inválido.")
        self.__status = valor

    def to_dict(self):
        return {
            'data_intencao': self.data_intencao,
            'status': self.status
        }
