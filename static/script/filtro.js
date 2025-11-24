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
        html += `<a href="/estante/${estante.cod_estante}"><div><span>${estante.estante}</span></div></a>`
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
        checkbox += `<input class="input-filtro" type="radio" id=${filtro.cod_categoria} name="filtro" value=${filtro.cod_categoria}>
                <label class="label-filtro" for=${filtro.cod_categoria}>${filtro.nome}</label><br />`;
    });

    checkbox+=`<button class="card-section--btnLimparFiltro" type="reset">Limpar Filtro</button>`

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
   
    const map = new Map();

    // Define a chave (o código) e o valor (o objeto).
    // Se a chave 1 já existir, ela só é sobrescrita.
    filtros.forEach(objeto => map.set(objeto.cod_categoria, objeto));

    // O 'map' agora só tem valores únicos por chave
    // Converte os VALORES do Map de volta para um array
    filtros = Array.from(map.values());

    console.log(filtros);

    alterar_estantes(estantes);
    alterar_filtros(filtros);
});

function limpar_filtros(){
    document.querySelectorAll('#filtros input').forEach(input=>input.checked=false);
}
