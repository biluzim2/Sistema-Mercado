
from database.conexao import conectar


class Vendedor:

    def cadastrar(self, nome, cpf, endereco):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO vendedor (nome, cpf, endereco)
                VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (nome, cpf, endereco))
            conexao.commit()
            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar vendedor:", erro)
            return False

        finally:
            cursor.close()
            conexao.close()

    def listar(self):
        conexao = conectar()

        if conexao is None:
            return []

        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM vendedor ORDER BY nome")
            return cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()
