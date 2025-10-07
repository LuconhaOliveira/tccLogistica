async function requisicao_filtros(filtro){
    filtro?filtro='/'+filtro:filtro='';
    try {
        const url = "/filtro"+filtro;
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

function alterar_estantes(estantes){
    let html = '';

    estantes.forEach(estante => {
        html += `<div>
            <a href="/estante/${estante.cod_estante}">${estante.nome}</a>
                <p>${estante.categoria}</p>
            </div>`
    });


    document.querySelector('#estantes').innerHTML = '';
    document.querySelector('#estantes').innerHTML = html;
}


async function alteracao_front(button) {
    let button_value=button.target.value;
    if(!button.target.checked)button_value='';
    let json = await requisicao_filtros(button_value)
    let estantes = json.estantes;

    alterar_estantes(estantes);
};

function alterar_filtros(filtros){    
    let checkbox = '';

    filtros.forEach(filtro => {
        checkbox += `<input type="radio" id=${filtro.nome} name="estante_filtro" value=${filtro.cod_categoria}>
                <label for=${filtro.nome}>${filtro.nome}</label><br />`;
    });

    checkbox+=`<button type="reset">Limpar filtro</button>`

    document.querySelector('#filtros').innerHTML = '';
    document.querySelector('#filtros').innerHTML = checkbox;
    document.querySelector('#filtros').addEventListener('input',(e)=>alteracao_front(e));
    document.querySelector('#filtros button').addEventListener('click',async(e)=>{
        if(e.target.tagName === 'BUTTON'){
            let json = await requisicao_filtros('')
            let estantes = json.estantes;

            alterar_estantes(estantes);
        }
    });
}

document.addEventListener('DOMContentLoaded',async ()=>{
    let estantesFiltros = await requisicao_filtros('');
    let estantes = estantesFiltros.estantes;
    let filtros = estantesFiltros.filtros;

    alterar_estantes(estantes);
    alterar_filtros(filtros);
});

function limpar_filtros(){
    document.querySelectorAll('#filtros input').forEach(input=>input.checked=false);
}
