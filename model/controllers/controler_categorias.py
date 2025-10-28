from data.conexao import Conection
import datetime
from mysql.connector import Error

class Categoria:

# CATEGORIA ------------------------------------------------------------------------------------------------------#

    # Verifica se a Categoria está ligada a alguma Estante ou Produto
    def verificar_dependencia_categoria(cod_categoria):

        try:
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
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchone()
            if resultado:
                # O resultado será (1,) se houver dependência, ou (0,) se não houver
                dependencia = resultado[0] == 1

            return dependencia # Retorna True se houver dependência

        except Error as e:
            # Erro no banco de dados (ex: tabela inexistente, erro de sintaxe)
            print(f"Erro no banco de dados ao verificar dependência da categoria: {e}")
            return True 

        except Exception as e:
            # Erros inesperados (ex: falha de conexão)
            print(f"Erro inesperado ao verificar dependência da categoria: {e}")
            return True 

        finally:
            # Garante que o cursor e a conexão sejam fechados
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

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

        try:
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
            
            resultado = cursor.fetchone()

            if resultado:
                # O resultado será (1,) se houver dependência, ou (0,) se não houver
                dependencia = resultado[0] == 1

            return dependencia # Retorna True se houver dependência

        except Error as e:
            # Erro no banco de dados (ex: tabela inexistente, erro de sintaxe)
            print(f"Erro no banco de dados ao verificar dependência do tipo: {e}")
            return True 

        except Exception as e:
            # Erros inesperados (ex: falha de conexão)
            print(f"Erro inesperado ao verificar dependência do tipo: {e}")
            return True 

        finally:
            # Garante que o cursor e a conexão sejam fechados
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
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
    @staticmethod
    def verificar_dependencia_caracterisica(cod_caracteristica):

        try:
            conexao = Conection.create_connection()

            cursor = conexao.cursor()

            # Verifica se a caracteristica está na tabela de produto_caracteristica
            sql = """
                SELECT EXISTS (
                    SELECT 1 FROM produto_caracteristica WHERE cod_caracteristica = %s
                ) AS dependencia;
            """

            valor = (cod_caracteristica,)
            
            # Executa a consulta
            cursor.execute(sql, valor)

            resultado = cursor.fetchone()
            
            if resultado:
                # O resultado será (1,) se houver dependência, ou (0,) se não houver
                dependencia = resultado[0] == 1

                return dependencia # Retorna True se houver dependência

        except Error as e:
            # Erro no banco de dados (ex: tabela inexistente, erro de sintaxe)
            print(f"Erro no banco de dados ao verificar dependência da caracteristica: {e}")
            return True 

        except Exception as e:
            # Erros inesperados (ex: falha de conexão)
            print(f"Erro inesperado ao verificar dependência da caracteristica: {e}")
            return True 

        finally:
                # Garante que o cursor e a conexão sejam fechados
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'conexao' in locals() and conexao:
                    conexao.close()
    
    # Conexao com o banco de dados para criar uma caracteristica com base no tipo
    @staticmethod
    def cadastrar_tipo_caracteristica(nome, cod_tipo, cpf):
        data_hora = datetime.datetime.today()
        conexao = None
        cursor = None
            
        try:
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
            
        except Exception as e:
            # Em caso de erro, faz rollback para manter a integridade
            if conexao: conexao.rollback()
            
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    
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
    @staticmethod
    def remover_caracteristica(cod_caracteristica):
        conexao = None
        cursor = None

        # 1. Verifica se a caracteristica possui uma dependencia 
        if Categoria.verificar_dependencia_caracterisica(cod_caracteristica):
            # Retorna se a remoção falhou por conta da dependência
            return False # Não pode excluir

        try:
            # 2. Se não possuir uma dependencia, executa a exclusão da caracteristica
            conexao = Conection.create_connection()
            cursor = conexao.cursor()

            sql = "DELETE FROM caracteristica WHERE cod_caracteristica = %s;"
            valor = (cod_caracteristica,)

            cursor.execute(sql, valor)
            conexao.commit()
            
            # 3. Retorna True se excluiu algo (rowcount > 0)
            return cursor.rowcount > 0

        except Exception as e:
            # Em caso de erro, faz rollback e retorna False
            if conexao: conexao.rollback()
            return False # Falha na DB

        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

