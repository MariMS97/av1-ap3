from abc import ABC, abstractmethod
from datetime import datetime

class Pessoa(ABC):
    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str,
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str,
                 cidade_residencia: str, estado_residencia: str, estado_civil: str):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.cidade_natal = cidade_natal
        self.estado_natal = estado_natal
        self.cpf = cpf
        self.profissao = profissao
        self.cidade_residencia = cidade_residencia
        self.estado_residencia = estado_residencia
        self.estado_civil = estado_civil

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser um número inteiro positivo.")
        self._id = valor

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, valor):
        if not isinstance(valor, int) or not (0 <= valor <= 120):
            raise ValueError("Idade inválida.")
        self.__idade = valor

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, valor):
        if valor not in ['M', 'F', 'O']:
            raise ValueError("Gênero inválido.")
        self.__genero = valor

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_nascimento = valor
        except ValueError:
            raise ValueError("Data de nascimento inválida (DD/MM/AAAA).")

    @property
    def estado_civil(self):
        return self.__estado_civil

    @estado_civil.setter
    def estado_civil(self, valor):
        opcoes = ['Solteiro', 'Solteira', 'Casado', 'Casada', 'Divorciado', 'Divorciada', 'Viúvo', 'Viúva']
        if valor not in opcoes:
            raise ValueError("Estado civil inválido.")
        self.__estado_civil = valor

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF inválido.")
        self.__cpf = valor

    @abstractmethod
    def cadastrar(self): pass

    @abstractmethod
    def listar(self): pass

    @abstractmethod
    def editar(self, **kwargs): pass

    @abstractmethod
    def buscar(self, identificador): pass
