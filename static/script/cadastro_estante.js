// =========================================================================
// FUNÇÕES DE CADASTRO DE ESTANTE COM AJAX, SWEETALERT E TEMPO MÍNIMO
// Objetivo: Submissão assíncrona do formulário para evitar recarregamento de página e
//           garantir uma User Experience (UX) fluida com feedback visual (SweetAlert).
// =========================================================================

document.addEventListener('DOMContentLoaded', (event) => {

    // --- Seleção de Elementos e Constantes ---
    const formEstante = document.getElementById('form-cadastro-estante');
    // Constante que define o piso de tempo de exibição do loader.
    // Essencial para UX: evita o "pisca-pisca" em requisições ultra-rápidas.
    const MIN_LOAD_TIME = 1000; 

    if (formEstante) {

        formEstante.addEventListener('submit', function (event) {
            // Previne o comportamento padrão do navegador (submissão síncrona e reload).
            event.preventDefault();

            // Coleta os dados do formulário de forma eficiente.
            const formData = new FormData(formEstante);
            const nome = formData.get('nome');
            const codCategoria = formData.get('cod_categoria');

            // --- Validação no Frontend (Feedback Imediato) ---
            if (!nome || !codCategoria || codCategoria === "") {
                Swal.fire({
                    title: 'Preenchimento Necessário',
                    text: 'Preencha o Nome e selecione a Categoria da estante.',
                    icon: 'warning',
                    confirmButtonText: 'Ok'
                });
                return; // Interrompe a submissão AJAX
            }

            // Marca o tempo exato de início da requisição para calcular o tempo mínimo.
            const startTime = Date.now(); 

            // 1. Alerta de Carregamento (Bloqueador de UI)
            Swal.fire({
                title: 'Processando Cadastro...',
                text: 'Aguarde, criando estante.',
                allowOutsideClick: false, // Bloqueia interações do usuário durante o processamento
                didOpen: () => {
                    Swal.showLoading(); // Exibe o ícone de carregamento
                }
            });

            // 2. Requisição AJAX (Fetch API)
            fetch(formEstante.action || '/post/cadastrar/estante', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                
                // --- Lógica de Tempo Mínimo (PISO) ---
                const elapsedTime = Date.now() - startTime; 
                // Garante que o remainingTime seja 0 se a requisição for mais lenta que MIN_LOAD_TIME.
                const remainingTime = Math.max(0, MIN_LOAD_TIME - elapsedTime);

                // Utiliza Promise e setTimeout para forçar o loader na tela pelo tempo mínimo.
                // O próximo .then só executa após este atraso.
                return new Promise(resolve => setTimeout(() => resolve(response), remainingTime)); 

            })
            .then(response => { 
                // Este bloco é o primeiro a ser executado APÓS o tempo mínimo de carregamento.
                
                // Fecha o alerta de processamento antes de exibir o resultado (sucesso/erro).
                Swal.close(); 
                
                // --- Tratamento de Erros HTTP (4xx e 5xx) ---
                if (!response.ok) {
                    return response.json().then(data => {
                        
                        // Tratamento específico para Sessão Expirada (401)
                        if (response.status === 401 && data.redirect) {
                            Swal.fire({
                                title: data.titulo || 'Sessão Expirada',
                                text: data.mensagem || 'Por favor, faça login novamente.',
                                icon: 'error',
                                timer: 2000,
                                showConfirmButton: false,
                                timerProgressBar: true
                            }).then(() => {
                                window.location.href = data.redirect; // Redireciona
                            });
                            throw new Error('Sessão expirada'); // Interrompe o fluxo de promises
                        }

                        // Tratamento de outros Erros de Servidor (e.g., 400 Bad Request, 500 Internal Server Error)
                        Swal.fire({
                            title: data.titulo || 'Erro HTTP',
                            text: data.mensagem || `Erro de Servidor: Status ${response.status}`,
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                        throw new Error('Erro HTTP'); // Interrompe o fluxo
                    });
                }

                // Caso 2xx (Sucesso): Retorna o JSON para o próximo .then
                return response.json();
            })
            .then(data => {
                // --- Lógica de Negócio (Sucesso/Falha no JSON) ---
                if (data.status === "success") {
                    // Feedback visual de Sucesso com timer e redirecionamento
                    Swal.fire({
                        title: data.titulo || 'Sucesso!',
                        text: `${data.mensagem}`,
                        icon: 'success',
                        timer: 1500, 
                        timerProgressBar: true,
                        showConfirmButton: false
                    }).then(() => {
                        window.location.href = "/principal"; // Redirecionamento após feedback
                    });

                } else {
                    // Feedback visual de Erro de Lógica (e.g., validação de dados no Flask)
                    Swal.fire({
                        title: data.titulo || 'Erro!',
                        text: data.mensagem || 'Falha ao processar a requisição.',
                        icon: 'error',
                        confirmButtonText: 'Tentar Novamente'
                    });
                }
            })
            .catch(error => {
                // --- Tratamento de Erros Finais (Rede, JSON Inválido) ---
                console.error('Erro na requisição de cadastro de estante:', error);

                // Garante que o alerta de carregamento feche mesmo em falha de rede/promessa.
                Swal.close(); 

                Swal.fire({
                    title: 'Erro de Conexão',
                    text: 'Não foi possível conectar ao servidor. Tente novamente.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
        });
    }
});