
from database.conexao import conectar


class Venda:

    def registrar(self, cliente_id, vendedor_id, itens, forma_pagamento):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor(dictionary=True)

        try:
            total = 0

           
            for item in itens:
                cursor.execute(
                    "SELECT * FROM produto WHERE id = %s FOR UPDATE",
                    (item["produto_id"],)
                )

                produto = cursor.fetchone()

                if produto is None:
                    raise Exception("Produto não encontrado.")

                if produto["estoque"] < item["quantidade"]:
                    raise Exception(
                        f"Estoque insuficiente para {produto['nome']}."
                    )

                item["preco"] = float(produto["preco"])
                total += item["preco"] * item["quantidade"]

            
            cursor.execute(
                """
                INSERT INTO venda
                (cliente_id, vendedor_id, total, forma_pagamento)
                VALUES (%s, %s, %s, %s)
                """,
                (cliente_id, vendedor_id, total, forma_pagamento)
            )

            venda_id = cursor.lastrowid

           
            for item in itens:
                cursor.execute(
                    """
                    INSERT INTO item_venda
                    (venda_id, produto_id, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        venda_id,
                        item["produto_id"],
                        item["quantidade"],
                        item["preco"]
                    )
                )

                cursor.execute(
                    """
                    UPDATE produto
                    SET estoque = estoque - %s
                    WHERE id = %s
                    """,
                    (item["quantidade"], item["produto_id"])
                )

            conexao.commit()
            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao registrar venda:", erro)
            return False

        finally:
            cursor.close()
            conexao.close()
