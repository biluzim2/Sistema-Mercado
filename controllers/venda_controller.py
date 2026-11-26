
from models.venda import Venda
from views.menu_view import MenuView


class VendaController:

    def __init__(self):
        self.model = Venda()
        self.view = MenuView()

    def registrar(self):
        cliente_id, vendedor_id, itens, forma = (
            self.view.realizar_venda()
        )

        formas = {
            "1": "Cartão de crédito",
            "2": "Cartão de débito",
            "3": "Dinheiro",
            "4": "Pix"
        }

        try:
            cliente_id = int(cliente_id)
            vendedor_id = int(vendedor_id)

            if not itens:
                raise ValueError("Nenhum produto informado.")

            for item in itens:
                item["produto_id"] = int(item["produto_id"])
                item["quantidade"] = int(item["quantidade"])

                if item["quantidade"] <= 0:
                    raise ValueError("Quantidade inválida.")

            if forma not in formas:
                raise ValueError("Forma de pagamento inválida.")

        except ValueError as erro:
            self.view.mensagem(f"Dados inválidos: {erro}")
            return

        resultado = self.model.registrar(
            cliente_id,
            vendedor_id,
            itens,
            formas[forma]
        )

        if resultado:
            self.view.mensagem("Venda realizada com sucesso!")
        else:
            self.view.mensagem("Não foi possível realizar a venda.")
