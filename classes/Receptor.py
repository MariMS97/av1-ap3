from classes.Pessoa import Pessoa
import json


class Receptor(Pessoa):
    receptores = {}

    def __init__(self, id: int, nome: str, idade: int, genero: str, data_nascimento: str, 
                 cidade_natal: str, estado_natal: str, cpf: str, profissao: str, 
                 cidade_residencia: str, estado_residencia: str, estado_civil: str,
                 orgao_necessario: str, gravidade_condicao: str, 
                 centro_transplante_vinculado: str, contato_emergencia: str, 
                 posicao_lista_espera: str, tipo_sanguineo: str):
        super().__init__(id, nome, idade, genero, data_nascimento, cidade_natal, estado_natal, 
                         cpf, profissao, cidade_residencia, estado_residencia, estado_civil)
        self.tipo_sanguineo = tipo_sanguineo
        self._orgao_necessario = orgao_necessario
        self._gravidade_condicao = gravidade_condicao
        self._centro_transplante_vinculado = centro_transplante_vinculado
        self._contato_emergencia = contato_emergencia
        self._posicao_lista_espera = posicao_lista_espera

    def cadastrar(self):
        if self.id in Receptor.receptores:
            raise ValueError("Receptor já cadastrado com este ID.")
        
        Receptor.receptores[self.id] = {
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
            "tipo_sanguineo": self.tipo_sanguineo,
            "orgao_necessario": self._orgao_necessario,
            "gravidade_condicao": self._gravidade_condicao,
            "centro_transplante_vinculado": self._centro_transplante_vinculado,
            "contato_emergencia": self._contato_emergencia,
            "posicao_lista_espera": self._posicao_lista_espera
        }
        return True

    @classmethod
    def listar(cls):
        return cls.receptores

    def editar(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, f"_{key}"):
                if key == 'cpf':
                    value = self.validar_cpf(value)
                setattr(self, f"_{key}", value)
        return True

    @classmethod
    def buscar(cls, identificador):
        if isinstance(identificador, int):
            return cls._receptores.get(identificador)
        elif isinstance(identificador, str):
            for receptor in cls._receptores.values():
                if receptor.get("cpf") == identificador:
                    return receptor
        return None

    def excluir(self):
        if self.id in Receptor.receptores:
            del Receptor.receptores[self.id]
            return True
        return False

    @classmethod
    def carregar_dados_do_json(cls):
        caminho_arquivo = r"jsons/receptores.json"
        try:
            with open(caminho_arquivo, "r") as arquivo:
                dados = json.load(arquivo)
                for item in dados:
                    receptor_data = item["dados"]
                    cls._receptores[receptor_data["id"]] = receptor_data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Arquivo JSON não encontrado ou vazio.")
            pass
