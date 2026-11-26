from controllers.mercado import MercadoController
from views.menu_view import MenuView


def main():

    controller = MercadoController()

    view = MenuView(controller)

    view.iniciar()


if __name__ == "__main__":
    main()
