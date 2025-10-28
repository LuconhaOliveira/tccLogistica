// Atribui a máscara de CPF ao campo
$('#exampleInputCPF').mask('000.000.000-00', {reverse: true});

// 1. Pega o formulário de cadastro pelo seu ID
// A seleção por ID ('cadastroForm') garante uma referência direta e eficiente ao elemento DOM.
const cadastroForm = document.getElementById('cadastroForm');

// 2. Adiciona um 'ouvinte' para o evento 'submit' do formulário
// Esta é a técnica padrão e recomendada para interceptar a submissão de formulários.
cadastroForm.addEventListener('submit', function(event) {

    // Previne o comportamento padrão do navegador (envio síncrono e recarregamento da página).
    event.preventDefault(); 
    
    // 3. Coleta os dados do formulário
    const formData = new FormData(cadastroForm);

    // 4. Inicia a requisição assíncrona (AJAX) usando a API 'fetch()'.
    fetch(cadastroForm.action, {
        method: 'POST', // Define o método HTTP para inserção de dados.
        body: formData  // O corpo da requisição contém os dados do formulário.
    })
    .then(response => {
        return response.json().then(data => ({
            status: response.status,
            data: data
        }));
    })
    .then(({ status, data }) => {
        // 5. Segundo bloco 'then': Processa a resposta final do Flask (status e dados JSON).
        if (status === 200) {
            // Cadastro de SUCESSO (Status 200 OK)
            // Alerta com Auto-Fechamento e Redirecionamento Automático
            Swal.fire({
                title: 'Sucesso!',
                text: `Redirecionando para o login.`, // Informa o usuário
                icon: 'success',
                timer: 1000, // Define o tempo do timer (3 segundos)
                timerProgressBar: true, // Mostra a barra de progresso
                showConfirmButton: false, // Não mostra o botão de confirmação manual
            }).then((result) => {
                // O bloco 'then' é executado quando o alerta é fechado,
                // seja pelo timer (result.dismiss === Swal.DismissReason.timer) 
                // ou manualmente (embora o botão esteja escondido).
                
                // Redireciona para a tela de login
                window.location.href = "/"; // Sua rota de login
            });
        } else {
            // ERRO (Status 400, 401, 500, etc.)
            Swal.fire({
                title: 'Erro no Cadastro!',
                text: data.message,
                icon: 'error',
                confirmButtonText: 'Tentar Novamente'
            });
            // Limpa o campo de senha
            document.getElementById('exampleInputPassword1').value = ''; 
        }
    })
    .catch(error => {
        // Bloco 'catch': Trata falhas de rede ou erros inesperados.
        console.error('Erro de rede ou processamento:', error);
        Swal.fire({
            title: 'Ops!',
            text: 'Ocorreu um erro de comunicação. Tente novamente.',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    });
});