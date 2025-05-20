from classes.Pessoa import Pessoa
from classes.IntencaoDoar import IntencaoDoar
import json

class Doador(Pessoa):
    doadores = {}

    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str,
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str,
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 contato_emergencia: str, tipo_sanguineo: str, intencao_doar=None):
        super().__init__(id, nome, idade, genero, data_nascimento, cidade_natal, estado_natal,
                         cpf, profissao, cidade_residencia, estado_residencia, estado_civil)
        self.contato_emergencia = contato_emergencia
        self.tipo_sanguineo = tipo_sanguineo
        self._orgaos_disponiveis = []

        if isinstance(intencao_doar, IntencaoDoar):
            self.intencao_doar = intencao_doar
        elif isinstance(intencao_doar, dict):
            self.intencao_doar = IntencaoDoar(**intencao_doar)
        else:
            self.intencao_doar = None

    @property
    def tipo_sanguineo(self):
        return self.__tipo_sanguineo

    @tipo_sanguineo.setter
    def tipo_sanguineo(self, valor):
        tipos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if valor not in tipos:
            raise ValueError("Tipo sanguíneo inválido.")
        self.__tipo_sanguineo = valor

    def cadastrar(self):
        if self._id in Doador.doadores:
            raise ValueError("Doador já cadastrado.")
        Doador.doadores[self._id] = self
        return True

    @classmethod
    def listar(cls):
        return cls.doadores

    def editar(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return True

    @classmethod
    def buscar(cls, identificador):
        if isinstance(identificador, int):
            return cls.doadores.get(identificador)
        elif isinstance(identificador, str):
            for d in cls.doadores.values():
                if d.cpf == identificador:
                    return d
        return None

    @classmethod
    def carregar_de_json(cls, caminho='jsons/doacoes.json'):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            for item in dados:
                dados_doador = item['dados']
                intencao = item.get('intencao', None)

                doador = cls(
                    id=dados_doador['id'],
                    nome=dados_doador['nome'],
                    idade=dados_doador['idade'],
                    genero=dados_doador['genero'],
                    data_nascimento=dados_doador['data_nascimento'],
                    cidade_natal=dados_doador['cidade_natal'],
                    estado_natal=dados_doador['estado_natal'],
                    cpf=dados_doador['cpf'],
                    profissao=dados_doador['profissao'],
                    cidade_residencia=dados_doador['cidade_residencia'],
                    estado_residencia=dados_doador['estado_residencia'],
                    estado_civil=dados_doador['estado_civil'],
                    contato_emergencia=dados_doador['contato_emergencia'],
                    tipo_sanguineo=dados_doador['tipo_sanguineo'],
                    intencao_doar=intencao
                )
                cls.doadores[doador.id] = doador
            return True
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return False
