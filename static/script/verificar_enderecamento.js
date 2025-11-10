document.addEventListener('DOMContentLoaded', () => {
    const estanteSelect = document.getElementById('nomeEstanteSelect');
    const colunaSelect = document.getElementById('colunaEstanteSelect');
    const linhaSelect = document.getElementById('linhaEstanteSelect');
    const cod_produto = window.location.href.split('/').slice(-1)[0];
    const estanteInicial = estanteSelect.value;
    
    estanteSelect.addEventListener('input',()=>{
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
                        <option class="select-coluna">10</option>`;

        linhaSelect.innerHTML= `<option class="select-linha" disabled selected>Selecione uma Linha:</option>

                        <option class="select-coluna">1</option>
                        <option class="select-coluna">2</option>
                        <option class="select-coluna">3</option>`;
    })
    colunaSelect.addEventListener('input',async ()=>{
        if(estanteSelect.value == estanteInicial){
            try {
                const url = "/api/get/enderecamento/"+estanteSelect.value;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if(data){
                    let options = linhaSelect.querySelectorAll('option');
                    options.forEach((option,i)=>{
                        if(i){
                            let display="block";
                            for(let ii=0;ii<data.length;ii++){
                                if(data[ii][2]==cod_produto){
                                    data.splice(ii,1);
                                } else if(i==data[ii][1] && colunaSelect.value == data[ii][0]){
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
        }else{
            try {
                const url = "/api/get/enderecamento/"+estanteSelect.value;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if(data){
                    let options = linhaSelect.querySelectorAll('option');
                    options.forEach((option,i)=>{
                        if(i){
                            let display="block";
                            for(let ii=0;ii<data.length;ii++){
                                if(i==data[ii][1] && colunaSelect.value == data[ii][0]){
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
       if(estanteSelect.value == estanteInicial){
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
                                if(data[ii][2]==cod_produto){
                                    console.log(data);
                                    data.splice(ii,1);
                                    console.log(data);
                                } else if(i==data[ii][0] && linhaSelect.value == data[ii][1]){
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
        }else{
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
    })

    // 1. MAPEAMENTO DOS ELEMENTOS
    // Seleciona os elementos do DOM cruciais para a interação.
    // O 'tipoSelect' é o dropdown que dispara a ação.
    const tipoSelect = document.querySelector('#tipoSelect');
    // O 'checkboxCaracteristicas' é o container <div> onde o novo
    // HTML dos checkboxes será injetado.
    const checkboxCaracteristicas = document.querySelector('.checkbox-caracteristicas');

    const actionUrl = document.querySelector('form').getAttribute('action');

    // Extrai o cod_produto da URL usando regex
    const codProduto = actionUrl.match(/\/post\/editar\/produto\/(\d+)/)[1];

    console.log(codProduto);

    async function alteracao_caracteristicas(){
        
        // Variável que irá acumular o HTML gerado dinamicamente.
        let checkboxes = '<label class="label-caracteristicas">Característica(s)</label>';

        // --- Requisição Assíncrona ---
        // 1. Chama a função 'requisicao_filtros' passando o valor atual do select.
        // 2. O 'await' pausa a execução DESTA FUNÇÃO até que a Promise
        //    (a requisição fetch) seja resolvida e retorne os dados.
        let novasCaracteristicas = await requisicao_filtros(tipoSelect.value);

        // --- Construção do HTML ---
        // Itera sobre o array de dados (JSON) retornado pela API.
        // (Assume-se que se 'novasCaracteristicas' for 'undefined' por um erro,
        // o .forEach simplesmente não rodará, resultando em 'checkboxes' vazio).
        novasCaracteristicas.forEach(caracteristica => {
            let check = false

            if(caracteristica.cod_produtos){
                caracteristica.cod_produtos.forEach(produto=>{
                    if (produto==codProduto){
                        check=true
                    }
                });
            }
            
            // Concatena o HTML de cada checkbox na variável acumuladora.
            // Template literals (crases ``) são usados para interpolar
            // as variáveis 'cod_caracteristica' e 'nome_caracteristica' facilmente.
            checkboxes += `<div class="form-check">
                             <input class="form-check-input" type="checkbox" name="cadastro-caracteristicas"
                                 value="${caracteristica.cod_caracteristica}"
                                 id="caracteristica-${caracteristica.cod_caracteristica}" ${check? 'checked':''}>
            
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
    }

    alteracao_caracteristicas();

    // 2. ADIÇÃO DO LISTENER (Escutador de Evento)
    // O evento 'input' é usado para uma resposta imediata (diferente de 'change',
    // que só dispara ao perder o foco).
    // A função do listener é 'async' para permitir o uso de 'await' na requisição.
    tipoSelect.addEventListener('input',alteracao_caracteristicas);

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
