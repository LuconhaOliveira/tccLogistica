from data.conexao import Conection
from mysql.connector import Error 

class ControleProduto:

    @staticmethod
    def cadastrar_produto(cpf, sku, arquivo_imagem, descricao, nome, valor, cod_tipo):
        """
        Cadastra um novo produto no banco de dados lendo os bytes de um objeto de arquivo.

        Argumentos:
        - cpf (VARCHAR): CPF do usuário.
        - sku (VARCHAR): Código SKU.
        - arquivo_imagem (FileStorage): Objeto de arquivo do Flask contendo a imagem.
        - descricao (VARCHAR): Descrição do produto.
        - nome (VARCHAR): Nome do produto.
        - valor (FLOAT): Preço/valor unitário do produto.
        - cod_tipo (INT): Código do tipo de produto (FK para tipo).

        Retorna:
        - True se o cadastro for bem-sucedido, False em caso de falha.
        """
        conexao = None
        cursor = None
        produto_imagem = None 

        try:
            # 1. TRATAMENTO DA IMAGEM
            if arquivo_imagem:
                # O método .read() lê os bytes puros do arquivo de imagem enviado.
                produto_imagem = arquivo_imagem.read()
            
            # 2. CONEXÃO
            conexao = Conection.create_connection()
            if not conexao:
                print("Erro: Não foi possível estabelecer a conexão com o banco de dados.")
                return False

            cursor = conexao.cursor()

            # 3. COMANDO SQL
            sql = """
            INSERT INTO produto (cpf, sku, imagem, descricao, nome, valor, cod_tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (cpf, sku, produto_imagem, descricao, nome, valor, cod_tipo)

            # 4. EXECUÇÃO
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Produto '{nome}' cadastrado com sucesso.")
            return True

        except Error as e:
            # Captura erros de banco de dados (ex: FK inválida, SKU duplicado, etc.)
            print(f"Erro ao cadastrar produto: {e}")
            return False

        except Exception as e:
            # Captura outros erros, como falha ao ler o arquivo
            print(f"Erro inesperado no processo de cadastro: {e}")
            return False

        finally:
            # GARANTIA DE LIMPEZA DE RECURSOS
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
