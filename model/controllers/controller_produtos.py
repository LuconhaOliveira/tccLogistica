from data.conexao import Conection
from mysql.connector import Error 
from datetime import datetime # Necessário para a coluna data_hora
from flask import session

class ControleProduto:

    @staticmethod
    def cadastrar_produto(nome, descricao, arquivo_imagem, quantidade, valor, sku, 
                          coluna, linha, cod_estante, cod_categoria, 
                          cod_tipo, cod_caracteristica, user_cpf):
        """
        Cadastra um novo produto no banco de dados.

        Argumentos (13 ao total, mais a data/hora gerada internamente):
        - nome (VARCHAR)
        - descricao (VARCHAR)
        - arquivo_imagem (bytes BLOB): Conteúdo binário da imagem.
        - quantidade (INT)
        - valor (FLOAT)
        - sku (VARCHAR)
        - coluna (VARCHAR)
        - linha (VARCHAR)
        - cod_estante (INT)
        - cod_categoria (INT)
        - cod_tipo (INT)
        - cod_caracteristica (INT)
        - user_cpf (VARCHAR)

        Retorna:
        - (True, cod_produto_inserido) se o cadastro for bem-sucedido.
        - (False, mensagem_de_erro) em caso de falha.
        """
        conexao = None
        cursor = None
        
        # 1. TRATAMENTO DA IMAGEM
        # O argumento 'arquivo_imagem' JÁ DEVE SER OS BYTES (BLOB)
        # Se você estiver usando o código da rota POST anterior, a leitura
        # (.read()) já foi feita. Ajustei a assinatura para refletir isso.
        produto_imagem = arquivo_imagem

        try:
            # 2. CONEXÃO
            conexao = Conection.create_connection()
            if not conexao:
                return False, "Falha na conexão com o banco de dados."

            cursor = conexao.cursor()

            # 3. COMANDO SQL: Inclui TODAS as 14 colunas da tabela 'produto'
            sql = """
            INSERT INTO produto (
                data_hora, nome, descricao, imagem, quantidade, valor, sku, 
                coluna, linha, cpf, cod_estante, cod_categoria, cod_tipo, cod_caracteristica
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # 4. VALORES: Ordem deve ser EXATA à do SQL
            valores = (
                datetime.now(),
                nome, 
                descricao, 
                produto_imagem, 
                quantidade, 
                valor, 
                sku, 
                coluna, 
                linha, 
                user_cpf,  # CPF do usuário (Chave estrangeira)
                cod_estante,
                cod_categoria, 
                cod_tipo, 
                cod_caracteristica
            )

            # 5. EXECUÇÃO
            cursor.execute(sql, valores)
            conexao.commit()
            
            produto_id = cursor.lastrowid
            print(f"Produto '{nome}' cadastrado com sucesso. ID: {produto_id}")
            
            # MUDANÇA: Retorna True e o ID do novo produto
            return True, produto_id

        except Error as e:
            # Captura erros de banco de dados
            if conexao: conexao.rollback()
            print(f"Erro ao cadastrar produto (SQL/DB): {e}")
            return False, f"Erro no banco de dados: {e}"

        except Exception as e:
            # Captura outros erros
            print(f"Erro inesperado no processo de cadastro: {e}")
            return False, f"Erro inesperado: {e}"

        finally:
            # GARANTIA DE LIMPEZA DE RECURSOS
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def buscar_produto(id):
        try:
            conexao = Conection.create_connection()
            if not conexao:
                return None

            cursor = conexao.cursor(dictionary=True)
            
            sql = """SELECT produto.cod_produto,produto.imagem,produto.descricao,produto.nome AS produto,produto.sku,produto.quantidade,produto.valor,estante.nome AS estante,produto.coluna,produto.linha,categoria.nome AS categoria,tipo.nome AS tipo,caracteristica.nome AS caracteristica
                    FROM produto INNER JOIN estante ON estante.cod_estante = produto.cod_estante
                    INNER JOIN categoria ON categoria.cod_categoria = produto.cod_categoria
                    INNER JOIN tipo ON tipo.cod_tipo = produto.cod_tipo
                    INNER JOIN caracteristica ON caracteristica.cod_caracteristica = produto.cod_caracteristica
                    WHERE produto.cod_produto = %s;"""
            valores = (id,)
            
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
    
    def editar_produto(descricao, arquivo_imagem, quantidade, valor, sku, 
                          coluna, linha, cod_estante, cod_categoria, 
                          cod_tipo, cod_caracteristica, cod_produto):
        """
        Cadastra um novo produto no banco de dados.

        Argumentos (13 ao total, mais a data/hora gerada internamente):
        - nome (VARCHAR)
        - descricao (VARCHAR)
        - arquivo_imagem (bytes BLOB): Conteúdo binário da imagem.
        - quantidade (INT)
        - valor (FLOAT)
        - sku (VARCHAR)
        - coluna (VARCHAR)
        - linha (VARCHAR)
        - cod_estante (INT)
        - cod_categoria (INT)
        - cod_tipo (INT)
        - cod_caracteristica (INT)
        - user_cpf (VARCHAR)

        Retorna:
        - (True, cod_produto_inserido) se o cadastro for bem-sucedido.
        - (False, mensagem_de_erro) em caso de falha.
        """
        conexao = None
        cursor = None
        

        try:
            # 2. CONEXÃO
            conexao = Conection.create_connection()
            if not conexao:
                return False, "Falha na conexão com o banco de dados."

            cursor = conexao.cursor()

            # 3. COMANDO SQL: Inclui TODAS as 14 colunas da tabela 'produto'
            sql = """
            UPDATE produto SET descricao=%s, imagem=%s, quantidade=%s, valor=%s, sku=%s, 
                coluna=%s, linha=%s, cod_estante=%s, cod_categoria=%s, cod_tipo=%s, cod_caracteristica=%s
                WHERE cod_produto=%s
            """
            
            # 4. VALORES: Ordem deve ser EXATA à do SQL
            valores = (
                descricao, 
                arquivo_imagem, 
                quantidade, 
                valor, 
                sku, 
                coluna, 
                linha,   # CPF do usuário (Chave estrangeira)
                cod_estante,
                cod_categoria, 
                cod_tipo, 
                cod_caracteristica,
                cod_produto
            )

            # 5. EXECUÇÃO
            cursor.execute(sql, valores)
            conexao.commit()
            
            produto_id = cursor.lastrowid
            print(f"Produto alterado com sucesso. ID: {produto_id}")
            
            # MUDANÇA: Retorna True e o ID do novo produto
            return True, produto_id

        except Error as e:
            # Captura erros de banco de dados
            if conexao: conexao.rollback()
            print(f"Erro ao cadastrar produto (SQL/DB): {e}")
            return False, f"Erro no banco de dados: {e}"

        except Exception as e:
            # Captura outros erros
            print(f"Erro inesperado no processo de cadastro: {e}")
            return False, f"Erro inesperado: {e}"

        finally:
            # GARANTIA DE LIMPEZA DE RECURSOS
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()