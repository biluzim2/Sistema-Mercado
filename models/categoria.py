from database.conexao import conectar

class Categoria:

    def cadastrar(self, nome):
        conexao = conectar()

        if conexao is None:
            return False

        cursor = conexao.cursor()

        try:
            sql = "INSERT INTO categoria (nome) VALUES (%s)"
            cursor.execute(sql, (nome))
            conexao.commit()
            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar categoria", erro)
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

           cursor.execute("Select * From categoria ORDER BY nome")
           return cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()


        