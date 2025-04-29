# Importações necessárias
from abc import ABC, abstractmethod  # ABC e abstractmethod são utilizados para definir classes e métodos abstratos (não usados diretamente aqui)
import json  # Para leitura e escrita em arquivos JSON
import os  # Para operações com o sistema de arquivos (não usado diretamente aqui)
from Pessoa import Pessoa  # Importa a classe base Pessoa

# Classe AdministradorSistema herda de Pessoa
class AdministradorSistema(Pessoa):
    # Constante com o nome do arquivo onde os dados dos administradores serão armazenados
    ARQUIVO_ADMINISTRADORES = 'admins.json'
    
    @classmethod
    def carregar_dados(cls):
        """Carrega os dados do arquivo JSON"""
        try:
            with open(cls.ARQUIVO_ADMINISTRADORES, 'r', encoding='utf-8') as f:
                return json.load(f)  # Tenta carregar os dados do JSON
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retorna lista vazia se o arquivo não existir ou estiver com erro

    @classmethod
    def salvar_dados(cls, dados):
        """Salva os dados no arquivo JSON"""
        with open(cls.ARQUIVO_ADMINISTRADORES, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)  # Salva dados no arquivo com formatação legível

    def __init__(self, dados_pessoais, acesso):
        # Inicializa atributos herdados da classe Pessoa com base em um dicionário
        super().__init__(
            id=dados_pessoais['id'],
            nome=dados_pessoais['nome'],
            idade=dados_pessoais['idade'],
            genero=dados_pessoais['sexo'],
            data_nascimento=dados_pessoais['data_nascimento'],
            cidade_natal=dados_pessoais['cidade_natal'],
            estado_natal=dados_pessoais['estado_natal'],
            cpf=dados_pessoais['cpf'],
            profissao=dados_pessoais['profissao'],
            cidade_residencia=dados_pessoais['cidade_residencia'],
            estado_residencia=dados_pessoais['estado_residencia'],
            estado_civil=dados_pessoais['estado_civil']
        )
        self.dados_pessoais = dados_pessoais  # Guarda os dados pessoais
        self.acesso = acesso  # Guarda os dados de acesso (ex: nome de usuário e senha)
        self.logado = False  # Por padrão, o administrador não está logado

    def cadastrar(self):
        """Cadastra um novo administrador no sistema"""
        dados = self.carregar_dados()  # Carrega lista de administradores já cadastrados

        # Verifica se o ID já foi cadastrado
        if any(adm['dados']['id'] == self.dados_pessoais['id'] for adm in dados):
            raise ValueError("ID já cadastrado")

        # Verifica se o nome de usuário já existe
        if any(adm['acesso']['nome_usuario'] == self.acesso['nome_usuario'] for adm in dados):
            raise ValueError("Nome de usuário já existe")

        # Cria um novo dicionário com os dados pessoais e de acesso
        novo_admin = {
            "dados": self.dados_pessoais,
            "acesso": self.acesso
        }

        dados.append(novo_admin)  # Adiciona o novo administrador à lista
        self.salvar_dados(dados)  # Salva a lista atualizada no arquivo JSON
        return f"Administrador {self.dados_pessoais['nome']} cadastrado com sucesso."

    @classmethod
    def listar(cls):
        """Lista todos os administradores cadastrados"""
        return cls.carregar_dados()  # Retorna a lista de administradores

    @classmethod
    def buscar(cls, id):
        """Busca um administrador pelo ID"""
        dados = cls.carregar_dados()  # Carrega os dados
        for admin in dados:
            if admin['dados']['id'] == id:
                # Cria e retorna um objeto AdministradorSistema com os dados encontrados
                return AdministradorSistema(admin['dados'], admin['acesso'])
        return None  # Retorna None se não encontrar

    def editar(self, **kwargs):
        """Edita os dados de um administrador"""
        dados = self.carregar_dados()
        for admin in dados:
            if admin['dados']['id'] == self.dados_pessoais['id']:  # Localiza o admin pelo ID
                for chave, valor in kwargs.items():
                    if chave in admin['dados']:
                        admin['dados'][chave] = valor  # Atualiza dados pessoais
                    elif chave in admin['acesso']:
                        admin['acesso'][chave] = valor  # Atualiza dados de acesso
                self.salvar_dados(dados)
                return f"Dados do administrador {self.dados_pessoais['nome']} atualizados."
        raise ValueError("Administrador não encontrado")

    @classmethod
    def excluir(cls, id):
        """Exclui um administrador pelo ID"""
        dados = cls.carregar_dados()
        for i, admin in enumerate(dados):
            if admin['dados']['id'] == id:
                nome = admin['dados']['nome']
                dados.pop(i)  # Remove o administrador da lista
                cls.salvar_dados(dados)  # Salva a nova lista
                return f"Administrador {nome} removido com sucesso."
        raise ValueError("Administrador não encontrado")

    # Métodos de autenticação
    def login(self, senha):
        """Realiza login validando a senha"""
        if self.acesso['senha'] == senha:
            self.logado = True  # Marca como logado
            return True
        return False  # Senha incorreta

    def logout(self):
        """Realiza logout do sistema"""
        self.logado = False
        return True

    # Métodos auxiliares
    def recuperar_senha(self):
        """Simula recuperação de senha (requer email configurado)"""
        if not hasattr(self, 'email') or not self.email:
            return "Nenhum email cadastrado para recuperação."
        return f"Instruções enviadas para {self.email}"

    def gerenciar_pessoas(self):
        """Permite gerenciar pessoas se estiver logado"""
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        return "Redirecionando para gerenciamento de pessoas..."

    def listar_orgaos_tipos(self):
        """Lista os órgãos e tipos de órgãos cadastrados"""
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        try:
            with open('orgãos_tipos.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados.get('orgaos', []), dados.get('tipos_de_orgaos', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return [], []  # Retorna listas vazias em caso de erro

    def gerenciar_centros_distribuicao(self):
        """Permite acesso ao gerenciamento de centros de distribuição"""
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        return "Redirecionando para gerenciamento de centros..."
