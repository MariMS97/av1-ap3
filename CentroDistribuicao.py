
import re
import json

class CentroDistribuicao:
    ORGAOS_VALIDOS = ["coração", "rim", "fígado", "pulmão", "pâncreas", "córnea"]

    def __init__(self, id, cidade, estado, endereco, telefone, estoque=None):
        self._id = id
        self._cidade = cidade
        self._estado = estado
        self._endereco = endereco
        self._telefone = self.validar_telefone(telefone)
        self._estoque = estoque if estoque else {}

    def validar_telefone(self, telefone: str) -> str:
        telefone = re.sub(r'[^0-9]', '', telefone)
        if len(telefone) not in [10, 11]:
            raise ValueError("Telefone inválido. Deve conter 10 ou 11 dígitos.")
        return telefone

    def exibir_estoque(self):
        print(f"\nid: {self._id} - {self._cidade}/{self._estado}")
        print("Endereço:", self._endereco)
        print("Telefone:", self._telefone)
        print("Estoque:")
        for orgao, quantidade in self._estoque.items():
            print(f"  - {orgao.capitalize()}: {quantidade}")

    @classmethod
    def carregar_centros_de_json(cls, caminho_arquivo):
        centros = []
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for centro in dados:
                    obj = cls(
                     centro['_id'],
                     centro['_cidade'],
                     centro['_estado'],
                     centro['_endereco'],
                     centro['_telefone'],
                     centro.get('_estoque', {})
                    )
                    centros.append(obj)
        except Exception as e:
            print(f"Erro ao carregar centros: {e}")
        return centros