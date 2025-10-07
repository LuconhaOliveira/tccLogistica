from data.conexao import Conection
import datetime

class Categoria:

# CATEGORIA ------------------------------------------------------------------------------------------------------#

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

    # Recupera as categorias registradas anteriormente
    def recuperar_categoria(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """SELECT cod_categoria, nome, data_hora 
                 FROM categoria
                 WHERE cpf = %s;"""
        
        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado
    
    # Conexao com o banco de dados para excluir uma categoria
    def remover_categoria(cod_categoria):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = "DELETE FROM categoria WHERE cod_categoria = %s;"

        cursor.execute(sql, (cod_categoria,))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True 
    
# TIPO ------------------------------------------------------------------------------------------------------#

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

    # Recupera os tipos registradas anteriormente
    def recuperar_tipo(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """select cod_tipo, nome, data_hora from tipo where cpf = %s;"""

        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado
    
    # Conexao com o banco de dados para excluir um tipo
    def remover_tipo(cod_categoria):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = "DELETE FROM tipo WHERE cod_tipo = %s;"

        cursor.execute(sql, (cod_categoria,))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True 
    
# CARACTERISTICA ------------------------------------------------------------------------------------------------------#

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
    
    # Recupera as caracteristicas registradas anteriormente
    def recuperar_caracteristica(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """select cod_caracteristica, nome, data_hora from caracteristica where cpf = %s;"""

        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado
    
    # Conexao com o banco de dados para excluir uma caracteristica
    def remover_caracteristica(cod_caracteristica):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = "DELETE FROM caracteristica WHERE cod_caracteristica = %s;"

        cursor.execute(sql, (cod_caracteristica,))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True 