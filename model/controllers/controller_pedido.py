from data.conexao import Conection
from flask import session
from mysql.connector import Error
import datetime

class Pedido:

    def criar_pedido():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor()
            
            sql = """INSERT INTO pedido (
                        cpf, data_pedido, ativo)
                    VALUES (
                        %s, %s, 1)"""
            valores = (session["cpf"],datetime.now())
            
            cursor.execute(sql, valores)
            
            cursor.commit()
            return cursor.lastrowid

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    def adicionar_ao_pedido(cod_pedido,cod_produto,quantidade):
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor()
            
            sql = """INSERT INTO item_pedido (
                        cod_pedido, cod_produto, quantidade)
                    VALUES (
                        %s, %s,%s)"""
            valores = (cod_pedido,cod_produto,quantidade)
            
            cursor.execute(sql, valores)
            
            cursor.commit()

            cursor.close()
            conexao.close()

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    def verificar_pedido_ativo():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor()
            
            sql = """SELECT cod_pedido FROM pedido WHERE cpf=%s AND ativo=1"""
            valores = (session["cpf"],)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchone()

            if resultado:
                return True,resultado
            else:
                return False,None

            cursor.close()
            conexao.close()

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    
#TODO: NA HORA DE FECHAR O PEDIDO LEMBRA DE MUDAR O ATIVO PARA 0