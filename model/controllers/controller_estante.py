from data.conexao import Conection
from flask import session
from mysql.connector import Error

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
            
            sql = "SELECT estante.enderecamento,estante.estante,categoria.nome FROM estante INNER JOIN categoria ON categoria.cod_categoria = estante.cod_categoria WHERE cpf= %s and enderecamento=%s"
            valores = (session["cpf"],id)
            
            cursor.execute(sql, valores)
            
            resultado = cursor.fetchone()
            
            if resultado:
                print(resultado)
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