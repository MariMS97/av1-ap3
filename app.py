
from utils import gerar_id_simples
from classes.Doador import Doador
from classes.Receptor import Receptor
from classes.AdministradorSistema import AdministradorSistema
from classes.Doacao import Doacao
from classes.CentroDistribuicao import CentroDistribuicao
from classes.IntencaoDoar import IntencaoDoar
from utils import carregar_dados_json  


# Função para cadastrar um novo doador
def cadastro_doador():
    print("\n--- Cadastro de Doador ---")

    # Coletando os dados do Doador
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    genero = input("Gênero: ")
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    cidade_natal = input("Cidade natal: ")
    estado_natal = input("Estado natal: ")
    cpf = input("CPF: ")
    profissao = input("Profissão: ")
    cidade_residencia = input("Cidade de residência: ")
    estado_residencia = input("Estado de residência: ")
    estado_civil = input("Estado civil: ")
    contato_emergencia = input("Contato de emergência: ")
    tipo_sanguineo = input("Tipo sanguíneo: ")
    
    # Geração de ID único para o doador (caso não exista um método, podemos criar um)
    id_gerado = max(Doador._doadores.keys(), default=0) + 1

    # Coletando dados para a Intenção de Doação
    status = input("Status da intenção (Pendente/Confirmada/Cancelada): ")
    data_intencao = input("Data de intenção (DD/MM/AAAA): ")
    orgaos_id = input("Órgãos para doação (separados por vírgula): ").split(',')

    # Removendo espaços desnecessários nos IDs de órgãos
    orgaos_id = [orgao.strip() for orgao in orgaos_id if orgao.strip()]

    # Criação do objeto IntencaoDoar
    intencao = IntencaoDoar(data_intencao=data_intencao, status=status, orgaos_id=orgaos_id)

    # Criação do objeto Doador com a Intenção de Doar
    doador = Doador(
        id=id_gerado,
        nome=nome,
        idade=idade,
        genero=genero,
        data_nascimento=data_nascimento,
        cidade_natal=cidade_natal,
        estado_natal=estado_natal,
        cpf=cpf,
        profissao=profissao,
        cidade_residencia=cidade_residencia,
        estado_residencia=estado_residencia,
        estado_civil=estado_civil,
        contato_emergencia=contato_emergencia,
        tipo_sanguineo=tipo_sanguineo,
        intencao_doar=intencao  # <- Aqui está correto, só passa o objeto, não precisa duplicar
    )

    # Cadastra no dicionário da classe (não salva em JSON)
    try:
        doador.cadastrar()
        print("Doador cadastrado com sucesso!")
    except ValueError as e:
        print(f"Erro ao cadastrar doador: {e}")


def cadastro_receptor():
    try:
        print("\n--- Cadastro de Receptor ---")

        # Geração de ID automático
        if Receptor._receptores:
            # Pega o maior ID existente no dicionário e adiciona 1
            novo_id = max(Receptor._receptores.keys()) + 1
        else:
            novo_id = 1  # Caso o dicionário esteja vazio, começa pelo ID 1
        
        print(f"ID gerado automaticamente: {novo_id}")

        # Coleta dos dados do receptor
        nome = input("Nome: ")
        idade = int(input("Idade: "))
        genero = input("Gênero: ")
        data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        cidade_natal = input("Cidade natal: ")
        estado_natal = input("Estado natal: ")
        cpf = input("CPF: ")
        profissao = input("Profissão: ")
        cidade_residencia = input("Cidade de residência: ")
        estado_residencia = input("Estado de residência: ")
        estado_civil = input("Estado civil: ")

        # Campos específicos do receptor
        orgao_necessario = input("Órgão necessário: ")
        gravidade_condicao = input("Gravidade da condição: ")
        centro_transplante_vinculado = input("Centro de transplante vinculado: ")
        contato_emergencia = input("Contato de emergência: ")
        posicao_lista_espera = int(input("Posição na lista de espera: "))

        # Criação do objeto Receptor
        receptor = Receptor(
            id=novo_id,  # ID gerado automaticamente
            nome=nome,
            idade=idade,
            genero=genero,
            data_nascimento=data_nascimento,
            cidade_natal=cidade_natal,
            estado_natal=estado_natal,
            cpf=cpf,
            profissao=profissao,
            cidade_residencia=cidade_residencia,
            estado_residencia=estado_residencia,
            estado_civil=estado_civil,
            orgao_necessario=orgao_necessario,
            gravidade_condicao=gravidade_condicao,
            centro_transplante_vinculado=centro_transplante_vinculado,
            contato_emergencia=contato_emergencia,
            posicao_lista_espera=posicao_lista_espera
        )

        # Cadastro no dicionário interno
        sucesso = receptor.cadastrar()
        if sucesso:
            print("Receptor cadastrado com sucesso!")

    except ValueError as e:
        print(f"Erro no cadastro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# Função para cadastrar um novo administrador
def cadastro_administrador():
    """Função para cadastrar um novo administrador no sistema."""
    try:
        print("\n--- Cadastro de Administrador ---")

        # Gerando um ID único para o novo administrador
        novo_id = gerar_id_simples()

        # Entrando com os dados de acesso
        nome_usuario = input("Nome de usuário: ").strip()

        # Verifica se o nome de usuário já está em uso
        if any(admin.acesso["nome_usuario"] == nome_usuario for admin in AdministradorSistema.administradores):
            print(f"Erro: o nome de usuário '{nome_usuario}' já está em uso.")
            return

        senha = input("Senha: ").strip()

        # Entrando com os dados pessoais
        nome = input("Nome completo: ").strip()
        idade = int(input("Idade: "))
        if idade <= 0 or idade > 80:
            raise ValueError("Idade inválida.")

        sexo = input("Sexo (M/F): ").strip().upper()
        data_nascimento = input("Data nascimento (DD/MM/AAAA): ").strip()
        cidade_natal = input("Cidade natal: ").strip()
        estado_natal = input("Estado natal (sigla): ").strip().upper()
        cpf = input("CPF (apenas números): ").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos numéricos.")

        profissao = input("Profissão: ").strip()
        cidade_residencia = input("Cidade residência: ").strip()
        estado_residencia = input("Estado residência (sigla): ").strip().upper()
        estado_civil = input("Estado civil: ").strip()
        contato_emergencia = input("Contato emergência: ").strip()
        tipo_sanguineo = input("Tipo sanguíneo: ").strip().upper()

        # Criando o dicionário de dados pessoais do novo administrador
        dados_pessoais = {
            "id": novo_id,
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "data_nascimento": data_nascimento,
            "cidade_natal": cidade_natal,
            "estado_natal": estado_natal,
            "cpf": cpf,
            "profissao": profissao,
            "cidade_residencia": cidade_residencia,
            "estado_residencia": estado_residencia,
            "estado_civil": estado_civil,
            "contato_emergencia": contato_emergencia,
            "tipo_sanguineo": tipo_sanguineo
        }

        # Criando o dicionário de acesso do novo administrador
        acesso = {
            "nome_usuario": nome_usuario,
            "senha": senha
        }

        # Instanciando o objeto AdministradorSistema
        admin = AdministradorSistema(dados_pessoais, acesso)

        # Adiciona ao dicionário interno da classe
        AdministradorSistema.administradores.append(admin)

        # Exibe mensagem de sucesso
        print(f"\nAdministrador {admin.dados_pessoais['nome']} cadastrado com sucesso.")

    except ValueError as ve:
        print(f"\n[Erro de Validação] {ve}")
    except Exception as e:
        print(f"\n[Erro Inesperado] {str(e)}")


# Função para login do administrador
def login_administrador():
    nome_usuario = input("Digite o nome de usuário: ").strip()
    senha = input("Digite a senha: ").strip()

    for admin in AdministradorSistema.administradores:
        if admin.acesso['nome_usuario'] == nome_usuario and admin.acesso['senha'] == senha:
            print("Login bem-sucedido!")
            return admin
    print("Credenciais inválidas!")
    return None


# Função para logout do administrador
def logout_administrador(admin):
    if admin:
        admin.logout()
        print("Logout realizado com sucesso!")
    else:
        print("Nenhum administrador logado.")


# Função para recuperar senha
def recuperar_senha():
    email = input("Digite o email cadastrado: ")
    print(f"Instruções para redefinição enviadas para {email}")
    return True

""# Função para gerenciar pessoas (doadores e receptores)
def gerenciar_pessoas():
    print("\n=== Gerenciamento de Pessoas ===")
    print("1. Listar doadores")
    print("2. Listar receptores")
    print("3. Voltar")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        listar_doadores()
    elif opcao == "2":
        listar_receptores()
    elif opcao == "3":
        return
    else:
        print("Opção inválida!")


# Função para mostrar órgãos e tipos
def mostrar_orgaos_tipos():
    print("\n=== Órgãos e Seus Tipos ===")
    
    try:
        # Carregar os dados do JSON
        dados = carregar_dados_json(r'jsons/orgaos_tipos.json')
        if dados:
            # Verifica se as listas têm o mesmo tamanho
            orgaos = dados.get('orgaos', [])
            tipos = dados.get('tipos_de_orgaos', [])

            if len(orgaos) == len(tipos):
                for orgao, tipo in zip(orgaos, tipos):
                    print(f"- {orgao} ({tipo})")
            else:
                print("Erro: Listas de órgãos e tipos têm tamanhos diferentes.")
        else:
            print("Nenhum dado encontrado no arquivo.")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
    
    input("\nPressione Enter para voltar...")


# Função para gerenciar os centros de distribuição
def gerenciar_centros_distribuicao():
    print("\n=== Centros de Distribuição ===")
    try:
        exibir_estoque_centros()
    except NameError:
        print("Erro: A função 'exibir_estoque_centros' não está definida.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    input("\nPressione Enter para voltar...")
""


def adicionar_doacao():
    print("\n=== Adicionar Doação ===")
    tipo_doacao = input("Tipo de doação: ")
    
    try:
        id_doador = int(input("ID do doador: "))
        id_receptor = int(input("ID do receptor: "))
    except ValueError:
        print("IDs devem ser números inteiros.")
        return

    status = input("Status da doação (Realizada/Pendente/Cancelada): ")

    try:
        # Cria uma nova instância de Doacao e registra automaticamente no dicionário interno
        Doacao(tipo_doacao, id_doador, id_receptor, status)
        print("Doação registrada com sucesso!")
    except ValueError as e:
        print(f"Erro ao registrar doação: {e}")


# Exibir Estoque dos Centros
def exibir_estoque_centros():
    centros = CentroDistribuicao.carregar_centros_de_json(r"jsons\centros_distribuicao.json")
    if centros:
        print("\n=== Estoque Atual dos Centros de Distribuição ===")
        for centro in centros:
            centro.exibir_estoque()
    else:
        print("Nenhum centro carregado.")

# Exibir Histórico de Doações
def exibir_historico_doacoes():
    print("\nHistórico de Doações")
    doacoes = carregar_dados_json(r'jsons\doacoes.json')
    if doacoes:
        for d in doacoes:
            print(f"ID: {d['id']} | Doador: {d['id_doador']} | Receptor: {d['id_receptor']} | Tipo: {d['tipo_doacao']}")
    else:
        print("Nenhuma doação registrada.")

# Listar Doadores
def listar_doadores():
    print("\n--- Lista de Doadores ---")
    doadores = Doador.listar()
    
    if doadores:
        for doador in doadores.values():
            print(f"ID: {doador.id} | Nome: {doador.nome} | CPF: {doador.cpf}")
            
            # Verifica se existe uma intenção de doar
            if doador.intencao_doar:
                print(f"Data de Intenção: {doador.intencao_doar.data_intencao} | Status: {doador.intencao_doar.status}")
            else:
                print("Intenção de doar não encontrada ou incompleta.")
            
            print("-" * 40)
    else:
        print("Nenhum doador cadastrado.")


# Listar Receptores
def listar_receptores():
    print("\n--- Lista de Receptores ---")
    receptores = Receptor.listar()
    
    if receptores:
        for receptor in receptores.values():
            print(f"ID: {receptor.id} | Nome: {receptor.nome} | Órgão Necessário: {receptor.orgao_necessario}")
            print("-" * 40)
    else:
        print("Nenhum receptor cadastrado.")


# Editar Doador
def editar_doador():
    doador_id = int(input("Digite o ID do doador a ser editado: "))
    doador = Doador.buscar(doador_id)
    
    if doador:
        nome = input(f"Nome ({doador.nome}): ") or doador.nome
        doador.editar(nome=nome)
        print("Doador editado com sucesso!")
    else:
        print("Doador não encontrado.")


# Editar Receptor
def editar_receptor():
    receptor_id = int(input("Digite o ID do receptor a ser editado: "))
    receptor = Receptor.buscar(receptor_id)

    if receptor:
        nome = input(f"Nome ({receptor.nome}): ") or receptor.nome
        receptor.editar(nome=nome)
        print("Receptor editado com sucesso!")
    else:
        print("Receptor não encontrado.")


# Buscar Doador
def buscar_doador():
    identificador = input("Digite o ID ou CPF do doador: ")
    if identificador.isdigit():
        identificador = int(identificador)
    doador = Doador.buscar(identificador)
    
    if doador:
        print(f"ID: {doador.id} | Nome: {doador.nome} | CPF: {doador.cpf}")
    else:
        print("Doador não encontrado.")


# Buscar Receptor
def buscar_receptor():
    identificador = input("Digite o ID ou CPF do receptor: ")
    if identificador.isdigit():
        identificador = int(identificador)
    receptor = Receptor.buscar(identificador)
    
    if receptor:
        print(f"ID: {receptor.id} | Nome: {receptor.nome} | Órgão Necessário: {receptor.orgao_necessario}")
    else:
        print("Receptor não encontrado.")


# Menu Principal
def menu_principal():
    while True:
        print("\n𝙱𝚎𝚖 𝚟𝚒𝚗𝚍𝚘 𝚊𝚘 𝚂𝙽𝙳𝙾𝚃 (𝚂𝚒𝚜𝚝𝚎𝚖𝚊 𝙽𝚊𝚌𝚒𝚘𝚗𝚊𝚕 𝚍𝚎 𝚍𝚘𝚊𝚌̧𝚊̃𝚘 𝚍𝚎 𝙾𝚛𝚐𝚊̃𝚘𝚜 𝚎 𝚝𝚎𝚌𝚒𝚍𝚘𝚜)!")
        print('''
              𝟷. Cadastro do Doador
              𝟸. Cadastro do Receptor
              𝟹. Página do Administrador
              𝟺. Adicionar doação
              𝟻. Exibir estoque atual dos Centros de Distribuição
              𝟼. Exibir histórico de doações
              𝟳. Listar doadores
              8. Listar receptores
              9. Editar doador
              10. Editar receptor
              𝟷1. Buscar doador
              𝟷2. Buscar receptor
              13. Finalizar aplicação''')

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastro_doador()
        elif opcao == "2":
            cadastro_receptor()
        elif opcao == "3":
            submenu_administrador()
        elif opcao == "4":
            adicionar_doacao()
        elif opcao == "5":
            exibir_estoque_centros()
        elif opcao == "6":
            exibir_historico_doacoes()  
        elif opcao == "7":
            listar_doadores()  
        elif opcao == "8":
            listar_receptores()
        elif opcao == "9":
            editar_doador()
        elif opcao == "10":
            editar_receptor()
        elif opcao == "11":
            buscar_doador()
        elif opcao == "12":
            buscar_receptor()
        elif opcao == "13":
            print("Finalizando aplicação...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Submenu do Administrador
def submenu_administrador():
    while True:
        print("\n=== 𝙼𝚎𝚗𝚞 𝚍𝚘 𝙰𝚍𝚖𝚒𝚗𝚒𝚜𝚝𝚛𝚊𝚍𝚘𝚛 ===")
        print('''
              1. Login
              2. Logout
              3. Recuperar Senha
              4. Cadastrar Administrador
              5. Gerenciar Pessoas
              6. Ver Órgãos/Tipos
              7. Gerenciar Centros
              8. Voltar''')
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            login_administrador()
        elif opcao == "2":
            logout_administrador()
        elif opcao == "3":
            recuperar_senha()
        elif opcao == "4":
            cadastro_administrador()
        elif opcao == "5":
            gerenciar_pessoas()
        elif opcao == "6":
            mostrar_orgaos_tipos()
        elif opcao == "7":
            gerenciar_centros_distribuicao()
        elif opcao == "8":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
