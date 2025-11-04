// =========================================================================
// FUNÇÕES ESSENCIAIS: MÁSCARA E ENVIO AJAX COM TEMPO MÍNIMO (Cadastro Produto)
// Objetivo: Implementar a submissão assíncrona do formulário com feedback visual
//           e otimização da User Experience (UX) para requisições rápidas.
// =========================================================================

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. CÓDIGO DA MÁSCARA (usando jQuery)
    // Aplica a máscara de dinheiro (R$) no campo com id="exampleInputValor".
    // A opção 'reverse: true' é crucial para moedas, garantindo que a digitação
    // comece da direita para a esquerda, tratando corretamente os centavos.
    $(document).ready(function(){
        $('#exampleInputValor').mask('000.000.000,00', {
            reverse: true, 
            placeholder: "0,00" 
        });
    });

    // Variável que define o PISO de tempo em milissegundos para o alerta de carregamento.
    // Essencial para evitar o "pisca-pisca" (flash) em requisições de latência muito baixa.
    const MIN_LOAD_TIME = 1000; 


    // Lógica de envio AJAX (SweetAlert)
    const cadastroProdutoForm = document.getElementById('cadastroProdutoForm');
    if (cadastroProdutoForm) {
        cadastroProdutoForm.addEventListener('submit', function(event) {
            // Intercepta a submissão e previne o recarregamento síncrono da página.
            event.preventDefault(); 
            
            // O objeto FormData captura de forma nativa e eficiente todos os campos 
            // do formulário (incluindo o campo <select multiple>), preparando-os para o POST.
            const formData = new FormData(cadastroProdutoForm);
            
            // Marca o tempo exato de início da requisição.
            const startTime = Date.now(); 

            // Exibe o alerta de carregamento e bloqueia a interface.
            Swal.fire({
                title: 'Processando...',
                text: 'Aguarde, cadastrando produto.',
                allowOutsideClick: false, // Força a espera do usuário
                didOpen: () => {
                    Swal.showLoading() // Exibe o ícone de spinner
                }
            });

            // Inicia a requisição assíncrona (Fetch API).
            fetch(cadastroProdutoForm.action, {
                method: 'POST', 
                body: formData 
            })
            .then(response => {
                
                // LÓGICA DO TEMPO MÍNIMO (PISO) DE CARREGAMENTO
                // Calcula o tempo real que a requisição levou até a resposta chegar.
                const elapsedTime = Date.now() - startTime; 
                
                // Calcula o tempo que ainda deve esperar (o máximo é 0 se a requisição foi lenta).
                const remainingTime = Math.max(0, MIN_LOAD_TIME - elapsedTime);

                // Retorna uma nova Promise para forçar o atraso no pipeline de Promises.
                // O fechamento do loader e a continuação do código só ocorrem após o 'remainingTime'.
                return new Promise(resolve => {
                    setTimeout(() => {
                        Swal.close(); // Fecha o alerta de carregamento APÓS o tempo mínimo.
                        resolve(response); // Passa o objeto response para o próximo .then.
                    }, remainingTime);
                });
            })
            .then(response => {
                // --- Tratamento da Resposta HTTP ---
                // Verifica se o status HTTP está fora da faixa 2xx (e.g., 400, 500).
                if (!response.ok) {
                    // Tenta ler o JSON de erro e lança uma exceção para o bloco .catch.
                    return response.json().then(err => { 
                        throw new Error(err.message || 'Erro desconhecido no servidor.'); 
                    });
                }
                // Se OK (2xx), prossegue para parsear o JSON de dados.
                return response.json(); 
            })
            .then(data => {
                // --- Lógica de Negócio (Sucesso/Erro no JSON) ---
                if (data.status === "success") {
                    // Feedback de Sucesso e redirecionamento para o formulário limpo.
                    Swal.fire({
                        title: 'Sucesso!',
                        text: `${data.message}`, 
                        icon: 'success',
                        timer: 1500, // Tempo de exibição
                        timerProgressBar: true, 
                        showConfirmButton: false, 
                    }).then(() => { 
                        // Redireciona para recarregar o formulário (limpo)
                        window.location.href = "/cadastrar/produto"; 
                    });
                    
                } else {
                    // Feedback de Erro de Lógica (e.g., validação de dados no backend).
                    Swal.fire({
                        title: 'Erro no Cadastro!',
                        text: data.message, 
                        icon: 'error',
                        confirmButtonText: 'Tentar Novamente'
                    });
                }
            })
            .catch(error => {
                // --- Tratamento de Falhas Críticas (Rede, JSON Inválido, Erros Lançados) ---
                console.error('Erro de comunicação ou validação:', error);
                
                // Garante que o alerta de carregamento feche em caso de falha de rede total.
                Swal.close(); 
                
                Swal.fire({
                    title: 'Ops!',
                    text: `Ocorreu um erro: ${error.message || 'Erro inesperado de rede.'}`, 
                    icon: 'warning',
                    confirmButtonText: 'OK'
                });
            });
        });
    }

    const tipoSelect = document.querySelector('#tipoSelect');
    const checkboxCaracteristicas = document.querySelector('.checkbox-caracteristicas');

    tipoSelect.addEventListener('input',async (e)=>{
        let checkboxes = '';

        let novasCaracteristicas = await requisicao_filtros(e.target.value);

        novasCaracteristicas.forEach(caracteristica=>{
            checkboxes+=`<div class="form-check">
                            <input class="form-check-input" type="checkbox" name="cadastro-caracteristicas"
                                value="${caracteristica.cod_caracteristica}"
                                id="caracteristica-${caracteristica.cod_caracteristica}">
                
                            <label class="form-check-label" for="caracteristica-${caracteristica.cod_caracteristica}">
                                ${caracteristica.nome_caracteristica}
                            </label>
                        </div>`
        });

        checkboxCaracteristicas.innerHTML=checkboxes;
    });


});

async function requisicao_filtros(tipo){
    try {
        const url = "/api/get/caracteristicas/"+tipo;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (erro) {
        console.error("Erro ao obter dados:", erro);
    }
} 