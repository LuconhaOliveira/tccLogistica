from data.conexao import Conection

class Historico:

    # Recupera as alterações dos produtos e estantes 
    def recuperar_historico_alteracoes(cpf):
        
        try:
            # Tenta criar a conexão
            conexao = Conection.create_connection()
            cursor = conexao.cursor(dictionary=True) 
            
            sql = """
                SELECT
                    cod_alteracao,
                    alteracao_realizada,
                    DATE_FORMAT(
                        CONVERT_TZ(data_hora, 'UTC', 'America/Sao_Paulo'),
                        '%d/%m/%Y %H:%i' 
                    ) AS data_hora
                FROM
                    alteracao_produto_estante
                WHERE
                    cpf = %s
                ORDER BY
                    data_hora DESC;"""

            valor = (cpf,)

            # Tenta executar a consulta dentro do banco de dados
            cursor.execute(sql, valor)
            resultado = cursor.fetchall()
            

        except Exception as e:
            # Erros inesperados (ex: falha de conexão)
            print(f"Erro ao recuperar histórico de alterações para o CPF {cpf}: {e}")
            resultado = []
            
        finally:
            # Garante que o cursor e a conexão sejam fechados
            if cursor:
                cursor.close()
            if conexao:
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