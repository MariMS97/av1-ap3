# Importação de módulos necessários: 'date' para trabalhar com datas e 'Pessoa' como classe base
from datetime import date
from Pessoa import Pessoa

# Classe Receptor herda de Pessoa
class Receptor(Pessoa):
    # Dicionário para armazenar os receptores cadastrados
    _receptores = {}

    # Construtor da classe Receptor, recebe informações relacionadas ao receptor
    def __init__(self, nome: str, idade: int, genero: str, data_nascimento: date, 
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str, 
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 orgao_necessario: str, gravidade_condicao: str, 
                 centro_transplante_vinculado: str, contato_emergencia: str, 
                 posicao_lista_espera: str):
        # Chama o construtor da classe base (Pessoa) para inicializar os atributos comuns
        super().__init__(nome, idade, genero, data_nascimento, cidade_natal, estado_natal, 
                         cpf, profissao, cidade_residencia, estado_residencia, estado_civil)
        # Inicializa os atributos específicos da classe Receptor
        self._orgao_necessario = orgao_necessario
        self._gravidade_condicao = gravidade_condicao
        self._centro_transplante_vinculado = centro_transplante_vinculado
        self._contato_emergencia = contato_emergencia
        self._posicao_lista_espera = posicao_lista_espera

    # Método de cadastro de receptor
    def cadastrar(self):
        # Verifica se já existe um receptor com o mesmo ID
        if self._id in Receptor._receptores:
            raise ValueError("Receptor já cadastrado com este ID.")
        # Adiciona o receptor ao dicionário de receptores
        Receptor._receptores[self._id] = self
        return True

    # Método de classe para listar todos os receptores cadastrados
    @classmethod
    def listar(cls):
        return cls._receptores

    # Método para editar os dados do receptor
    def editar(self, **kwargs):
        # Itera sobre os parâmetros passados para editar os atributos do receptor
        for key, value in kwargs.items():
            # Verifica se o receptor possui o atributo a ser editado
            if hasattr(self, f"_{key}"):
                # Se for o CPF, valida antes de atribuir
                if key == 'cpf':
                    value = self.validar_cpf(value)
                # Atribui o novo valor ao atributo
                setattr(self, f"_{key}", value)
        return True

    # Método de classe para buscar um receptor pelo ID ou CPF
    @classmethod
    def buscar(cls, identificador):
        # Se o identificador for um ID (inteiro), busca no dicionário de receptores
        if isinstance(identificador, int):
            return cls._receptores.get(identificador)
        # Se for um CPF (string), busca entre os receptores pelo CPF
        elif isinstance(identificador, str):
            for receptor in cls._receptores.values():
                if receptor._cpf == identificador:
                    return receptor
        # Se não encontrar, retorna None
        return None

    # Método para excluir o receptor do cadastro
    def excluir(self):
        # Verifica se o ID do receptor existe no dicionário de receptores
        if self._id in Receptor._receptores:
            # Remove o receptor do dicionário
            del Receptor._receptores[self._id]
            return True
        return False


