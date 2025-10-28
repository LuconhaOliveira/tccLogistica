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

            sql = """SELECT cod_pedido FROM item_pedido WHERE cod_produto=%s AND cod_pedido=%s"""
            valores = (cod_produto,cod_pedido)
            
            cursor.execute(sql, valores)
            pedido = cursor.fetchone()

            if pedido:
                raise ValueError("Produto ja está no pedido atual")
            else:
                sql = """SELECT quantidade FROM produto WHERE cod_produto=%s"""
                valores = (cod_produto,)
                
                cursor.execute(sql, valores)
                resultado = cursor.fetchone()[0]

                if resultado>=int(quantidade):
                    sql = """UPDATE produto SET quantidade=quantidade-%s WHERE cod_produto=%s;"""
                    valores = (quantidade,cod_produto)
                    
                    cursor.execute(sql, valores)
                        
                    conexao.commit()
                    
                    sql = """INSERT INTO item_pedido (
                                cod_pedido, cod_produto, quantidade)
                            VALUES (
                                %s, %s,%s)"""
                    valores = (cod_pedido,cod_produto,quantidade)
                    
                    cursor.execute(sql, valores)
                    
                    conexao.commit()
                else:
                    raise ValueError("Quantidade adicionada maior que o estoque")

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

    def buscar_itens_pedido():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT produto.cod_produto, produto.imagem, produto.nome, produto.valor, item_pedido.quantidade FROM pedido 
INNER JOIN item_pedido ON item_pedido.cod_pedido = pedido.cod_pedido
INNER JOIN produto ON produto.cod_produto=item_pedido.cod_produto 
WHERE pedido.cpf=%s AND pedido.ativo=1;"""
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

    
#TODO: NA HORA DE FECHAR O PEDIDO LEMBRA DE MUDAR O ATIVO PARA 0