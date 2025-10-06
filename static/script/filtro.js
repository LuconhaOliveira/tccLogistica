async function requisicao_filtros(filtro){
    filtro?filtro='/'+filtro:filtro='';
    try {
        const url = "/filtro"+filtro;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (erro) {
        console.error("Erro ao obter dados:", erro);
    }
} 

function alterar_estantes(estantes){
    let html = '';

    estantes.forEach(estante => {
        html += `<div>
            <a href="/estante/${estante.enderecamento}">${estante.enderecamento}</a>
                <ul>
                    <li>${estante.estante}</li>
                    <li>${estante.categoria}</li>
                </ul>
            </div>`
    });


    document.querySelector('#estantes').innerHTML = '';
    document.querySelector('#estantes').innerHTML = html;
}


async function alteracao_front(button) {
    let button_id=button.target.id;
    if(!button.target.checked)button_id='';
    let json = await requisicao_filtros(button_id)
    let estantes = json.estantes;

    alterar_estantes(estantes);
};

function alterar_filtros(filtros){    
    let checkbox = '';

    filtros.forEach(filtro => {
        checkbox += `<input type="checkbox" id=${filtro} name="filtro" value=${filtro}>
                <label for=${filtro}>${filtro}</label><br>`;
    });

    document.querySelector('#filtros').innerHTML = '';
    document.querySelector('#filtros').innerHTML = checkbox;
    document.querySelector('#filtros').addEventListener('input',(e)=>alteracao_front(e));
}

document.addEventListener('DOMContentLoaded',async ()=>{
    let estantesFiltros = await requisicao_filtros('');
    let estantes = estantesFiltros.estantes;
    let filtros = estantesFiltros.filtros;

    alterar_estantes(estantes);
    alterar_filtros(filtros);
});

//TODO: alteração de checkbox para radio e botão de limpeza de filtros