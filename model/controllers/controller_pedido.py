from data.conexao import Conection
from flask import session
from mysql.connector import Error
from datetime import datetime

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
            
            conexao.commit()
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

            sql = """SELECT SUM(quantidade) FROM item_pedido WHERE cod_produto=%s"""
            valores = (cod_produto,)
            
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()[0]
            if not resultado: resultado=0

            sql = """SELECT quantidade FROM produto WHERE cod_produto=%s"""
            valores = (cod_produto,)
            
            cursor.execute(sql, valores)
            resultado2 = cursor.fetchone()[0]
            print(resultado)
            print(quantidade)

            if resultado2>=int(quantidade)+int(resultado):
                sql = """INSERT INTO item_pedido (
                            cod_pedido, cod_produto, quantidade)
                        VALUES (
                            %s, %s,%s)"""
                valores = (cod_pedido,cod_produto,quantidade)
                
                cursor.execute(sql, valores)
                
                conexao.commit()
            else:
                raise ValueError("Quantidade adicionada maior que o estoque")

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
                return True,resultado[0]
            else:
                return False,None

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()

    
#TODO: NA HORA DE FECHAR O PEDIDO LEMBRA DE MUDAR O ATIVO PARA 0