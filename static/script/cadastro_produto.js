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

    // 1. MAPEAMENTO DOS ELEMENTOS
    // Seleciona os elementos do DOM cruciais para a interação.
    // O 'tipoSelect' é o dropdown que dispara a ação.
    const tipoSelect = document.querySelector('#tipoSelect');
    // O 'checkboxCaracteristicas' é o container <div> onde o novo
    // HTML dos checkboxes será injetado.
    const checkboxCaracteristicas = document.querySelector('.checkbox-caracteristicas');

    // 2. ADIÇÃO DO LISTENER (Escutador de Evento)
    // O evento 'input' é usado para uma resposta imediata (diferente de 'change',
    // que só dispara ao perder o foco).
    // A função do listener é 'async' para permitir o uso de 'await' na requisição.
    tipoSelect.addEventListener('input', async (e) => {
        
        // Variável que irá acumular o HTML gerado dinamicamente.
        let checkboxes = '';

        // --- Requisição Assíncrona ---
        // 1. Chama a função 'requisicao_filtros' passando o valor atual do select.
        // 2. O 'await' pausa a execução DESTA FUNÇÃO até que a Promise
        //    (a requisição fetch) seja resolvida e retorne os dados.
        let novasCaracteristicas = await requisicao_filtros(e.target.value);

        // --- Construção do HTML ---
        // Itera sobre o array de dados (JSON) retornado pela API.
        // (Assume-se que se 'novasCaracteristicas' for 'undefined' por um erro,
        // o .forEach simplesmente não rodará, resultando em 'checkboxes' vazio).
        novasCaracteristicas.forEach(caracteristica => {
            
            // Concatena o HTML de cada checkbox na variável acumuladora.
            // Template literals (crases ``) são usados para interpolar
            // as variáveis 'cod_caracteristica' e 'nome_caracteristica' facilmente.
            checkboxes += `<div class="form-check">
                             <input class="form-check-input" type="checkbox" name="cadastro-caracteristicas"
                                 value="${caracteristica.cod_caracteristica}"
                                 id="caracteristica-${caracteristica.cod_caracteristica}">
            
                             <label class="form-check-label" for="caracteristica-${caracteristica.cod_caracteristica}">
                                 ${caracteristica.nome_caracteristica}
                             </label>
                         </div>`;
        });

        // --- Injeção no DOM ---
        // Substitui o conteúdo HTML do container <div> pela string HTML
        // que acabamos de construir. Isso limpa os checkboxes antigos e
        // insere os novos.
        checkboxCaracteristicas.innerHTML = checkboxes;
    });

    // =========================================================================
    // FUNÇÃO HELPER: REQUISIÇÃO AJAX (Fetch API)
    // Objetivo: Encapsular a lógica de busca de dados (fetch) na API
    //           de forma assíncrona e reutilizável.
    // =========================================================================

    // Função declarada como 'async' para usar 'await' e retornar uma Promise
    // implicitamente.
    async function requisicao_filtros(tipo) {
        // Bloco 'try...catch' é essencial em 'async/await' para capturar
        // erros de rede (fetch) ou erros de resposta (response.ok).
        try {
            // Constrói a URL do endpoint da API dinamicamente.
            const url = "/api/get/caracteristicas/" + tipo;
            
            // Aguarda a requisição de rede (headers e status).
            const response = await fetch(url);
            
            // --- Validação da Resposta HTTP ---
            // Verifica se o status HTTP está fora da faixa 2xx (sucesso).
            if (!response.ok) {
                // Lança um erro explícito que será pego pelo bloco 'catch'.
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Aguarda o 'body' da resposta ser lido e parseado como JSON.
            const data = await response.json();
            
            // Retorna os dados (o array de características) para quem chamou (o listener).
            return data;

        } catch (erro) {
            // Captura falhas de rede (e.g., offline) ou o erro lançado (response.ok).
            console.error("Erro ao obter dados:", erro);
            // A função implicitamente retorna 'undefined' se um erro for pego.
        }
    }
});
    //selects relacionados ao endereçamento
    const estanteSelect = document.getElementById('nomeEstanteSelect');
    const colunaSelect = document.getElementById('colunaEstanteSelect');
    const linhaSelect = document.getElementById('linhaEstanteSelect');
    
    //quando mudar a estante
    estanteSelect.addEventListener('input',()=>{
        //reseta as colunas e linhas

        colunaSelect.innerHTML= `<option class="select-coluna" disabled selected>Selecione uma Coluna:</option>

                        <option class="select-coluna">1</option>
                        <option class="select-coluna">2</option>
                        <option class="select-coluna">3</option>
                        <option class="select-coluna">4</option>
                        <option class="select-coluna">5</option>
                        <option class="select-coluna">6</option>
                        <option class="select-coluna">7</option>
                        <option class="select-coluna">8</option>
                        <option class="select-coluna">9</option>
                        <option class="select-coluna">10</option>`

        linhaSelect.innerHTML= `<option class="select-linha" disabled selected>Selecione uma Linha:</option>

                        <option class="select-coluna">1</option>
                        <option class="select-coluna">2</option>
                        <option class="select-coluna">3</option>`
    })

    colunaSelect.addEventListener('input',async ()=>{
    //quando mudar a coluna e houver estante selecionada
        if(estanteSelect.value){
            try {
                //requisição na api
                const url = "/api/get/enderecamento/"+estanteSelect.value;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                //lista com [[coluna,linha,codigo]]
                const data = await response.json();
                if(data){
                    //busca os selects da linha, que serão alteradas
                    let options = linhaSelect.querySelectorAll('option');
                    options.forEach((option,i)=>{
                        //roda em todos os options depois do primeiro
                        if(i){
                            let display="block";
                            for(let ii=0;ii<data.length;ii++){
                                if(i==data[ii][1] && colunaSelect.value == data[ii][0]){
                                    //se o option for de uma linha que ja tenha produto desta coluna ela não aparece
                                    display = "none";
                                }
                            }
                            option.style.display = display;
                        }
                    })
                }
            } catch (erro) {
                console.error("Erro ao obter dados:", erro);
            }
        }
    });

    linhaSelect.addEventListener('input',async ()=>{
    //quando mudar a coluna e houver estante selecionada
       if(estanteSelect.value){
            try {
                const url = "/api/get/enderecamento/"+estanteSelect.value;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if(data){
                    let options = colunaSelect.querySelectorAll('option');
                    options.forEach((option,i)=>{
                        if(i){
                            let display="block";
                            for(let ii=0;ii<data.length;ii++){
                                if(i==data[ii][0] && linhaSelect.value == data[ii][1]){
                                    display = "none";
                                }
                            }
                            option.style.display = display;
                        }
                    })
                }
            } catch (erro) {
                console.error("Erro ao obter dados:", erro);
            }
        }
    });
