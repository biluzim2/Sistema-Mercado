from models.vendedor import Vendedor
from views.menu_view import MenuView


class VendedorController:

    def __init__(self):
        self.model = Vendedor()
        self.view = MenuView()

    def cadastrar(self):
        nome, cpf, endereco = self.view.cadastrar_vendedor()

        if not nome.strip() or not cpf.strip():
            self.view.mensagem("Nome e CPF são obrigatórios.")
            return

        resultado = self.model.cadastrar(nome, cpf, endereco)

        if resultado:
            self.view.mensagem("Vendedor cadastrado com sucesso!")
        else:
            self.view.mensagem("Não foi possível cadastrar o vendedor.")
