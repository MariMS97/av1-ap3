from datetime import date
from Pessoa import Pessoa
import json

class Doador(Pessoa):
    _doadores = {}  # Dicionário para armazenar doadores

    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str,
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str,
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 contato_emergencia: str, tipo_sanguineo: str):
        super().__init__(id, nome, idade, genero, data_nascimento, cidade_natal,
                        estado_natal, cpf, profissao, cidade_residencia,
                        estado_residencia, estado_civil)
        self.contato_emergencia = contato_emergencia
        self.tipo_sanguineo = tipo_sanguineo
        self._orgaos_disponiveis = []

    @property
    def tipo_sanguineo(self):
        return self.__tipo_sanguineo

    @tipo_sanguineo.setter
    def tipo_sanguineo(self, valor):
        tipos_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if valor not in tipos_validos:
            raise ValueError(f"Tipo sanguíneo inválido: {valor}")
        self.__tipo_sanguineo = valor

    def cadastrar(self):
        if self.id in Doador._doadores:
            raise ValueError("Doador já cadastrado com este ID.")
        Doador._doadores[self.id] = self
        return True

    @classmethod
    def listar(cls):
        return cls._doadores

    def editar(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return True

    @classmethod
    def buscar(cls, identificador):
        if isinstance(identificador, int):
            return cls._doadores.get(identificador)
        elif isinstance(identificador, str):
            for doador in cls._doadores.values():
                if doador.cpf == identificador:
                    return doador
        return None

    @classmethod
    def carregar_de_json(cls, arquivo='doacoes.json'):
        try:
            with open(arquivo, 'r') as f:
                dados = json.load(f)
            
            for item in dados:
                doador = cls(
                    id=item['id'],
                    nome=item['nome'],
                    idade=item['idade'],
                    genero=item['genero'],
                    data_nascimento=item['data_nascimento'],
                    cidade_natal=item['cidade_natal'],
                    estado_natal=item['estado_natal'],
                    cpf=item['cpf'],
                    profissao=item['profissao'],
                    cidade_residencia=item['cidade_residencia'],
                    estado_residencia=item['estado_residencia'],
                    estado_civil=item['estado_civil'],
                    contato_emergencia=item['contato_emergencia'],
                    tipo_sanguineo=item['tipo_sanguineo']
                )
                doador.cadastrar()
            return True
        except Exception as e:
            print(f"Erro ao carregar doadores: {e}")
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'genero': self.genero,
            'data_nascimento': self.data_nascimento,
            'cidade_natal': self.cidade_natal,
            'estado_natal': self.estado_natal,
            'cpf': self.cpf,
            'profissao': self.profissao,
            'cidade_residencia': self.cidade_residencia,
            'estado_residencia': self.estado_residencia,
            'estado_civil': self.estado_civil,
            'contato_emergencia': self.contato_emergencia,
            'tipo_sanguineo': self.tipo_sanguineo,
            'orgaos_disponiveis': self._orgaos_disponiveis
        }