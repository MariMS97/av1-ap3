# Importação da classe datetime para validação da data da doação
from datetime import datetime

# Classe que representa uma doação
class Doacao:
    doacoes = {}  # Dicionário de doações registradas
    
    # Construtor da classe, recebe id, data da doação e status
    def __init__(self, tipo_doacao: str, id_doador: int, id_receptor: int, status: str):
        self.tipo_doacao = tipo_doacao
        self.id_doador = id_doador
        self.id_receptor = id_receptor
        self.data_doacao = datetime.now().strftime("%d/%m/%Y")  # Data atual
        self.status = status
        self.registrar_doacao()

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

    # Método para registrar a doação no dicionário interno
    def registrar_doacao(self):
        chave = f"{self.id_doador}-{self.id_receptor}"
        Doacao.doacoes[chave] = {
            "tipo_doacao": self.tipo_doacao,
            "data_doacao": self.data_doacao,
            "status": self.status
        }
        print(f"Doação registrada com sucesso: {chave}")

    # Método para listar as doações registradas
    @classmethod
    def listar_doacoes(cls):
        for chave, dados in cls.doacoes.items():
            print(f"ID: {chave} | Tipo: {dados['tipo_doacao']} | Data: {dados['data_doacao']} | Status: {dados['status']}")
