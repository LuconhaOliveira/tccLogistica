// Atribui a máscara de CPF ao campo
$('#exampleInputCPF').mask('000.000.000-00', {reverse: true});

// 1. Pega o formulário de cadastro pelo seu ID
// A seleção por ID ('senhaForm') garante uma referência direta e eficiente ao elemento DOM.
const senhaForm = document.getElementById('senhaForm');

// 2. Adiciona um 'ouvinte' para o evento 'submit' do formulário
// Esta é a técnica padrão e recomendada para interceptar a submissão de formulários.
senhaForm.addEventListener('submit', function(event) {

    // Previne o comportamento padrão do navegador (envio síncrono e recarregamento da página).
    // Esta ação é fundamental para permitir a submissão assíncrona via AJAX/Fetch,
    // garantindo uma User Experience (UX) mais fluida.
    event.preventDefault(); 
    
    // 3. Coleta os dados do formulário
    // 'FormData' encapsula automaticamente todos os campos de entrada e seus valores,
    // preparando-os no formato 'multipart/form-data', que o Flask espera receber.
    const formData = new FormData(senhaForm);

    console.log(formData);

    // 4. Inicia a requisição assíncrona (AJAX) usando a API 'fetch()'.
    // Os dados são enviados para a rota de ação definida no atributo 'action' do formulário.
    fetch(senhaForm.action, {
        method: 'POST', // Define o método HTTP para inserção de dados.
        body: formData  // O corpo da requisição contém os dados do formulário.
    })
    .then(async response => {
        // Primeiro bloco 'then': Trata a resposta HTTP inicial.
        // O status HTTP (200, 400, 500) é capturado, e o corpo da resposta é parseado como JSON.
        const data = await response.json();
        return ({
            status: response.status,
            data: data
        });
    })
    .then(({ status, data }) => {
        // 5. Segundo bloco 'then': Processa a resposta final do Flask (status e dados JSON).
        // A lógica de interface (UI) é definida com base no código de status retornado.
        if (status === 200) {
            // Cadastro de SUCESSO (Status 200 OK)
            // Exibe um alerta AUTOMÁTICO com a mensagem de sucesso e redirecionamento.
            Swal.fire({
                title: 'Sucesso!',
                // Informa o usuário sobre o redirecionamento automático
                text: `${data.message}! Redirecionando para o login.`, 
                icon: 'success',
                // --- Configurações para Alerta Automático ---
                timer: 3000,           // Define o tempo do timer (3 segundos)
                timerProgressBar: true, // Mostra a barra de progresso
                showConfirmButton: false, // Não mostra o botão de confirmação manual
                // ---------------------------------------------
            }).then(() => {
                // O bloco 'then' é executado quando o alerta é fechado (pelo timer ou manual).
                // Redireciona AUTOMATICAMENTE para a tela de login
                window.location.href = "/"; // Sua rota de login
            });
        } else {
            // ERRO (Status 400, 401, 500, etc.)
            // Exibe um alerta de erro, utilizando a mensagem de erro detalhada fornecida pelo servidor Flask.
            Swal.fire({
                title: 'Erro no Cadastro!',
                text: data.message,
                icon: 'error',
                confirmButtonText: 'Tentar Novamente'
            });
            // O campo de senha é limpo
            document.getElementById('exampleInputPassword1').value = ''; 
        }
    })
    .catch(error => {
        // Bloco 'catch': Trata falhas de rede ou erros inesperados na execução do JavaScript.
        // Garante que o usuário receba feedback visual mesmo em caso de falha de comunicação completa.
        console.error('Erro de rede ou processamento:', error);
        Swal.fire({
            title: 'Ops!',
            text: 'Ocorreu um erro de comunicação. Tente novamente.',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    });
});