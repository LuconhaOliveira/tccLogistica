// Aplica uma máscara de formatação de CPF (000.000.000-00) ao elemento com o ID 'exampleInputCPF'.
// O parâmetro '{reverse: true}' garante que a máscara funcione corretamente para números digitados da direita para a esquerda (útil em alguns casos, embora menos comum para CPF).
$('#exampleInputCPF').mask('000.000.000-00', {reverse: true});


// 1. Pega o formulário de login pelo seu ID
const loginForm = document.getElementById('loginForm');

// 2. Adiciona um 'ouvinte' para quando o formulário for enviado (evento 'submit')
loginForm.addEventListener('submit', function(event) {

    // Previne o comportamento padrão do navegador de enviar o formulário e recarregar a página (comportamento síncrono).
    // Isso é essencial para que o envio seja feito via AJAX (assíncrono).
    event.preventDefault(); 
    
    // 3. Coleta todos os dados (campos) do formulário 'loginForm' em um objeto 'FormData'.
    const formData = new FormData(loginForm);

    // 4. Envia os dados para a URL de ação do formulário (rota do Flask) usando a API fetch (AJAX)
    fetch(loginForm.action, {
        method: 'POST', // Define o método de envio como POST
        body: formData  // O corpo da requisição são os dados coletados
    })
    .then(response => {
        // Primeiro 'then': Recebe a resposta HTTP completa do servidor.
        // O Flask retorna um JSON, então o lemos aqui (response.json()).
        // Retorna o status HTTP junto com os dados JSON para o próximo 'then'.
        return response.json().then(data => ({
            status: response.status,
            data: data
        }));
    })
    .then(({ status, data }) => {
        
        // 5. Segundo 'then': Processa a resposta final do servidor (status e dados JSON).
        if (status === 200) {
            // Login de SUCESSO (Status 200 OK)
            // Exibe um alerta de sucesso usando a biblioteca SweetAlert2 (Swal.fire).
            Swal.fire({
                title: 'Sucesso!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'Continuar'
            }).then((result) => {
                // Após o usuário clicar em "Continuar" no alerta...
                if (result.isConfirmed) {
                    // Redireciona o navegador para a página principal (rota definida no Flask).
                    window.location.href = "/pagina/principal";
                }
            });
        } else {
            // Login de ERRO (Status 401 Unauthorized, conforme definido no Flask)
            // Exibe um alerta de erro (SweetAlert2).
            Swal.fire({
                title: 'Erro!',
                text: data.message,
                icon: 'error',
                confirmButtonText: 'Tentar Novamente'
            }).then((result) => {
                // Após o usuário clicar em "Tentar Novamente"...
                if (result.isConfirmed) {
                    // Limpa o campo de senha (assumindo o ID 'exampleInputPassword1') para nova tentativa.
                    document.getElementById('exampleInputPassword1').value = ''; 
                }
            });
        }
    })
    .catch(error => {
        // Bloco 'catch': Trata erros de rede ou falhas na requisição (ex: servidor fora do ar).
        console.error('Erro de rede ou processamento:', error);
        // Exibe um alerta genérico de falha de comunicação.
        Swal.fire({
            title: 'Ops!',
            text: 'Ocorreu um erro inesperado. Tente novamente.',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    });
});