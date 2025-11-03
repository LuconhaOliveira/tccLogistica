from data.conexao import Conection

class Historico:

    # Recupera as alterações dos produtos e estantes 
    def recuperar_historico_alteracoes(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """
                SELECT
                    cod_alteracao,
                    alteracao_realizada,
                    DATE_FORMAT(data_hora, '%d/%m/%Y %h:%i') AS data_hora
                FROM
                    alteracao_produto_estante
                WHERE
                    cpf = %s
                ORDER BY
                    data_hora DESC;"""

        valor = (cpf,)

        cursor.execute(sql, valor)

        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado
    
    
    # Excluir todas as alterações dos produtos e estantes 
    def excluir_historico_alteracoes(cpf):
        
        conexao = Conection.create_connection()

        cursor = conexao.cursor(dictionary = True) 
        
        sql = """ DELETE FROM alteracao_produto_estante WHERE cpf = %s; """

        valor = (cpf,)

        cursor.execute(sql, valor)
        
        conexao.commit() 
        
        cursor.close()
        conexao.close()

        # Retorna True ou None, indicando sucesso, mas o retorno não é mais usado
        return True 