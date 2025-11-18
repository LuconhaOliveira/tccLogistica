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
                        cpf, data_pedido)
                    VALUES (
                        %s, %s)"""
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

    def buscar_itens_pedido():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT produto.cod_produto, produto.imagem, produto.nome, produto.descricao, produto.valor, item_pedido.quantidade FROM pedido 
INNER JOIN item_pedido ON item_pedido.cod_pedido = pedido.cod_pedido
INNER JOIN produto ON produto.cod_produto=item_pedido.cod_produto 
WHERE pedido.cpf=%s;"""
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


    def remover_produto(cod_produto):
            try:
                conexao = Conection.create_connection()
                if not conexao:
                    return None

                cursor = conexao.cursor()

                sql = """UPDATE produto SET quantidade=quantidade+
    (SELECT quantidade FROM item_pedido INNER JOIN pedido ON pedido.cod_pedido=item_pedido.cod_pedido 
    WHERE item_pedido.cod_produto=%s) WHERE cod_produto=%s;"""
                valores = (cod_produto,cod_produto)
                
                cursor.execute(sql, valores)
                conexao.commit()
                        
                sql = """DELETE item_pedido
    FROM item_pedido
    INNER JOIN pedido ON pedido.cod_pedido = item_pedido.cod_pedido
    WHERE item_pedido.cod_produto = %s;"""
                valores = (cod_produto,)
                
                cursor.execute(sql, valores)
                
                conexao.commit()

            except Error as e:
                print(f"Erro ao validar login: {e}")
                return None

            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'conexao' in locals() and conexao:
                    conexao.close()

    def remover_pedido():
            try:
                conexao = Conection.create_connection()
                if not conexao:
                    return None

                cursor = conexao.cursor()

                itens = Pedido.buscar_itens_pedido()

                mensagem=""

                for item in itens:
                    mensagem+=f"""Nome:{item['nome']},Valor:{item['valor']},Quantidade:{item['quantidade']},Descricao:{item['descricao']};"""

                print(mensagem)
                

                sql = """INSERT INTO historico_pedido(cpf,pedido_realizado) 
                VALUES(%s,%s);"""
                valores = (session['cpf'],mensagem)
                
                cursor.execute(sql, valores)
                conexao.commit()


                cod_pedido=Pedido.buscar_pedido()[0]
                sql = """DELETE FROM item_pedido WHERE cod_pedido=%s;"""
                valores = (cod_pedido,)
                
                cursor.execute(sql, valores)
                conexao.commit()

                sql = """DELETE FROM pedido WHERE cpf=%s;"""
                valores = (session['cpf'],)
                
                cursor.execute(sql, valores)
                conexao.commit()

            except Error as e:
                print(f"Erro ao validar login: {e}")
                return None

            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'conexao' in locals() and conexao:
                    conexao.close()
    
    def buscar_pedido():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor()
            
            sql = """SELECT cod_pedido FROM pedido WHERE cpf=%s;"""
            valores = (session["cpf"],)
            
            cursor.execute(sql, valores)
            resultado=cursor.fetchone()
            if not resultado: resultado=None

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

    def buscar_historico():
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT cod_historico,pedido_realizado,data_hora FROM historico_pedido WHERE cpf=%s;"""
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