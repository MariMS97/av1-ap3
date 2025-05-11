
import json
import os
from utils import gerar_id_simples
from classes.Doador import Doador
from classes.Receptor import Receptor
from classes.AdministradorSistema import AdministradorSistema
from classes.Doacao import Doacao
from classes.CentroDistribuicao import CentroDistribuicao
from classes.IntencaoDoar import IntencaoDoar
from utils import carregar_dados_json  


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
    
    # Geração de ID único para o doador
    id_gerado = int(gerar_id_simples(r"jsons\potenciais_doadores.json")) 

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
        intencao_doar=intencao
    )

    # Cadastra no dicionário da classe
    try:
        doador.cadastrar()
        print("Doador cadastrado com sucesso!")
    except ValueError as e:
        print(f"Erro ao cadastrar doador: {e}")
        return

    # Atualiza o arquivo JSON no formato correto
    doadores = carregar_dados_json(r'jsons\potenciais_doadores.json')
    doadores.append({
        "dados": doador.to_dict(),
        "intencao": intencao.to_dict()
    })
    salvar_dados_json(r'jsons\potenciais_doadores.json', doadores)

# Função para cadastrar um novo receptor
def cadastro_receptor():
    print("\nCadastro de Receptor")
    
    # Caminho do arquivo JSON
    caminho_arquivo = r'jsons\receptores.json'
    
    # Dados pessoais
    id_receptor = int(gerar_id_simples(caminho_arquivo)) 
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

    # Instanciando o objeto Receptor
    novo_receptor = Receptor(
        id=id_receptor,
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
        centro_transplante_vinculado=centro_transplante,
        contato_emergencia=contato_emergencia,
        posicao_lista_espera=posicao_lista_espera
    )

    try:
        # Chamando o método cadastrar do objeto
        novo_receptor.cadastrar()
        print("Receptor cadastrado com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as e:
        print(f"Erro ao cadastrar receptor: {e}")



# Função para cadastrar um novo administrador
def cadastro_administrador():
    """Função para cadastrar um novo administrador no sistema."""
    administradores = carregar_dados_json(r'jsons\admins.json')
    
    try:
        print("\n--- Cadastro de Administrador ---")
        
        # Gerando um ID único para o novo administrador
        novo_id = gerar_id_simples(r'jsons\admins.json')

        # Entrando com os dados de acesso
        nome_usuario = input("Nome de usuário: ").strip()
        
        # Verifica se o nome de usuário já está em uso
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

        # Salva os dados no JSON
        salvar_dados_json(r'jsons\admins.json', administradores)

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
    
    administradores = carregar_dados_json(r'jsons\admins.json')
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
        dados = carregar_dados_json(r'jsons\orgãos_tipos.json')
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

def adicionar_doacao():
    print("\nAdicionar Doação")
    tipo_doacao = input("Tipo de doação: ")
    id_doador = int(input("ID do doador: "))  # Convertendo para inteiro
    id_receptor = int(input("ID do receptor: "))  # Convertendo para inteiro
    status = input("Status da doação (Realizada/Pendente/Cancelada): ")

    doacao = Doacao(tipo_doacao, id_doador, id_receptor)
    doacoes = carregar_dados_json(r'jsons\doacoes.json')
    doacoes.append(doacao.to_dict())

    salvar_dados_json(r'jsons\doacoes.json', doacoes)
    print("Doação registrada com sucesso!")

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
    print("\nLista de Doadores")
    doadores = carregar_dados_json(r'jsons\potenciais_doadores.json')
    
    if doadores:
        for doador in doadores:
            dados = doador.get("dados", {})
            print(f"ID: {dados.get('id')} | Nome: {dados.get('nome')} | CPF: {dados.get('cpf')}")

            # Verifica se existe uma intenção de doar
            intencao = doador.get("intencao", {})
            if "data_intencao" in intencao and "status" in intencao:
                print(f"Data de Intenção: {intencao['data_intencao']} | Status: {intencao['status']}")
            else:
                print("Intenção de doar não encontrada ou incompleta.")
                
            print("-" * 40)
    else:
        print("Nenhum doador cadastrado.")



# Listar Receptores
def listar_receptores():
    print("\nLista de Receptores")
    receptores = carregar_dados_json(r'jsons\receptores.json')
    if receptores:
        for receptor in receptores:
            dados = receptor["dados"]
            print(f"ID: {dados['id']} | Nome: {dados['nome']} | Órgão Necessário: {receptor['necessidade']['orgao_necessario']}")
    else:
        print("Nenhum receptor cadastrado.")

# Editar Doador
def editar_doador():
    doador_id = int(input("Digite o ID do doador a ser editado: "))
    doadores = carregar_dados_json(r'jsons\potenciais_doadores.json')
    doador = next((d for d in doadores if d["dados"]["id"] == doador_id), None)
    if doador:
        nome = input(f"Nome ({doador['dados']['nome']}): ") or doador['dados']['nome']
        doador['dados']['nome'] = nome
        salvar_dados_json(r'jsons\potenciais_doadores.json', doadores)
        print("Doador editado com sucesso!")
    else:
        print("Doador não encontrado.")

# Editar Receptor
def editar_receptor():
    receptor_id = int(input("Digite o ID do receptor a ser editado: "))
    receptores = carregar_dados_json(r'jsons\receptores.json')
    receptor = next((r for r in receptores if r["id"] == receptor_id), None)
    if receptor:
        nome = input(f"Nome ({receptor['dados']['nome']}): ") or receptor['dados']['nome']
        receptor['dados']['nome'] = nome
        salvar_dados_json(r'jsons\receptores.json', receptores)
        print("Receptor editado com sucesso!")
    else:
        print("Receptor não encontrado.")

# Buscar Doador
def buscar_doador():
    doador_id = input("Digite o ID ou CPF do doador: ")
    doadores = carregar_dados_json(r'jsons\potenciais_doadores.json')
    doador = next((d for d in doadores if str(d['dados']['id']) == doador_id or d['dados']['cpf'] == doador_id), None)
    if doador:
        print(f"ID: {doador['dados']['id']} | Nome: {doador['dados']['nome']} | CPF: {doador['dados']['cpf']}")
    else:
        print("Doador não encontrado.")

# Buscar Receptor
def buscar_receptor():
    receptor_id = input("Digite o ID ou CPF do receptor: ")
    receptores = carregar_dados_json(r'jsons\receptores.json')
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
