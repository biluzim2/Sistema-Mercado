
from database.conexao import conectar


class Produto:

    def cadastrar(self, nome, codigo, preco, estoque, categoria_id):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO produto
                (nome, codigo, preco, estoque, id_categoria)
                VALUES (%s, %s, %s, %s, %s)
            """

            valores = (nome, codigo, preco, estoque, categoria_id)

            cursor.execute(sql, valores)
            conexao.commit()

            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar produto:", erro)
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
            sql = """
                SELECT
                    produto.id_produto,
                    produto.nome,
                    produto.codigo,
                    produto.preco,
                    produto.estoque,
                    categoria.nome AS categoria
                FROM produto
                LEFT JOIN categoria
                    ON produto.id_categoria = categoria.id_categoria
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print("Erro ao listar produtos:", erro)
            return []

        finally:
            cursor.close()
            conexao.close()

    def buscar(self, codigo):
        conexao = conectar()

        if conexao is None:
            return None

        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM produto WHERE codigo = %s",
                (codigo,)
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

    def atualizar(self, id_produto, nome, codigo, preco, estoque, categoria_id):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE produto
                SET nome = %s,
                    codigo = %s,
                    preco = %s,
                    estoque = %s,
                    id_categoria = %s
                WHERE id_produto = %s
            """

            valores = (
                nome, codigo, preco, estoque,
                categoria_id, id_produto
            )

            cursor.execute(sql, valores)
            conexao.commit()

            return cursor.rowcount > 0

        except Exception as erro:
            conexao.rollback()
            print("Erro ao atualizar produto:", erro)
            return False

        finally:
            cursor.close()
            conexao.close()

    def excluir(self, id_produto):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor()

        try:
            cursor.execute(
                "DELETE FROM produto WHERE id_produto = %s",
                (id_produto,)
            )

            conexao.commit()

            return cursor.rowcount > 0

        except Exception as erro:
            conexao.rollback()
            print("Erro ao excluir produto:", erro)
            return False

        finally:
            cursor.close()
            conexao.close()
