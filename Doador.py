# Importação da classe Pessoa (classe base da qual Doador herda)
from Pessoa import Pessoa
# Importação do módulo json para manipulação de dados JSON
import json

# Classe Doador, herda de Pessoa
class Doador(Pessoa):
    # Dicionário para armazenar os doadores, sendo a chave o ID do doador
    _doadores = {}

    # Construtor da classe Doador, inicializa os atributos da classe
    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str,
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str,
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 contato_emergencia: str, tipo_sanguineo: str):
        # Chama o construtor da classe base (Pessoa) para inicializar os atributos comuns
        super().__init__(id, nome, idade, genero, data_nascimento, cidade_natal,
                        estado_natal, cpf, profissao, cidade_residencia,
                        estado_residencia, estado_civil)
        # Atribui o contato de emergência e tipo sanguíneo, além de inicializar lista de órgãos disponíveis
        self.contato_emergencia = contato_emergencia
        self.tipo_sanguineo = tipo_sanguineo
        self._orgaos_disponiveis = []  # Lista de órgãos disponíveis para doação

    # Propriedade para tipo sanguíneo com validação dos tipos possíveis
    @property
    def tipo_sanguineo(self):
        return self.__tipo_sanguineo

    @tipo_sanguineo.setter
    def tipo_sanguineo(self, valor):
        # Tipos sanguíneos válidos
        tipos_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if valor not in tipos_validos:
            raise ValueError(f"Tipo sanguíneo inválido: {valor}")  # Erro se o valor não for válido
        self.__tipo_sanguineo = valor

    # Método para cadastrar um doador
    def cadastrar(self):
        if self.id in Doador._doadores:
            raise ValueError("Doador já cadastrado com este ID.")  # Erro se já existir um doador com o mesmo ID
        Doador._doadores[self.id] = self  # Adiciona o doador ao dicionário
        return True

    # Método de classe para listar todos os doadores cadastrados
    @classmethod
    def listar(cls):
        return cls._doadores  # Retorna o dicionário de doadores

    # Método para editar os dados do doador, passando novos valores através de kwargs
    def editar(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):  # Verifica se o atributo existe
                setattr(self, key, value)  # Atribui o novo valor
        return True

    # Método de classe para buscar doadores por ID ou CPF
    @classmethod
    def buscar(cls, identificador):
        if isinstance(identificador, int):
            return cls._doadores.get(identificador)  # Busca por ID
        elif isinstance(identificador, str):
            for doador in cls._doadores.values():
                if doador.cpf == identificador:  # Busca por CPF
                    return doador
        return None  # Retorna None se não encontrar o doador

    # Método de classe para carregar doadores a partir de um arquivo JSON
    @classmethod
    def carregar_de_json(cls, arquivo='doacoes.json'):
        try:
            with open(arquivo, 'r') as f:  # Abre o arquivo JSON
                dados = json.load(f)  # Carrega os dados JSON
            # Para cada item no JSON, cria um objeto Doador e o cadastra
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
                doador.cadastrar()  # Registra o doador no dicionário
            return True
        except Exception as e:
            print(f"Erro ao carregar doadores: {e}")  # Exibe erro caso ocorra
            return False

    # Método para converter o objeto Doador em um dicionário
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
            'orgaos_disponiveis': self._orgaos_disponiveis  # Inclui a lista de órgãos disponíveis
        }
