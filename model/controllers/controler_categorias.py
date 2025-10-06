from data.conexao import Conection
import datetime

class Categoria:

    # Conexao com o banco de dados para criar uma categoria
    def cadastrar_categoria(nome, cpf):

        data_hora = datetime.datetime.today()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO categoria (
                        nome, data_hora, cpf)
                    VALUES (
                        %s, %s, %s)"""

        nome = nome.upper()
        valores = (nome, data_hora, cpf)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

    # Conexao com o banco de dados para criar um tipo com base em uma categoria
    def cadastrar_tipo_categoria(nome, cpf, cod_categoria):

        data_hora = datetime.datetime.today()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO tipo (
                        nome, data_hora, cpf, cod_categoria)
                    VALUES (
                        %s, %s, %s, %s)"""

        nome = nome.upper()
        valores = (nome, data_hora, cpf, cod_categoria)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

    # Conexao com o banco de dados para criar uma caracteristica com base no tipo
    def cadastrar_tipo_caracteristica(nome, cod_tipo, cpf):

        data_hora = datetime.datetime.today()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO caracteristica (
                        nome, data_hora, cod_tipo, cpf)
                    VALUES (
                        %s, %s, %s, %s)"""

        nome = nome.upper()
        valores = (nome, data_hora, cod_tipo, cpf)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()