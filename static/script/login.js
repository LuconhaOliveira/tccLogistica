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
        return response.json(); 
    })
    .then(data => {
        
        // 5. Processa a resposta final do servidor (usando o campo 'status' do JSON)
        
        if (data.status === "success") {
            // Bloco de SUCESSO - AGORA COM ALERTA AUTOMÁTICO
            
            Swal.fire({
                title: 'Sucesso!',
                // Mensagem aprimorada para informar sobre o redirecionamento automático
                text: `${data.message}`, 
                icon: 'success',
                // --- Configurações para Alerta Automático ---
                timer: 1000, // Define o tempo do timer (3 segundos)
                timerProgressBar: true, // Mostra a barra de progresso
                showConfirmButton: false, // Esconde o botão de confirmação manual
                // ---------------------------------------------
            }).then(() => { // O then() é executado quando o timer expira ou o alerta é fechado
                // Redireciona o navegador para a página principal AUTOMATICAMENTE
                
                window.location.href = "/principal";
                // window.location.href = "/pagina/cadastrar/categoria";
                // window.location.href = "/cadastrar/produto";
                // window.location.href = "/visualizar/produto/3";
                // window.location.href = "/pagina/cadastro_estante";
            });
            
        } else {
            // Bloco de ERRO (data.status é "error") - Sem alteração
            
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