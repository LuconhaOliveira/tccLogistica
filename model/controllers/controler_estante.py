from data.conexao import Conection
from flask import session
from mysql.connector import Error
import datetime

class Estante:

    def buscar_estantes():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = "SELECT estante.cod_estante,estante.nome AS estante,categoria.nome AS categoria,estante.cod_categoria FROM estante " \
            "INNER JOIN categoria ON categoria.cod_categoria = estante.cod_categoria " \
            "WHERE estante.cpf= %s"
            valores = (session["cpf"],)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            
            if resultado:
                return resultado
            else:
                return None

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    def buscar_estante(id):
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT produto.cod_produto, produto.nome, produto.imagem, produto.coluna, produto.linha
                        FROM produto INNER JOIN usuario ON usuario.cpf = produto.cpf
                        INNER JOIN estante ON produto.cod_estante = estante.cod_estante
                        WHERE usuario.cpf= %s and estante.cod_estante= %s"""
            valores = (session["cpf"],id)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            
            if resultado:
                return resultado
            else:
                return None

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    def buscar_estantes_filtro(filtro):
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT estante.cod_estante,estante.nome AS estante,categoria.nome AS categoria, estante.cod_categoria FROM estante
            INNER JOIN categoria ON categoria.cod_categoria = estante.cod_categoria
            WHERE estante.cpf= %s AND estante.cod_categoria=%s"""
            valores = (session["cpf"],filtro)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            
            if resultado:
                return resultado
            else:
                return None

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    # Conexao com o banco de dados para criar uma nova estante
    def cadastrar_estante(nome, cpf, cod_categoria):
        try:

            data_hora = datetime.datetime.today()
                
            conexao = Conection.create_connection()

            cursor = conexao.cursor()

            sql = """INSERT INTO estante (
                            nome, data_hora, cpf, cod_categoria)
                        VALUES (
                            %s, %s, %s, %s)"""

            nome = nome.upper()
            valores = (nome, data_hora, cpf, cod_categoria)

            cursor.execute(sql, valores)

            conexao.commit()

            return True
        
        except Exception as e:
            # Em caso de erro, faz rollback e retorna False
            if conexao: 
                conexao.rollback()
            print(f"Erro ao cadastrar estante: {e}")
            return False

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    # Conexao com o banco de dados para excluir todos os produtos da estante
    def remover_produtos_estante(cod_estante):

        try:
            conexao = Conection.create_connection()
            if not conexao:
                return False
            cursor = conexao.cursor()
            
            # Localiza e exclui todos os produtos dentro da tabela de produtos_caracteristica, para remover a dependencia
            sql_dependencia = """
                DELETE FROM produto_caracteristica 
                WHERE cod_produto IN (
                    SELECT cod_produto FROM produto WHERE cod_estante = %s
                );
            """
            valor_estante = (cod_estante,)
            
            cursor.execute(sql_dependencia, valor_estante) 

            # Exclui todos os produtos da estante
            sql_produtos = "DELETE FROM produto WHERE cod_estante = %s"
            
            cursor.execute(sql_produtos, valor_estante) # Executa o DELETE dos produtos
            
            conexao.commit()
            return True
        
        except Exception as e:
            # Em caso de erro, faz rollback e retorna False
            if conexao: 
                conexao.rollback()
            print(f"Erro inesperado ao remover produtos: {e}")
            return False

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()


    # Conexao com o banco de dados para excluir uma estante mesmo com todos os produtos dentro
    def remover_estante(cod_estante):

        try:
            conexao = Conection.create_connection()
            if not conexao:
                return False

            # Remove as dependências dos produtos dentro da tabela de produto_caracteristica
            sql_del_caracteristicas = """
                DELETE FROM produto_caracteristica 
                WHERE cod_produto IN (
                    SELECT cod_produto FROM produto WHERE cod_estante = %s
                );
            """

            cursor = conexao.cursor()

            valor = (cod_estante,)

            cursor.execute(sql_del_caracteristicas, valor) 

            # Remove todos os produtos da estante  
            sql_del_produtos = "DELETE FROM produto WHERE cod_estante = %s"
            cursor.execute(sql_del_produtos, valor)

            # Remove a estante, por fim
            sql_del_estante = "DELETE FROM estante WHERE cod_estante = %s;"
            cursor.execute(sql_del_estante, valor)

            conexao.commit()
            return True
        
        except Exception as e:
            if 'conexao' in locals() and conexao: 
                conexao.rollback()
            print(f"Erro inesperado ao remover estante e seus produtos: {e}")
            return False
            
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()
    
    # Recupera as estantes registradas anteriormente
    def recuperar_estante(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """select cod_estante, nome, data_hora from estante where cpf = %s;"""

        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado
    
    # Busca o nome da estante desejada no banco de dados
    def buscar_nome_estante(cod_estante):
        try:
            conexao = Conection.create_connection()

            if not conexao:
                return "Estante" # Retorna um nome padrão em caso de erro

            cursor = conexao.cursor()
            
            # Buscar o nome da estante no banco
            sql = "SELECT nome FROM estante WHERE cod_estante = %s"
            valores = (cod_estante,)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Retorna o primeiro elemento da tupla (o nome da estante)
                return resultado[0]
            else:
                return "Estante Não Encontrada"

        except Error as e:
            print(f"Erro ao buscar nome da estante: {e}")
            return "Erro de Busca"

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()
