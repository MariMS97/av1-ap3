import json
from datetime import datetime

def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

class Doacao:
    doacoes = {}

    def __init__(self, tipo_doacao: str, id_doador: int, id_receptor: int, status: str):
        self.tipo_doacao = tipo_doacao
        self.id_doador = id_doador
        self.id_receptor = id_receptor
        self.data_doacao = datetime.now().strftime("%d/%m/%Y")
        self.status = status

        # Carregar e adaptar os dados dos JSONs
        self.doador_data = {
            str(d["dados"]["id"]): {
                "nome": d["dados"].get("nome", ""),
                "tipo_sanguineo": d["dados"].get("tipo_sanguineo", ""),
                "orgaos_disponiveis": d.get("intencao", {}).get("orgaos_id", []),
                "intencao_doacao": d.get("intencao", {}).get("status", "") == "Confirmada"
            }
            for d in carregar_json("jsons/potenciais_doadores.json")
        }

        data = carregar_json("jsons/receptores.json")  # data será um dict ou lista

        # Se for lista, cria dicionário por id; se for dict único, adapta
        if isinstance(data, list):
            self.receptor_data = {
                str(r["dados"]["id"]): r["dados"] for r in data
            }
        else:
            self.receptor_data = {
                str(data["dados"]["id"]): data["dados"]
            }

        # Definir doador e receptor com base nos ids fornecidos
        self.doador = self.doador_data.get(str(self.id_doador))
        self.receptor = self.receptor_data.get(str(self.id_receptor))

        if not self.doador or not self.receptor:
            raise ValueError("Doador ou receptor não encontrado.")

        # Inicia validação com chain of responsibility interno
        if self.validar_doacao():
            self.registrar_doacao()

    @property
    def data_doacao(self):
        return self.__data_doacao

    @data_doacao.setter
    def data_doacao(self, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            self.__data_doacao = valor
        except ValueError:
            raise ValueError("Data da doação inválida.")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in ['Realizada', 'Pendente', 'Cancelada']:
            raise ValueError("Status inválido.")
        self.__status = valor

    # ----------------------------------------
    # Chain of Responsibility 
    # ----------------------------------------
    class HandlerBase:
        def __init__(self):
            self._proximo = None

        def set_proximo(self, proximo):
            self._proximo = proximo
            return proximo

        def handle(self, doador, receptor):
            if self._proximo:
                return self._proximo.handle(doador, receptor)
            return True

    class CompatibilidadeSanguineaHandler(HandlerBase):
        def handle(self, doador, receptor):
            compatibilidade = {
                "O-": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                "O+": ["A+", "B+", "AB+", "O+"],
                "A-": ["A+", "A-", "AB+", "AB-"],
                "A+": ["A+", "AB+"],
                "B-": ["B+", "B-", "AB+", "AB-"],
                "B+": ["B+", "AB+"],
                "AB-": ["AB+", "AB-"],
                "AB+": ["AB+"]
            }
            if receptor["tipo_sanguineo"] in compatibilidade.get(doador["tipo_sanguineo"], []):
                print("Compatibilidade sanguínea verificada: Compatível.")
                return super().handle(doador, receptor)
            print("Compatibilidade sanguínea verificada: Incompatível.")
            return False

    class OrgaoNecessarioHandler(HandlerBase):
        def handle(self, doador, receptor):
            if receptor.get("orgao_necessario") in doador.get("orgaos_disponiveis", []):
                print("Órgão necessário verificado: Compatível.")
                return super().handle(doador, receptor)
            print("Órgão necessário verificado: Incompatível.")
            return False

    class IntencaoDoacaoHandler(HandlerBase):
        def handle(self, doador, receptor):
            if doador.get("intencao_doacao"):
                print("Intenção de doação verificada: Positiva.")
                return super().handle(doador, receptor)
            print("Intenção de doação verificada: Negativa.")
            return False

    class PrioridadeListaHandler(HandlerBase):
        def handle(self, doador, receptor):
            gravidade = receptor.get("gravidade_condicao", "Baixa")
            if gravidade.lower() == "grave" or gravidade.lower() == "alta":
                print("Gravidade da condição verificada: Alta prioridade.")
            else:
                print(f"Gravidade da condição verificada: Prioridade {gravidade}.")
            return super().handle(doador, receptor)

    def validar_doacao(self):
        compat = self.CompatibilidadeSanguineaHandler()
        orgao = compat.set_proximo(self.OrgaoNecessarioHandler())
        intencao = orgao.set_proximo(self.IntencaoDoacaoHandler())
        prioridade = intencao.set_proximo(self.PrioridadeListaHandler())

        return compat.handle(self.doador, self.receptor)

    def registrar_doacao(self):
        chave = f"{self.id_doador}-{self.id_receptor}"
        Doacao.doacoes[chave] = {
            "tipo_doacao": self.tipo_doacao,
            "data_doacao": self.data_doacao,
            "status": self.status
        }
        print(f"Doação registrada com sucesso: {chave}")

    @classmethod
    def listar_doacoes(cls):
        for chave, dados in cls.doacoes.items():
            print(f"ID: {chave} | Tipo: {dados['tipo_doacao']} | Data: {dados['data_doacao']} | Status: {dados['status']}")
