from data.conexao import Conection
from flask import session

class Estante:

    # Conexao com o banco de dados para criar uma nova estante
    def cadastrar_estante(enderecamento, estante, linha, coluna, cpf, cod_categoria):
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO estante (
                        enderecamento, 
                        estante,
                        linha,
                        coluna,
                        cpf,
                        cod_categoria)
                    VALUES (
                        %s, %s, %s, %s, %s, %s)"""

        valores = (enderecamento, estante, linha, coluna, cpf, cod_categoria)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()