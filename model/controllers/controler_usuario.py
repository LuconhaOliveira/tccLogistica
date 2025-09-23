from hashlib import sha256
from data.conexao import Conection
from flask import session
from mysql.connector import Error

class Usuario:

    # Conexao com o banco de dados para cadastrar um novo usuario
    def cadastrar_usuario(cpf, nome, senha):
        
        senha = sha256(senha.encode()).hexdigest()
            
        conexao = Conection.create_connection()

        cursor = conexao.cursor()

        sql = """INSERT INTO usuario (
                        cpf, 
                        nome,
                        senha)
                        
                    VALUES (
                        %s, %s, %s)"""

        valores = (cpf, nome, senha)

        cursor.execute(sql, valores)

        conexao.commit()

        cursor.close()
        conexao.close()

    
    @staticmethod
    def validar_login(cpf, senha):

        """
        Valida as credenciais do usuário.
        
        Retorna o nome do usuário se o login for bem-sucedido,
        caso contrário, retorna None.
        """

        try:
            
            senha_criptografada = sha256(senha.encode()).hexdigest()
            
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor()
            
            sql = "SELECT nome FROM usuario WHERE cpf = %s and senha = %s"
            valores = (cpf, senha_criptografada)
            
            cursor.execute(sql, valores)
            
            # Pega o primeiro (e único) resultado da consulta
            resultado = cursor.fetchone()
            
            if resultado:
                # Retorna o nome do usuário se as credenciais forem válidas
                print("Login bem-sucedido!")
                return resultado[0] # O nome está na primeira posição da tupla
            else:
                # Retorna None se as credenciais forem inválidas
                print("CPF ou senha incorretos.")
                return None

        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexao' in locals() and conexao:
                conexao.close()