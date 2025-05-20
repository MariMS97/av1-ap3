from classes.Pessoa import Pessoa
import json

class AdministradorSistema(Pessoa):
    ARQUIVO_ADMINISTRADORES = "administradores.json"  # caminho do JSON

    administradores = {}  # dicionário interno, estático para todos os objetos

    @classmethod
    def carregar_dados(cls):
        """Carrega os dados do arquivo JSON para o dicionário interno apenas uma vez."""
        if not cls.administradores:
            try:
                with open(cls.ARQUIVO_ADMINISTRADORES, 'r', encoding='utf-8') as f:
                    cls.administradores = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                cls.administradores = []

    def __init__(self, dados_pessoais, acesso):
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

    def cadastrar(self):
        """Cadastra um novo administrador no dicionário interno."""
        self.carregar_dados()

        if any(adm['dados']['id'] == self.dados_pessoais['id'] for adm in self.administradores):
            raise ValueError("ID já cadastrado.")
        if any(adm['acesso']['nome_usuario'] == self.acesso['nome_usuario'] for adm in self.administradores):
            raise ValueError("Nome de usuário já existe.")

        novo_admin = {
            "dados": self.dados_pessoais,
            "acesso": self.acesso
        }
        self.administradores.append(novo_admin)
        return f"Administrador {self.dados_pessoais['nome']} cadastrado com sucesso."

    @classmethod
    def listar(cls):
        """Lista todos os administradores do dicionário interno."""
        cls.carregar_dados()
        if not cls.administradores:
            return "Nenhum administrador cadastrado."

        for admin in cls.administradores:
            print(f"\nID: {admin['dados']['id']}")
            print(f"Nome: {admin['dados']['nome']}")
            print(f"Usuário: {admin['acesso']['nome_usuario']}")
            print("-" * 30)

    @classmethod
    def buscar(cls, id):
        """Busca um administrador pelo ID no dicionário interno."""
        cls.carregar_dados()
        for admin in cls.administradores:
            if admin['dados']['id'] == id:
                return AdministradorSistema(admin['dados'], admin['acesso'])
        return None

    def editar(self, **kwargs):
        """Edita os dados de um administrador no dicionário interno."""
        self.carregar_dados()
        for admin in self.administradores:
            if admin['dados']['id'] == self.dados_pessoais['id']:
                for chave, valor in kwargs.items():
                    if chave in admin['dados']:
                        admin['dados'][chave] = valor
                    elif chave in admin['acesso']:
                        admin['acesso'][chave] = valor
                return f"Dados do administrador {self.dados_pessoais['nome']} atualizados."
        raise ValueError("Administrador não encontrado.")

    @classmethod
    def excluir(cls, id):
        """Exclui um administrador pelo ID no dicionário interno."""
        cls.carregar_dados()
        for i, admin in enumerate(cls.administradores):
            if admin['dados']['id'] == id:
                nome = admin['dados']['nome']
                cls.administradores.pop(i)
                return f"Administrador {nome} removido com sucesso."
        raise ValueError("Administrador não encontrado.")

    def login(self, senha):
        """Realiza login validando a senha."""
        if self.acesso['senha'] == senha:
            self.logado = True
            return True
        return False

    def logout(self):
        """Realiza logout do sistema."""
        self.logado = False
        return True
