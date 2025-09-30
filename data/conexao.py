import mysql.connector
from mysql.connector import Error

class Conection:

    # Definimos as credenciais para o banco de dados local.
    # Essas variáveis de classe são usadas para manter a configuração de forma organizada.
    _LOCAL_HOST = 'localhost'
    _LOCAL_DATABASE = 'tcc_logistica'
    _LOCAL_USER = 'root'
    _LOCAL_PASSWORD = 'root'
    _LOCAL_PORT = 3306
    
    # Definimos as credenciais para o banco de dados online.
    _ONLINE_HOST = 'lucas-mysql-service-ds-aluno-d374.i.aivencloud.com' 
    _ONLINE_DATABASE = 'tcc_logistica'   
    _ONLINE_USER = 'avnadmin'            
    _ONLINE_PASSWORD = 'AVNS_YoiuI6G-rpT4G7mGW3A'   
    _ONLINE_PORT = 28179                 

    @staticmethod
    def create_connection(is_online=False):

        """
        Cria uma conexão com o banco de dados MySQL.

        A função tenta se conectar ao banco de dados usando as credenciais
        locais por padrão. Se o parâmetro 'is_online' for definido como True,
        ela usará as credenciais do banco de dados online.

        Retorna o objeto de conexão se a conexão for bem-sucedida,
        ou None em caso de falha.
        """

        try:

            if is_online:

                # Usa as credenciais online
                host = Conection._ONLINE_HOST
                database = Conection._ONLINE_DATABASE
                user = Conection._ONLINE_USER
                password = Conection._ONLINE_PASSWORD
                port = Conection._ONLINE_PORT

            else:

                # Usa as credenciais locais por padrão
                host = Conection._LOCAL_HOST
                database = Conection._LOCAL_DATABASE
                user = Conection._LOCAL_USER
                password = Conection._LOCAL_PASSWORD
                port = Conection._LOCAL_PORT

            # Tenta estabelecer a conexão com o servidor MySQL
            conn = mysql.connector.connect(

                host=host,
                database=database,
                user=user,
                password=password,
                port=port 
                
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