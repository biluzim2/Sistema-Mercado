
from database.conexao import conectar


class MercadoModel:

    CONFIG = {
        "Categorias": {
            "table": "categoria",
            "pk": "id_categoria",
            "fields": ["nome"],
            "select": """
                SELECT id_categoria, nome
                FROM categoria
                ORDER BY id_categoria DESC
            """
        },

        "Produtos": {
            "table": "produto",
            "pk": "id_produto",
            "fields": [
                "nome", "codigo", "preco",
                "estoque", "id_categoria"
            ],
            "select": """
                SELECT
                    p.id_produto,
                    p.nome,
                    p.codigo,
                    p.preco,
                    p.estoque,
                    p.id_categoria,
                    COALESCE(c.nome, 'Sem categoria') AS categoria
                FROM produto p
                LEFT JOIN categoria c
                    ON c.id_categoria = p.id_categoria
                ORDER BY p.id_produto DESC
            """
        },

        "Clientes": {
            "table": "cliente",
            "pk": "id_cliente",
            "fields": ["nome", "cpf", "endereco"],
            "select": """
                SELECT id_cliente, nome, cpf, endereco
                FROM cliente
                ORDER BY id_cliente DESC
            """
        },

        "Vendedores": {
            "table": "vendedor",
            "pk": "id_vendedor",
            "fields": ["nome", "cpf", "endereco"],
            "select": """
                SELECT id_vendedor, nome, cpf, endereco
                FROM vendedor
                ORDER BY id_vendedor DESC
            """
        }
    }

    def listar(self, modulo):

        if modulo == "Vendas":
            return self.listar_vendas()

        config = self.CONFIG[modulo]

        conexao = conectar()

        if conexao is None:
            return []

        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(config["select"])
            return cursor.fetchall()

        except Exception as erro:
            print("Erro ao listar:", erro)
            return []

        finally:
            cursor.close()
            conexao.close()

    def salvar(self, modulo, dados, identificador=None):

        config = self.CONFIG[modulo]

        tabela = config["table"]
        pk = config["pk"]
        campos = config["fields"]

        conexao = conectar()

        if conexao is None:
            return False, "Erro ao conectar ao banco."

        cursor = conexao.cursor()

        try:
            valores = [dados[campo] for campo in campos]

            if identificador:

                atribuicoes = ", ".join(
                    f"{campo} = %s" for campo in campos
                )

                sql = f"""
                    UPDATE {tabela}
                    SET {atribuicoes}
                    WHERE {pk} = %s
                """

                cursor.execute(
                    sql,
                    valores + [identificador]
                )

                conexao.commit()

                return True, "Registro atualizado com sucesso!"

            else:

                colunas = ", ".join(campos)
                marcadores = ", ".join(["%s"] * len(campos))

                sql = f"""
                    INSERT INTO {tabela}
                    ({colunas})
                    VALUES ({marcadores})
                """

                cursor.execute(sql, valores)
                conexao.commit()

                return True, "Registro cadastrado com sucesso!"

        except Exception as erro:
            conexao.rollback()
            print("Erro ao salvar:", erro)

            return False, f"Erro ao salvar: {erro}"

        finally:
            cursor.close()
            conexao.close()

    def excluir(self, modulo, identificador):

        config = self.CONFIG[modulo]

        conexao = conectar()

        if conexao is None:
            return False, "Erro ao conectar ao banco."

        cursor = conexao.cursor()

        try:
            sql = f"""
                DELETE FROM {config["table"]}
                WHERE {config["pk"]} = %s
            """

            cursor.execute(sql, (identificador,))
            conexao.commit()

            if cursor.rowcount > 0:
                return True, "Registro excluído com sucesso!"

            return False, "Registro não encontrado."

        except Exception as erro:
            conexao.rollback()
            print("Erro ao excluir:", erro)

            return False, (
                "Não foi possível excluir. "
                "Verifique se existem registros relacionados."
            )

        finally:
            cursor.close()
            conexao.close()

    def listar_vendas(self):

        conexao = conectar()

        if conexao is None:
            return []

        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    v.id_venda,
                    v.data_venda,
                    v.total,
                    c.nome AS cliente,
                    COALESCE(
                        ve.nome,
                        'Não informado'
                    ) AS vendedor
                FROM vendas v
                INNER JOIN cliente c
                    ON c.id_cliente = v.id_cliente
                LEFT JOIN vendedor ve
                    ON ve.id_vendedor = v.id_vendedor
                ORDER BY v.id_venda DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print("Erro ao listar vendas:", erro)
            return []

        finally:
            cursor.close()
            conexao.close()

    def registrar_venda(
        self,
        id_cliente,
        id_vendedor,
        id_produto,
        quantidade
    ):

        conexao = conectar()

        if conexao is None:
            return False, "Erro ao conectar ao banco."

        cursor = conexao.cursor(dictionary=True)

        try:
            id_cliente = int(id_cliente)
            id_produto = int(id_produto)
            quantidade = int(quantidade)

            if str(id_vendedor).strip():
                id_vendedor = int(id_vendedor)
            else:
                id_vendedor = None

            if quantidade <= 0:
                return False, "A quantidade deve ser maior que zero."

            # Verifica o produto e o estoque
            cursor.execute(
                """
                SELECT preco, estoque
                FROM produto
                WHERE id_produto = %s
                FOR UPDATE
                """,
                (id_produto,)
            )

            produto = cursor.fetchone()

            if produto is None:
                return False, "Produto não encontrado."

            if produto["estoque"] < quantidade:
                return False, "Estoque insuficiente."

            preco = produto["preco"]
            total = preco * quantidade

            # Cria a venda
            cursor.execute(
                """
                INSERT INTO vendas
                (id_cliente, id_vendedor, total)
                VALUES (%s, %s, %s)
                """,
                (id_cliente, id_vendedor, total)
            )

            id_venda = cursor.lastrowid

            # Registra o item vendido
            cursor.execute(
                """
                INSERT INTO item_venda
                (id_venda, id_produto, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (id_venda, id_produto, quantidade, preco)
            )

            # Atualiza o estoque
            cursor.execute(
                """
                UPDATE produto
                SET estoque = estoque - %s
                WHERE id_produto = %s
                """,
                (quantidade, id_produto)
            )

            conexao.commit()

            return True, (
                f"Venda #{id_venda} registrada! "
                f"Total: R$ {total:.2f}"
            )

        except Exception as erro:
            conexao.rollback()
            print("Erro ao registrar venda:", erro)

            return False, f"Erro ao registrar venda: {erro}"

        finally:
            cursor.close()
            conexao.close()

    def dashboard(self):

        conexao = conectar()

        if conexao is None:
            return {
                "produtos": 0,
                "clientes": 0,
                "vendedores": 0,
                "vendas": 0,
                "faturamento": 0
            }

        cursor = conexao.cursor(dictionary=True)

        try:
            consultas = {
                "produtos": "SELECT COUNT(*) AS total FROM produto",
                "clientes": "SELECT COUNT(*) AS total FROM cliente",
                "vendedores": "SELECT COUNT(*) AS total FROM vendedor",
                "vendas": "SELECT COUNT(*) AS total FROM vendas",
                "faturamento": """
                    SELECT COALESCE(SUM(total), 0) AS total
                    FROM vendas
                """
            }

            resultado = {}

            for chave, sql in consultas.items():
                cursor.execute(sql)
                resultado[chave] = cursor.fetchone()["total"]

            return resultado

        except Exception as erro:
            print("Erro no dashboard:", erro)

            return {
                "produtos": 0,
                "clientes": 0,
                "vendedores": 0,
                "vendas": 0,
                "faturamento": 0
            }

        finally:
            cursor.close()
            conexao.close()
