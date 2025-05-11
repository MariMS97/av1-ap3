# Importação de módulos necessários: 'date' para trabalhar com datas e 'Pessoa' como classe base
from classes.Pessoa import Pessoa
import json
# Classe Receptor herda de Pessoa
class Receptor(Pessoa):
    # Dicionário para armazenar os receptores cadastrados
    _receptores = {}

    # Construtor da classe Receptor, recebe informações relacionadas ao receptor
    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str, 
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str, 
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 orgao_necessario: str, gravidade_condicao: str, 
                 centro_transplante_vinculado: str, contato_emergencia: str, 
                 posicao_lista_espera: str):
        # Chama o construtor da classe base (Pessoa) para inicializar os atributos comuns
        super().__init__(id, nome, idade, genero, data_nascimento, cidade_natal, estado_natal, 
                         cpf, profissao, cidade_residencia, estado_residencia, estado_civil)
        # Inicializa os atributos específicos da classe Receptor
        self._orgao_necessario = orgao_necessario
        self._gravidade_condicao = gravidade_condicao
        self._centro_transplante_vinculado = centro_transplante_vinculado
        self._contato_emergencia = contato_emergencia
        self._posicao_lista_espera = posicao_lista_espera

    # Método de cadastro de receptor
    def cadastrar(self):
     if self.id in Receptor._receptores:
        raise ValueError("Receptor já cadastrado com este ID.")
    
     Receptor._receptores[self.id] = self
    
     self.salvar_em_json()
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
        if self.__id in Receptor._receptores:
            # Remove o receptor do dicionário
            del Receptor._receptores[self.__id]
            return True
        return False
    
    def salvar_em_json(self):
        caminho_arquivo = r"jsons\receptores.json"

        # Carregar os dados existentes do arquivo (se existir)
        try:
            with open(caminho_arquivo, "r") as arquivo:
                dados_existentes = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            dados_existentes = []  # Se o arquivo não existir ou estiver vazio, inicializa como uma lista vazia

        # Criar um dicionário para o novo receptor
        novo_receptor = {
            "dados": {
                "id": self.id,
                "nome": self.nome,
                "idade": self.idade,
                "genero": self.genero,
                "data_nascimento": self.data_nascimento,
                "cidade_natal": self.cidade_natal,
                "estado_natal": self.estado_natal,
                "cpf": self.cpf,
                "profissao": self.profissao,
                "cidade_residencia": self.cidade_residencia,
                "estado_residencia": self.estado_residencia,
                "estado_civil": self.estado_civil,
                "orgao_necessario": self._orgao_necessario,
                "gravidade_condicao": self._gravidade_condicao,
                "centro_transplante_vinculado": self._centro_transplante_vinculado,
                "contato_emergencia": self._contato_emergencia,
                "posicao_lista_espera": self._posicao_lista_espera
            }
        }

        # Verificar se já existe um receptor com o mesmo ID
        for receptor in dados_existentes:
            if receptor["dados"]["id"] == self.id:
                raise ValueError("Receptor já cadastrado com este ID.")

        # Adicionar o novo receptor aos dados existentes
        dados_existentes.append(novo_receptor)

        # Salvar todos os dados no arquivo JSON
        with open(caminho_arquivo, "w") as arquivo:
            json.dump(dados_existentes, arquivo, indent=4)

