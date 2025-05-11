from datetime import datetime

class IntencaoDoar:

    def __init__(self, data_intencao: str, status: str, orgaos_id):
        self.data_intencao = data_intencao
        self.status = status
        self.__orgaos_id = orgaos_id

    @property
    def data_intencao(self):
        return self.__data_intencao

    @data_intencao.setter
    def data_intencao(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_intencao = valor
        except ValueError:
            raise ValueError("Data de intenção deve estar no formato DD/MM/AAAA.")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in ['Pendente', 'Confirmada', 'Cancelada']:
            raise ValueError("Status inválido.")
        self.__status = valor

    def registrar_intencao_doar(self):
        print("Intenção de doação registrada.")

    def atualizar_intencao_doar(self, nova_data, novo_status):
        self.data_intencao = nova_data
        self.status = novo_status

    # Método para converter para dicionário
    def to_dict(self):
        return {
            'data_intencao': self.data_intencao,
            'status': self.status
        }

    # Construtor alternativo para criar uma intenção com a data atual
    @classmethod
    def criar_intencao_automatica(cls, status="Pendente"):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        return cls(data_intencao=data_atual, status=status)
