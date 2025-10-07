from data.conexao import Conection
import datetime

class Categoria:

# CATEGORIA ------------------------------------------------------------------------------------------------------#

    # Verifica se a Categoria está ligada a alguma Estante ou Produto
    def verificar_dependencia_categoria(cod_categoria):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        # Verifica se a categoria está em alguma estante ou em algum produto
        sql = """
            SELECT EXISTS (
                SELECT 1 FROM estante WHERE cod_categoria = %s
                UNION ALL
                SELECT 1 FROM produto WHERE cod_categoria = %s
            ) AS dependencia;
        """

        valores = (cod_categoria, cod_categoria)
        
        # Executa a consulta
        cursor.execute(sql, valores)
        
        # O resultado será (1,) se houver dependência, ou (0,) se não houver
        dependencia = cursor.fetchone()[0] == 1

        cursor.close()
        conexao.close()
        return dependencia # Retorna True se houver dependência

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

        # Verifica se a categoria possui uma dependencia 
        if Categoria.verificar_dependencia_categoria(cod_categoria):
            # Retorna se a remoção falhou por conta da dependência
            return False # Não pode excluir

        # Se não possuir uma dependencia, executa a exclusão da categoria
        conexao = Conection.create_connection()
        cursor = conexao.cursor()

        sql = "DELETE FROM categoria WHERE cod_categoria = %s;"

        valor = (cod_categoria,)

        cursor.execute(sql, valor)

        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True
    
# TIPO ------------------------------------------------------------------------------------------------------#

    # Verifica se o Tipo está ligado a alguma Estante ou Produto
    def verificar_dependencia_tipo(cod_tipo):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        # Verifica se o tipo está em alguma categoria
        sql = """
            SELECT EXISTS (
                SELECT 1 FROM caracteristica WHERE cod_tipo = %s
            ) AS dependencia;
        """

        valor = (cod_tipo,)
        
        # Executa a consulta
        cursor.execute(sql, valor)
        
        # O resultado será (1,) se houver dependência, ou (0,) se não houver
        dependencia = cursor.fetchone()[0] == 1

        cursor.close()
        conexao.close()
        return dependencia # Retorna True se houver dependência

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
    def remover_tipo(cod_tipo):

        # Verifica se a categoria possui uma dependencia 
        if Categoria.verificar_dependencia_tipo(cod_tipo):
            # Retorna se a remoção falhou por conta da dependência
            return False # Não pode excluir

        # Se não possuir uma dependencia, executa a exclusão do tipo
        conexao = Conection.create_connection()
        cursor = conexao.cursor()

        sql = "DELETE FROM tipo WHERE cod_tipo = %s;"

        valor = (cod_tipo,)

        cursor.execute(sql, valor)

        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True
    
# CARACTERISTICA ------------------------------------------------------------------------------------------------------#

   # Verifica se a Caracteristica está ligada a alguma Estante ou Produto
    def verificar_dependencia_caracterisica(cod_caracteristica):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        # Verifica se a categoria está em alguma estante ou em algum produto
        sql = """
            SELECT EXISTS (
                SELECT 1 FROM produto WHERE cod_caracteristica = %s
            ) AS dependencia;
        """

        valor = (cod_caracteristica,)
        
        # Executa a consulta
        cursor.execute(sql, valor)
        
        # O resultado será (1,) se houver dependência, ou (0,) se não houver
        dependencia = cursor.fetchone()[0] == 1

        cursor.close()
        conexao.close()
        return dependencia # Retorna True se houver dependência
    
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

        # Verifica se a categoria possui uma dependencia 
        if Categoria.verificar_dependencia_caracterisica(cod_caracteristica):
            # Retorna se a remoção falhou por conta da dependência
            return False # Não pode excluir

        # Se não possuir uma dependencia, executa a exclusão do tipo
        conexao = Conection.create_connection()
        cursor = conexao.cursor()

        sql = "DELETE FROM caracteristica WHERE cod_caracteristica = %s;"

        valor = (cod_caracteristica,)

        cursor.execute(sql, valor)

        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True

