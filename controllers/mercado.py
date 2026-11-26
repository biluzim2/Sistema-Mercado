
from models.mercado import MercadoModel


class MercadoController:

    CAMPOS = {
        "Categorias": ["nome"],

        "Produtos": [
            "nome",
            "codigo",
            "preco",
            "estoque",
            "id_categoria"
        ],

        "Clientes": [
            "nome",
            "cpf",
            "endereco"
        ],

        "Vendedores": [
            "nome",
            "cpf",
            "endereco"
        ]
    }

    def __init__(self):
        self.model = MercadoModel()

    def listar(self, modulo):
        return self.model.listar(modulo)

    def salvar(self, modulo, valores, identificador=None):

        campos = self.CAMPOS[modulo]

        if len(valores) != len(campos):
            return False, "Quantidade de campos inválida."

        dados = dict(zip(campos, valores))

        for campo in campos:

            if campo in ["nome", "codigo", "cpf"]:

                if not str(dados[campo]).strip():
                    return False, f"Preencha o campo {campo}."

        if modulo == "Produtos":

            try:
                dados["preco"] = float(
                    str(dados["preco"]).replace(",", ".")
                )

                dados["estoque"] = int(dados["estoque"])
                dados["id_categoria"] = int(dados["id_categoria"])

                if dados["preco"] <= 0:
                    return False, "O preço deve ser maior que zero."

                if dados["estoque"] < 0:
                    return False, "O estoque não pode ser negativo."

            except ValueError:
                return False, "Verifique preço, estoque e categoria."

        return self.model.salvar(
            modulo,
            dados,
            identificador
        )

    def excluir(self, modulo, identificador):

        try:
            identificador = int(identificador)

        except ValueError:
            return False, "Selecione um registro válido."

        return self.model.excluir(
            modulo,
            identificador
        )

    def dashboard(self):
        return self.model.dashboard()

    def registrar_venda(
        self,
        id_cliente,
        id_vendedor,
        id_produto,
        quantidade
    ):

        try:
            return self.model.registrar_venda(
                id_cliente,
                id_vendedor,
                id_produto,
                quantidade
            )

        except ValueError:
            return False, "Verifique os IDs e a quantidade."
