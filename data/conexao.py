import mysql.connector
from mysql.connector import Error

class Conection:

    # Definimos as credenciais para o banco de dados local.
    # Essas variáveis de classe são usadas para manter a configuração de forma organizada.
    _HOST = 'localhost'
    _DATABASE = 'tcc_logistica'
    _USER = 'root'
    _PASSWORD = 'root'
    _PORT = 3306
    
    # "Descomente" o código a baix e comente o código a cima para trocar entre banco de dados online e local
    
    # _HOST = 'lucas-mysql-service-ds-aluno-d374.i.aivencloud.com' 
    # _DATABASE = 'tcc_logistica'   
    # _USER = 'avnadmin'            
    # _PASSWORD = 'AVNS_YoiuI6G-rpT4G7mGW3A'   
    # _PORT = 28179                 

    @staticmethod
    def create_connection():

        """
        Cria uma conexão com o banco de dados MySQL.

        A função tenta se conectar ao banco de dados usando as credenciais
        locais por padrão. Se o parâmetro 'is_online' for definido como True,
        ela usará as credenciais do banco de dados online.

        Retorna o objeto de conexão se a conexão for bem-sucedida,
        ou None em caso de falha.
        """

        try:

            # Tenta estabelecer a conexão com o servidor MySQL
            conn = mysql.connector.connect(

                host=Conection._HOST,
                database=Conection._DATABASE,
                user=Conection._USER,
                password=Conection._PASSWORD,
                port=Conection._PORT
                
            )
            
            # Verifica se a conexão foi estabelecida com sucesso
            if conn.is_connected():
                print("Conexão bem-sucedida ao banco de dados!")
                return conn
                
        except Error as e:
            # Captura e exibe qualquer erro de conexão
            print(f"Erro ao conectar ao MySQL: {e}")
            
        # Retorna None se a conexão não puder ser estabelecida por qualquer motivo
        return None