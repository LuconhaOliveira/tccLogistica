// =========================================================================
// CÓDIGO JS OTIMIZADO: RECUPERAR SENHA COM SWEETALERT E TEMPO MÍNIMO
// Objetivo: Submissão assíncrona da solicitação de recuperação de senha com
//           garantia de feedback visual e gestão do tempo de processamento.
// =========================================================================

// Atribui a máscara de CPF ao campo
$('#exampleInputCPF').mask('000.000.000-00', {reverse: true});

// 1. Pega o formulário de recuperação de senha pelo seu ID
const senhaForm = document.getElementById('senhaForm');

// Constante que define o PISO de tempo de exibição do loader (em milissegundos).
// Essencial para UX, especialmente em processos que podem envolver tempo de envio de e-mail.
const MIN_LOAD_TIME = 1000; 

if (senhaForm) {
    // 2. Adiciona um 'ouvinte' para o evento 'submit' do formulário
    senhaForm.addEventListener('submit', function(event) {

        // Previne o comportamento padrão (reload da página).
        event.preventDefault(); 
        
        // 3. Coleta os dados do formulário de forma eficiente.
        const formData = new FormData(senhaForm);
        
        // Marca o tempo de início da requisição para cálculo do tempo mínimo.
        const startTime = Date.now(); 

        // ADIÇÃO 1: ALERTA DE CARREGAMENTO (Bloqueia UI enquanto espera)
        Swal.fire({
            title: 'Processando...',
            // Mensagem clara para o usuário sobre o que está ocorrendo
            text: 'Aguarde, processando solicitação.',
            allowOutsideClick: false, 
            didOpen: () => {
                Swal.showLoading(); 
            }
        });
        
        // 4. Inicia a requisição assíncrona (Fetch API)
        fetch(senhaForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            
            // ADIÇÃO 2: LÓGICA DO TEMPO MÍNIMO DE CARREGAMENTO
            const elapsedTime = Date.now() - startTime; 
            // Calcula o tempo restante, garantindo que o loader fique pelo menos 1000ms.
            const remainingTime = Math.max(0, MIN_LOAD_TIME - elapsedTime);

            // Usa Promise/setTimeout para atrasar o fechamento do loader.
            return new Promise(resolve => {
                setTimeout(() => {
                    Swal.close(); // Fecha o alerta de carregamento APÓS o tempo mínimo.
                    resolve(response); // Permite que a Promise continue com a resposta.
                }, remainingTime);
            });
        })
        .then(response => {
            // Processa a resposta JSON e encapsula status e dados.
            return response.json().then(data => ({
                status: response.status,
                data: data
            }));
        })
        .then(({ status, data }) => {
            // 5. Bloco final: Processa a resposta (sucesso ou erro HTTP/Lógico)
            if (status === 200) {
                // SUCESSO: Feedback de sucesso e redirecionamento para a tela de login.
                Swal.fire({
                    title: 'Sucesso!',
                    // Utiliza a mensagem do servidor, que provavelmente informa sobre o e-mail enviado.
                    text: `${data.message}`, 
                    icon: 'success',
                    timer: 1000, 
                    timerProgressBar: true, 
                    showConfirmButton: false, 
                }).then(() => {
                    // Redireciona após o feedback visual.
                    window.location.href = "/"; 
                });
            } else {
                // ERRO (Tratamento para 4xx, 5xx ou erro lógico do servidor)
                Swal.fire({
                    title: 'Erro!',
                    text: data.message || 'Falha ao processar a requisição.',
                    icon: 'error',
                    confirmButtonText: 'Tentar Novamente'
                });
                // Limpeza opcional do campo de senha (se o formulário de recuperação incluir senha).
                const passwordField = document.getElementById('exampleInputPassword1');
                if (passwordField) {
                    passwordField.value = '';
                }
            }
        })
        .catch(error => {
            // Bloco 'catch': Trata falhas de rede ou erros na execução do script.
            console.error('Erro de rede ou processamento:', error);
            
            // Garante que o alerta de carregamento feche em qualquer falha de comunicação.
            Swal.close(); 

            Swal.fire({
                title: 'Ops!',
                text: 'Ocorreu um erro de comunicação. Tente novamente.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
        });
    });
}