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

            cursor.close()
            conexao.close()
            return True
        except Exception as e:
            # Loga o erro e retorna False para o Flask detectar falha
            print(f"Erro ao cadastrar estante no banco de dados: {e}")

            try:
                conexao.rollback()
            except:
                pass

        return False

    # Verifica se a Estante está ligada a algum produto
    def verificar_dependencia_estante(cod_estante):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        # Verifica se a estante está em algum produto
        sql = """
            SELECT EXISTS (
                    SELECT 1 FROM produto WHERE cod_estante = %s  
                ) AS dependencia;
        """

        valores = (cod_estante,)
        
        # Executa a consulta
        cursor.execute(sql, valores)
        
        # O resultado será (1,) se houver dependência, ou (0,) se não houver
        dependencia = cursor.fetchone()[0] == 1

        cursor.close()
        conexao.close()
        return dependencia # Retorna True se houver dependência    

    # Conexao com o banco de dados para excluir uma estante
    def remover_estante(cod_estante):

        # Verifica se a estante possui uma dependencia 
        if  Estante.verificar_dependencia_estante(cod_estante):
            # Retorna se a remoção falhou por conta da dependência
            return False # Não pode excluir

        # Se não possuir uma dependencia, executa a exclusão da estante
        conexao = Conection.create_connection()
        cursor = conexao.cursor()

        sql = "DELETE FROM estante WHERE cod_estante = %s;"

        valor = (cod_estante,)

        cursor.execute(sql, valor)

        conexao.commit()
        
        cursor.close()
        conexao.close()
        return True
    
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
