from datetime import date
from Pessoa import Pessoa

class Receptor(Pessoa):
    _receptores = {}

    def __init__(self, nome: str, idade: int, genero: str, data_nascimento: date, 
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str, 
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 orgao_necessario: str, gravidade_condicao: str, 
                 centro_transplante_vinculado: str, contato_emergencia: str, 
                 posicao_lista_espera: str):
        super().__init__(nome, idade, genero, data_nascimento, cidade_natal, estado_natal, 
                         cpf, profissao, cidade_residencia, estado_residencia, estado_civil)
        self._orgao_necessario = orgao_necessario
        self._gravidade_condicao = gravidade_condicao
        self._centro_transplante_vinculado = centro_transplante_vinculado
        self._contato_emergencia = contato_emergencia
        self._posicao_lista_espera = posicao_lista_espera

    # Método de cadastro de receptor
    def cadastrar(self):
        if self._id in Receptor._receptores:
            raise ValueError("Receptor já cadastrado com este ID.")
        Receptor._receptores[self._id] = self
        return True

    # Método para listar todos os receptores
    @classmethod
    def listar(cls):
        return cls._receptores

    # Método de edição do receptor
    def editar(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, f"_{key}"):
                if key == 'cpf':
                    value = self.validar_cpf(value)
                setattr(self, f"_{key}", value)
        return True

    # Método de busca de receptor
    @classmethod
    def buscar(cls, identificador):
        if isinstance(identificador, int):
            return cls._receptores.get(identificador)
        elif isinstance(identificador, str):
            for receptor in cls._receptores.values():
                if receptor._cpf == identificador:
                    return receptor
        return None

    # Método para excluir receptor
    def excluir(self):
        if self._id in Receptor._receptores:
            del Receptor._receptores[self._id]
            return True
        return False

