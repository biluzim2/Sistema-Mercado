from models.cliente import Cliente
from views.menu_view import MenuView


class ClienteController:

    def __init__(self):
        self.model = Cliente()
        self.view = MenuView()

    def cadastrar(self):
        nome, cpf, endereco = self.view.cadastrar_cliente()

        if not nome.strip() or not cpf.strip():
            self.view.mensagem("Nome e CPF são obrigatórios.")
            return

        resultado = self.model.cadastrar(nome, cpf, endereco)

        if resultado:
            self.view.mensagem("Cliente cadastrado com sucesso!")
        else:
            self.view.mensagem("Não foi possível cadastrar o cliente.")
