from models.produto import Produto


class ProdutoController:

    def __init__(self):
        self.model = Produto()

    def listar(self):
        return self.model.listar()

    def cadastrar(self, nome, codigo, preco, estoque, categoria_id):

        try:
            preco = float(preco.replace(",", "."))
            estoque = int(estoque)
            categoria_id = int(categoria_id)

            if not nome.strip() or not codigo.strip():
                return False, "Preencha todos os campos."

            if preco <= 0 or estoque < 0:
                return False, "Preço ou estoque inválido."

        except ValueError:
            return False, "Verifique os valores informados."

        resultado = self.model.cadastrar(
            nome, codigo, preco, estoque, categoria_id
        )

        if resultado:
            return True, "Produto cadastrado com sucesso!"

        return False, "Não foi possível cadastrar o produto."

    def excluir(self, id_produto):

        try:
            id_produto = int(id_produto)
        except ValueError:
            return False, "ID inválido."

        resultado = self.model.excluir(id_produto)

        if resultado:
            return True, "Produto excluído com sucesso!"

        return False, "Não foi possível excluir o produto."
