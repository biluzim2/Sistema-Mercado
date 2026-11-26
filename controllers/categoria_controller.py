from models.categoria import Categoria
from views.menu_view import MenuView


class CategoriaController:

    def __init__(self):
        self.model = Categoria()
        self.view = MenuView()

    def cadastrar(self):
        nome = self.view.cadastrar_categoria()

        if not nome.strip():
            self.view.mensagem("Informe o nome da categoria.")
            return

        resultado = self.model.cadastrar(nome)

        if resultado:
            self.view.mensagem("Categoria cadastrada com sucesso!")
        else:
            self.view.mensagem("Não foi possível cadastrar.")
