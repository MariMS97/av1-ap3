# Importações necessárias
import re      # Usado para processar e validar o telefone com expressões regulares
import json    # Usado para carregar os dados de centros de um arquivo JSON

class CentroDistribuicao:
    # Lista de órgãos válidos que podem estar em estoque
    ORGAOS_VALIDOS =  ["Coração", "Rins", "Fígado", "Pâncreas", "Pulmões", "Intestino", 
                   "Córneas", "Pele", "Ossos", "Válvulas cardíacas", "Cartilagem", "Medula Óssea", 
                   "Tendões", "Vasos Sanguíneos", "Sangue de Cordão Umbilical", "Sangue Universal"]

    # Construtor da classe
    def __init__(self, id, cidade, estado, endereco, telefone, estoque=None):
        self._id = id                                # Identificador do centro
        self._cidade = cidade                        # Cidade onde o centro está localizado
        self._estado = estado                        # Estado onde o centro está localizado
        self._endereco = endereco                    # Endereço completo
        self._telefone = self.validar_telefone(telefone)  # Validação do número de telefone
        self._estoque = estoque if estoque else {}   # Estoque de órgãos (dicionário), inicializado vazio se não fornecido

    # Método para validar e formatar o número de telefone
    def validar_telefone(self, telefone: str) -> str:
        telefone = re.sub(r'[^0-9]', '', telefone)  # Remove tudo que não for número
        if len(telefone) not in [10, 11]:           # Deve conter 10 ou 11 dígitos
            raise ValueError("Telefone inválido. Deve conter 10 ou 11 dígitos.")
        return telefone

    # Método para exibir as informações do centro e seu estoque de órgãos
    def exibir_estoque(self):
        print(f"\nid: {self._id} - {self._cidade}/{self._estado}")
        print("Endereço:", self._endereco)
        print("Telefone:", self._telefone)
        print("Estoque:")
        for orgao, quantidade in self._estoque.items():
            print(f"  - {orgao.capitalize()}: {quantidade}")  # Mostra o nome do órgão com inicial maiúscula e sua quantidade

    # Método de classe para carregar múltiplos centros de distribuição a partir de um arquivo JSON
    @classmethod
    def carregar_centros_de_json(cls, caminho_arquivo):
        centros = []  # Lista que armazenará os objetos criados
        try:
            # Abre e lê o conteúdo do arquivo JSON
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for centro in dados:
                    # Para cada item no JSON, cria um objeto da classe e adiciona à lista
                    obj = cls(
                        centro['_id'],
                        centro['_cidade'],
                        centro['_estado'],
                        centro['_endereco'],
                        centro['_telefone'],
                        centro.get('_estoque', {})  # Pega o estoque ou um dicionário vazio se não existir
                    )
                    centros.append(obj)
        except Exception as e:
            # Em caso de erro, exibe mensagem informando o problema
            print(f"Erro ao carregar centros: {e}")
        return centros  # Retorna a lista de centros carregados
