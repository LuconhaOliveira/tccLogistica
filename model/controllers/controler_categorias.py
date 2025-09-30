from data.conexao import Conection
from flask import session

class Categoria:

    # Conexao com o banco de dados para criar uma categoria
    def cadastrar_categoria(nome):
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO categoria (
                        nome)
                    VALUES (
                        %s)"""

        valores = (nome)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()