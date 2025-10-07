from data.conexao import Conection
from flask import session
from mysql.connector import Error
import datetime

class Historico:

    # Recupera as estantes registradas anteriormente
    def recuperar_historico_alteracoes(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """ """

        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado