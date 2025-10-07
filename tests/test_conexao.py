import pytest
from unittest import mock
from data.conexao import Conection

# Teste para conexão local
def test_create_connection_local():
    # mockar a função mysql.connector.connect
    with mock.patch('mysql.connector.connect') as mock_connect:
        # Configura o mock para simular um objeto de conexão
        mock_conn = mock.MagicMock()
        mock_connect.return_value = mock_conn

        # Chama o método create_connection com is_online=False (conexão local)
        conn = Conection.create_connection(is_online=False)

        # Verifica se o connect foi chamado com as credenciais locais
        mock_connect.assert_called_once_with(
            host=Conection._LOCAL_HOST,
            database=Conection._LOCAL_DATABASE,
            user=Conection._LOCAL_USER,
            password=Conection._LOCAL_PASSWORD,
            port=Conection._LOCAL_PORT
        )

        # Verifica se a conexão retornada é a esperada
        assert conn == mock_conn
        # Verifica se a conexão foi realmente "bem-sucedida"
        assert conn.is_connected.called