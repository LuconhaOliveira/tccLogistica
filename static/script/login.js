// Aplica uma máscara de formatação de CPF (000.000.000-00)
$('#exampleInputCPF').mask('000.000.000-00', {reverse: true});


// 1. Pega o formulário de login pelo seu ID
const loginForm = document.getElementById('loginForm');

// 2. Adiciona um 'ouvinte' para quando o formulário for enviado (evento 'submit')
loginForm.addEventListener('submit', function(event) {

    // Previne o comportamento padrão (envio síncrono da página)
    event.preventDefault(); 
    
    // 3. Coleta todos os dados do formulário
    const formData = new FormData(loginForm);

    // 4. Envia os dados para a URL de ação do formulário (AJAX/fetch)
    fetch(loginForm.action, {
        method: 'POST', 
        body: formData 
    })
    .then(response => {
        // Passo 1: Como o Flask SEMPRE retorna 200, podemos apenas ler o JSON.
        // Não precisamos verificar response.ok, pois o tratamento será feito pelo JSON 'status'.
        return response.json(); 
    })
    .then(data => {
        
        // 5. Processa a resposta final do servidor (usando o campo 'status' do JSON)
        
        if (data.status === "success") {
            // Bloco de SUCESSO
            
            Swal.fire({
                title: 'Sucesso!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'Continuar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redireciona o navegador para a página principal
                    window.location.href = "/pagina/principal";
                }
            });
            
        } else {
            // Bloco de ERRO (data.status é "error")
            
            Swal.fire({
                title: 'Erro!',
                text: data.message, // Usa a mensagem de erro que veio do Flask
                icon: 'error',
                confirmButtonText: 'Tentar Novamente'
            }).then((result) => {
                // Limpa o campo de senha após o clique
                if (result.isConfirmed) {
                    document.getElementById('exampleInputPassword1').value = ''; 
                }
            });
        }
    })
    .catch(error => {
        // Bloco 'catch': Trata APENAS erros de rede ou falhas na leitura do JSON
        
        console.error('Erro de rede ou processamento:', error);
        
        Swal.fire({
            title: 'Ops!',
            // Mensagem genérica, pois ocorreu uma falha de comunicação ou parsing (não erro de login)
            text: 'Ocorreu um erro de comunicação inesperado. Tente novamente.', 
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    });
});