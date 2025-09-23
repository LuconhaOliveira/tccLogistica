from hashlib import sha256
from data.conexao import Conexao
from flask import session

class Usuario:

    # Conexao com o banco de dados para cadastrar um novo usuario
    def cadastrar_usuario(cpf, nome, senha):
        
        senha = sha256(senha.encode()).hexdigest()
            
        conexao = Conexao.criar_conexao()

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