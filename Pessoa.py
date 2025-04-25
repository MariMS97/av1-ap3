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
        return self.__id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser um número inteiro positivo.")
        self.__id = valor

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
            raise ValueError("Idade deve ser um número entre 0 e 120.")
        self.__idade = valor

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, valor):
        if valor not in ['M', 'F', 'O']:
            raise ValueError("Gênero deve ser 'M', 'F' ou 'O'.")
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
            raise ValueError("Data de nascimento deve estar no formato DD/MM/AAAA.")

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        self.__cpf = valor

    @abstractmethod
    def cadastrar(self):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def editar(self, **kwargs):
        pass

    @abstractmethod
    def buscar(self, identificador):
        pass

    @abstractmethod
    def excluir(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.nome} (ID: {self.id}, CPF: {self.cpf})"

    