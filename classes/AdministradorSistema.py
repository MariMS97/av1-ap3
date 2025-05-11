
from classes.Pessoa import Pessoa
import json
import os


class AdministradorSistema(Pessoa):
    # Caminho do arquivo JSON onde os dados são armazenados
    ARQUIVO_ADMINISTRADORES = os.path.join('dados', r'jsons\admins.json')

    @classmethod
    def carregar_dados(cls):
        """Carrega os dados do arquivo JSON."""
        try:
            with open(cls.ARQUIVO_ADMINISTRADORES, 'r', encoding='utf-8') as f:
                return json.load(f)  # Carrega os dados do JSON
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retorna lista vazia se o arquivo não existir ou estiver com erro

    @classmethod
    def salvar_dados(cls, dados):
        """Salva os dados no arquivo JSON."""
        with open(cls.ARQUIVO_ADMINISTRADORES, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)  # Salva os dados no arquivo

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
        """Cadastra um novo administrador no sistema."""
        dados = self.carregar_dados()

        # Verifica se o ID ou nome de usuário já existem
        if any(adm['dados']['id'] == self.dados_pessoais['id'] for adm in dados):
            raise ValueError("ID já cadastrado.")
        if any(adm['acesso']['nome_usuario'] == self.acesso['nome_usuario'] for adm in dados):
            raise ValueError("Nome de usuário já existe.")

        # Adiciona o novo administrador
        novo_admin = {
            "dados": self.dados_pessoais,
            "acesso": self.acesso
        }
        dados.append(novo_admin)
        self.salvar_dados(dados)
        return f"Administrador {self.dados_pessoais['nome']} cadastrado com sucesso."

    @classmethod
    def listar(cls):
        """Lista todos os administradores cadastrados."""
        dados = cls.carregar_dados()
        if not dados:
            return "Nenhum administrador cadastrado."
        
        # Exibição formatada dos administradores
        for admin in dados:
            print(f"\nID: {admin['dados']['id']}")
            print(f"Nome: {admin['dados']['nome']}")
            print(f"Usuário: {admin['acesso']['nome_usuario']}")
            print("-" * 30)

    @classmethod
    def buscar(cls, id):
        """Busca um administrador pelo ID."""
        dados = cls.carregar_dados()
        for admin in dados:
            if admin['dados']['id'] == id:
                return AdministradorSistema(admin['dados'], admin['acesso'])
        return None

    def editar(self, **kwargs):
        """Edita os dados de um administrador."""
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
        raise ValueError("Administrador não encontrado.")

    @classmethod
    def excluir(cls, id):
        """Exclui um administrador pelo ID."""
        dados = cls.carregar_dados()
        for i, admin in enumerate(dados):
            if admin['dados']['id'] == id:
                nome = admin['dados']['nome']
                dados.pop(i)
                cls.salvar_dados(dados)
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
