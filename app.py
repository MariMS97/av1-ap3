
import json
from utils import gerar_id_simples
from Doador import Doador
from Receptor import Receptor
from AdministradorSistema import AdministradorSistema
from Doacao import Doacao
from CentroDistribuicao import CentroDistribuicao


# Função para carregar dados JSON
def carregar_dados_json(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Função para salvar dados JSON
def salvar_dados_json(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Cadastro de Doador
def cadastro_doador():
    print("\nCadastro de Doador")
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
    id_gerado = gerar_id_simples("potenciais_doadores.json") 

    doador_dict = {
        "dados": {
            "id": id_gerado,
            "nome": nome,
            "idade": idade,
            "sexo": genero,
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
        },
        "intencao": {
            "status": "s",
            "orgaos_id": []
        }
    }

    doadores = carregar_dados_json('potenciais_doadores.json')
    doadores.append(doador_dict)
    salvar_dados_json('potenciais_doadores.json', doadores)
    print("Doador cadastrado com sucesso!")

# Cadastro de Receptor
def cadastro_receptor():
    print("\nCadastro de Receptor")

    # Dados pessoais
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    genero = input("Gênero (M/F/O): ")
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    cidade_natal = input("Cidade natal: ")
    estado_natal = input("Estado natal: ")
    cpf = input("CPF: ")
    profissao = input("Profissão: ")
    cidade_residencia = input("Cidade de residência: ")
    estado_residencia = input("Estado de residência: ")
    estado_civil = input("Estado civil: ")
    contato_emergencia = input("Contato de emergência: ")

    # Necessidades médicas
    orgao_necessario = input("Órgão necessário: ")
    gravidade_condicao = input("Gravidade da condição (Leve/Moderada/Grave/Gravíssima): ")
    centro_transplante = input("Centro de transplante vinculado: ")
    posicao_lista_espera = input("Posição na lista de espera: ")

    receptores = carregar_dados_json('receptores.json')
    id_receptor = gerar_id_simples("receptores.json")

    novo_receptor = {
        "id": id_receptor,
        "dados": {
            "id": id_receptor,
            "nome": nome,
            "idade": idade,
            "sexo": genero,
            "data_nascimento": data_nascimento,
            "cidade_natal": cidade_natal,
            "estado_natal": estado_natal,
            "cpf": cpf,
            "profissao": profissao,
            "cidade_residencia": cidade_residencia,
            "estado_residencia": estado_residencia,
            "estado_civil": estado_civil,
            "contato_emergencia": contato_emergencia,
        },
        "necessidade": {
            "orgao_necessario": orgao_necessario,
            "gravidade_condicao": gravidade_condicao,
            "centro_transplante": centro_transplante,
            "posicao_lista_espera": posicao_lista_espera
        }
    }

    receptores.append(novo_receptor)
    salvar_dados_json('receptores.json', receptores)

    print("Receptor cadastrado com sucesso!")

# Função para cadastrar um novo administrador
def cadastro_administrador():
    administradores = carregar_dados_json('admins.json')
    try:
        print("\n--- Cadastro de Administrador ---")
        
        # Gerando um ID único para o novo administrador
        novo_id = gerar_id_simples('admins.json')

        # Entrando com os dados de acesso
        nome_usuario = input("Nome de usuário: ").strip()
        
        # Verifica se o nome de usuário já está em uso
        administradores = AdministradorSistema.carregar_dados()
        if any(admin["acesso"]["nome_usuario"] == nome_usuario for admin in administradores):
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

        # Chama o método de cadastro do administrador
        resultado = admin.cadastrar()

        salvar_dados_json('admins.json', administradores)
       

        # Exibe mensagem de sucesso
        print(f"\n{resultado}")

    except ValueError as ve:
        print(f"\n[Erro de Validação] {ve}")
    except Exception as e:
        print(f"\n[Erro Inesperado] {str(e)}")

# Função para login do administrador
def login_administrador():
    nome_usuario = input("Digite o nome de usuário: ").strip()
    senha = input("Digite a senha: ").strip()
    
    administradores = carregar_dados_json('admins.json')
    for admin in administradores:
        if admin['acesso']['nome_usuario'] == nome_usuario and admin['acesso']['senha'] == senha:
            print("Login bem-sucedido!")
            return True
    print("Credenciais inválidas!")
    return False

# Função para logout do administrador
def logout_administrador():
    print("Logout realizado com sucesso!")
    return True

# Função para recuperar senha
def recuperar_senha():
    email = input("Digite o email cadastrado: ")
    print(f"Instruções para redefinição enviadas para {email}")
    return True

#função para gerenciar pessoas (doadores e receptores)
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

#Função para mostrar órgãos e tipos
def mostrar_orgaos_tipos():
    print("\n=== Órgãos e Seus Tipos ===")
    
    try:
        dados = carregar_dados_json('orgãos_tipos.json')
        if dados:
            # Verifica se as listas têm o mesmo tamanho
            if len(dados['orgaos']) == len(dados['tipos_de_orgaos']):
                for i in range(len(dados['orgaos'])):
                    print(f"- {dados['orgaos'][i]} ({dados['tipos_de_orgaos'][i]})")
            else:
                print("Erro: Listas de órgãos e tipos têm tamanhos diferentes.")
        else:
            print("Nenhum dado encontrado no arquivo.")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
    
    input("\nPressione Enter para voltar...")

#Função para gerenciar os centros de distribuição
def gerenciar_centros_distribuicao():
    print("\n=== Centros de Distribuição ===")
    exibir_estoque_centros()
    input("\nPressione Enter para voltar...")

# Adicionar Doação
def adicionar_doacao():
    print("\nAdicionar Doação")
    tipo_doacao = input("Tipo de doação: ")
    id_doador = input("ID do doador: ")
    id_receptor = input("ID do receptor: ")

    doacao = Doacao(tipo_doacao, id_doador, id_receptor)
    doacoes = carregar_dados_json('doacoes.json')
    doacoes.append(doacao.to_dict())

    salvar_dados_json('doacoes.json', doacoes)
    print("Doação registrada com sucesso!")

# Exibir Estoque dos Centros
def exibir_estoque_centros():
    centros = CentroDistribuicao.carregar_centros_de_json("centros_distribuicao.json")
    if centros:
        print("\n=== Estoque Atual dos Centros de Distribuição ===")
        for centro in centros:
            centro.exibir_estoque()
    else:
        print("Nenhum centro carregado.")

# Exibir Histórico de Doações
def exibir_historico_doacoes():
    print("\nHistórico de Doações")
    doacoes = carregar_dados_json('doacoes.json')
    if doacoes:
        for d in doacoes:
            print(f"ID: {d['id']} | Doador: {d['id_doador']} | Receptor: {d['id_receptor']} | Tipo: {d['tipo_doacao']}")
    else:
        print("Nenhuma doação registrada.")

# Listar Doadores
def listar_doadores():
    print("\nLista de Doadores")
    doadores = carregar_dados_json('potenciais_doadores.json')
    if doadores:
        for doador in doadores:
            dados = doador["dados"]
            print(f"ID: {dados['id']} | Nome: {dados['nome']} | CPF: {dados['cpf']}")
    else:
        print("Nenhum doador cadastrado.")

# Listar Receptores
def listar_receptores():
    print("\nLista de Receptores")
    receptores = carregar_dados_json('receptores.json')
    if receptores:
        for receptor in receptores:
            dados = receptor["dados"]
            print(f"ID: {dados['id']} | Nome: {dados['nome']} | Órgão Necessário: {receptor['necessidade']['orgao_necessario']}")
    else:
        print("Nenhum receptor cadastrado.")

# Editar Doador
def editar_doador():
    doador_id = int(input("Digite o ID do doador a ser editado: "))
    doadores = carregar_dados_json('potenciais_doadores.json')
    doador = next((d for d in doadores if d["dados"]["id"] == doador_id), None)
    if doador:
        nome = input(f"Nome ({doador['dados']['nome']}): ") or doador['dados']['nome']
        doador['dados']['nome'] = nome
        salvar_dados_json('potenciais_doadores.json', doadores)
        print("Doador editado com sucesso!")
    else:
        print("Doador não encontrado.")

# Editar Receptor
def editar_receptor():
    receptor_id = int(input("Digite o ID do receptor a ser editado: "))
    receptores = carregar_dados_json('receptores.json')
    receptor = next((r for r in receptores if r["id"] == receptor_id), None)
    if receptor:
        nome = input(f"Nome ({receptor['dados']['nome']}): ") or receptor['dados']['nome']
        receptor['dados']['nome'] = nome
        salvar_dados_json('receptores.json', receptores)
        print("Receptor editado com sucesso!")
    else:
        print("Receptor não encontrado.")

# Buscar Doador
def buscar_doador():
    doador_id = input("Digite o ID ou CPF do doador: ")
    doadores = carregar_dados_json('potenciais_doadores.json')
    doador = next((d for d in doadores if str(d['dados']['id']) == doador_id or d['dados']['cpf'] == doador_id), None)
    if doador:
        print(f"ID: {doador['dados']['id']} | Nome: {doador['dados']['nome']} | CPF: {doador['dados']['cpf']}")
    else:
        print("Doador não encontrado.")

# Buscar Receptor
def buscar_receptor():
    receptor_id = input("Digite o ID ou CPF do receptor: ")
    receptores = carregar_dados_json('receptores.json')
    receptor = next((r for r in receptores if str(r['dados']['id']) == receptor_id or r['dados']['cpf'] == receptor_id), None)
    if receptor:
        print(f"ID: {receptor['dados']['id']} | Nome: {receptor['dados']['nome']} | Órgão Necessário: {receptor['necessidade']['orgao_necessario']}")
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
