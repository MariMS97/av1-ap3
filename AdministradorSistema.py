from abc import ABC, abstractmethod
from Pessoa import Pessoa
import json

class AdministradorSistema(Pessoa):
    ARQUIVO_ADMINISTRADORES = 'administradores.json'
    
    @classmethod
    def carregar_dados(cls):
        try:
            with open(cls.ARQUIVO_ADMINISTRADORES, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def salvar_dados(cls, dados):
        with open(cls.ARQUIVO_ADMINISTRADORES, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def __init__(self, dados_pessoais, acesso):
        # Implementação dos métodos abstratos
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
        self.dados_pessoais = dados_pessoais
        self.acesso = acesso
        self.logado = False

    # Implementação dos métodos abstratos obrigatórios
    def cadastrar(self):
        dados = self.carregar_dados()
        
        if any(adm['dados']['id'] == self.dados_pessoais['id'] for adm in dados):
            raise ValueError("ID já cadastrado")
            
        if any(adm['acesso']['nome_usuario'] == self.acesso['nome_usuario'] for adm in dados):
            raise ValueError("Nome de usuário já existe")
            
        novo_admin = {
            "dados": self.dados_pessoais,
            "acesso": self.acesso
        }
        
        dados.append(novo_admin)
        self.salvar_dados(dados)
        return f"Administrador {self.dados_pessoais['nome']} cadastrado com sucesso."

    @classmethod
    def listar(cls):
        return cls.carregar_dados()

    @classmethod
    def buscar(cls, id):
        dados = cls.carregar_dados()
        for admin in dados:
            if admin['dados']['id'] == id:
                return AdministradorSistema(admin['dados'], admin['acesso'])
        return None

    def editar(self, **kwargs):
        dados = self.carregar_dados()
        for admin in dados:
            if admin['dados']['id'] == self.dados_pessoais['id']:
                for chave, valor in kwargs.items():
                    if chave in admin['dados']:
                        admin['dados'][chave] = valor
                    elif chave in admin['acesso']:
                        admin['acesso'][chave] = valor
                self.salvar_dados(dados)
                return f"Dados do administrador {self.dados_pessoais['nome']} atualizados."
        raise ValueError("Administrador não encontrado")

    @classmethod
    def excluir(cls, id):
        dados = cls.carregar_dados()
        for i, admin in enumerate(dados):
            if admin['dados']['id'] == id:
                nome = admin['dados']['nome']
                dados.pop(i)
                cls.salvar_dados(dados)
                return f"Administrador {nome} removido com sucesso."
        raise ValueError("Administrador não encontrado")

    # Métodos específicos do Administrador
    @classmethod
    def buscar_por_usuario(cls, nome_usuario):
        dados = cls.carregar_dados()
        for admin in dados:
            if admin['acesso']['nome_usuario'] == nome_usuario:
                return AdministradorSistema(admin['dados'], admin['acesso'])
        return None

    def login(self, senha):
        if self.acesso['senha'] == senha:
            self.logado = True
            return True
        return False

    def logout(self):
        self.logado = False
        return True

    # Métodos de autenticação
def login(self, usuario, senha):
        if self.nome_usuario == usuario and self.senha == senha:
            self.logado = True
            return True
        return False

def logout(self):
        self.logado = False
        return True

def recuperar_senha(self):
        if not self.email:
            return "Nenhum email cadastrado para recuperação."
        return f"Instruções enviadas para {self.email}"

    # Métodos de gerenciamento simplificados para integração com app.py
def gerenciar_pessoas(self):
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        return "Redirecionando para gerenciamento de pessoas..."

def listar_orgaos_tipos(self):
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        try:
            with open('orgãos_tipos.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados.get('orgaos', []), dados.get('tipos_de_orgaos', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return [], []
def gerenciar_centros_distribuicao(self):
        if not self.logado:
            raise PermissionError("Acesso negado. Faça login primeiro.")
        return "Redirecionando para gerenciamento de centros..."