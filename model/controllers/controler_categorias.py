from data.conexao import Conection
from flask import session
import datetime

class Categoria:

    # Conexao com o banco de dados para criar uma categoria
    def cadastrar_categoria(nome):

        data_hora = datetime.datetime.today()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO categoria (
                        nome, data_hora)
                    VALUES (
                        %s)"""

        valores = (nome)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

    # Conexao com o banco de dados para criar um tipo com base em uma categoria
    def cadastrar_tipo_categoria(nome, cod_categoria):
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO tipo (
                        nome, cod_categoria)
                    VALUES (
                        %s, %s)"""

        valores = (nome, cod_categoria)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

    # Conexao com o banco de dados para criar uma caracteristica com base no tipo
    def cadastrar_tipo_categoria(nome, cod_tipo, cpf):
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO caracteristica (
                        nome, cod_tipo, cpf)
                    VALUES (
                        %s, %s, %s)"""

        valores = (nome, cod_tipo, cpf)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()