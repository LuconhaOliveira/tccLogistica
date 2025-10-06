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

            cursor = conexao.cursor()
            
            sql = "SELECT estante.enderecamento,estante.estante,categoria.nome FROM estante INNER JOIN categoria ON categoria.cod_categoria = estante.cod_categoria WHERE cpf= %s"
            valores = (session["cpf"],)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchall()
            
            if resultado:
                estantes = [{"enderecamento":estante[0], "estante": estante[1], "categoria": estante[2]} for estante in resultado]
                return estantes
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
            
            sql = """SELECT produto.nome, produto.sku, produto.imagem, tipo.nome AS 'tipo'
                        FROM produto INNER JOIN usuario ON usuario.cpf = produto.cpf
                        INNER JOIN estante ON usuario.cpf = estante.cpf
                        INNER JOIN tipo ON tipo.cod_tipo=produto.cod_tipo
                        WHERE usuario.cpf= %s and enderecamento=%s"""
            valores = (session["cpf"],id)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchone()
            
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
    def cadastrar_estante(cod_estante, nome, cpf, cod_categoria):

        data_hora = datetime.datetime.today()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO estante (
                        cod_estante, nome, data_hora, cpf, cod_categoria)
                    VALUES (
                        %s, %s, %s, %s, %s)"""

        nome = nome.upper()
        valores = (cod_estante, nome, data_hora, cpf, cod_categoria)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()
