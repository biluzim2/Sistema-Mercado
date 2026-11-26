import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

dados = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def conectar():
    try:
        conexao = mysql.connector.connect(**dados)

        if conexao.is_connected():
            print("Banco conectado com sucesso!")
            return conexao

    except Error as erro:
        print("Erro ao conectar com o banco de dados:", erro)

    return None