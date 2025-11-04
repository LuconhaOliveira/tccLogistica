// =========================================================================
// CÓDIGO JS OTIMIZADO: MÁSCARA, AJAX, SWEETALERT COM TEMPO MÍNIMO
// Objetivo: Submissão assíncrona do formulário de cadastro de usuário com
//           garantia de feedback visual e tratamento robusto de erros HTTP.
// =========================================================================

// Configuração da Máscara (Mantendo jQuery)
$(document).ready(function() {
    // Atribui a máscara de CPF ao campo. A opção 'reverse: true' é útil para formatos
    // numéricos, embora para CPF seja mais didática para usuários que preenchem ao contrário.
    $('#exampleInputCPF').mask('000.000.000-00', {reverse: true});
}); 

// 1. Pega o formulário de cadastro pelo seu ID
const cadastroForm = document.getElementById('cadastroForm');

// Constante que define o PISO de tempo de exibição do loader (em milissegundos).
// Essencial para UX: evita o "pisca-pisca" (flash) em requisições ultra-rápidas.
const MIN_LOAD_TIME = 1000; 

if (cadastroForm) {
    // 2. Adiciona um 'ouvinte' para o evento 'submit' do formulário
    cadastroForm.addEventListener('submit', function(event) {

        // Previne o comportamento padrão do navegador (submissão síncrona e recarregamento).
        event.preventDefault(); 
        
        // 3. Coleta os dados do formulário de forma eficiente (FormData).
        const formData = new FormData(cadastroForm);
        
        // Marca o tempo exato de início da requisição para cálculo do tempo mínimo.
        const startTime = Date.now(); 

        // ADIÇÃO 1: ALERTA DE CARREGAMENTO (Bloqueador de UI)
        Swal.fire({
            title: 'Processando Cadastro...',
            text: 'Aguarde, finalizando registro.',
            allowOutsideClick: false, // Bloqueia interações durante o processamento
            didOpen: () => {
                Swal.showLoading(); // Exibe o ícone de spinner
            }
        });
        
        // 4. Inicia a requisição assíncrona (Fetch API) para a rota de cadastro.
        fetch(cadastroForm.action, {
            method: 'POST', 
            body: formData 
        })
        .then(response => {
            
            // ADIÇÃO 2: LÓGICA DO TEMPO MÍNIMO DE CARREGAMENTO (Garantia de UX)
            const elapsedTime = Date.now() - startTime; 
            // Calcula o tempo restante, garantindo que seja no mínimo 0.
            const remainingTime = Math.max(0, MIN_LOAD_TIME - elapsedTime);

            // Cria uma Promise para forçar o atraso e garantir que o loader permaneça visível.
            return new Promise(resolve => {
                setTimeout(() => {
                    // Após o delay (se houver), fecha o alerta de carregamento.
                    Swal.close(); 
                    resolve(response); // Resolve com o objeto response original para prosseguir.
                }, remainingTime);
            });
        })
        .then(response => {
            // Continua o pipeline: Tenta parsear o corpo da resposta como JSON,
            // encapsulando o status HTTP e os dados em um único objeto.
            return response.json().then(data => ({
                status: response.status,
                data: data
            }));
        })
        .then(({ status, data }) => {
            // 5. Bloco final: Processa a resposta do servidor (código HTTP + dados JSON).
            if (status === 200) {
                // SUCESSO: Feedback visual e redirecionamento automático.
                Swal.fire({
                    title: 'Sucesso!',
                    text: `Redirecionando para o login.`, 
                    icon: 'success',
                    timer: 1000, 
                    timerProgressBar: true, 
                    showConfirmButton: false, 
                }).then(() => {
                    // Redireciona para a tela de login após o término do timer do SweetAlert.
                    window.location.href = "/"; 
                });
            } else {
                // ERRO (Tratamento para 400, 401, 500, etc., conforme retornado pelo Flask).
                Swal.fire({
                    title: 'Erro no Cadastro!',
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'Tentar Novamente'
                });
                // Limpa o campo de senha (medida de segurança e feedback visual).
                document.getElementById('exampleInputPassword1').value = ''; 
            }
        })
        .catch(error => {
            // Bloco 'catch': Trata falhas de rede (e.g., servidor offline, timeout) ou erros lançados.
            console.error('Erro de rede ou processamento:', error);
            
            // Garante que o alerta de carregamento feche em qualquer cenário de falha crítica.
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