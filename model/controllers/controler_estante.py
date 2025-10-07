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
            
            sql = "SELECT estante.cod_estante,estante.nome AS 'nome',categoria.nome AS 'categoria',estante.cod_categoria " \
            "FROM estante INNER JOIN categoria ON " \
            "categoria.cod_categoria = estante.cod_categoria " \
            "WHERE estante.cpf= %s"
            valores = (session["cpf"],)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            print(resultado)
            
            if resultado:
                #estantes = [{"cod_estante":estante[0], "nome": estante[1], "categoria": estante[2]} for estante in resultado]
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
            
            sql = """SELECT produto.nome AS 'nome', produto.imagem AS 'imagem', produto.coluna AS 'coluna', produto.linha AS 'linha', estante.nome AS 'estante'
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
            sql = """SELECT estante.cod_estante,estante.nome AS 'nome',categoria.nome AS 'categoria',estante.cod_categoria 
            FROM estante INNER JOIN categoria 
            ON categoria.cod_categoria = estante.cod_categoria 
            WHERE estante.cpf= %s AND categoria.cod_categoria=%s"""
            valores = (session["cpf"],filtro)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            
            if resultado:
                print(resultado)
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

    # Conexao com o banco de dados para excluir uma estante
    def remover_estante(cod_estante):

        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = "DELETE FROM estante WHERE cod_estante = %s;"

        cursor.execute(sql, (cod_estante,))
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
