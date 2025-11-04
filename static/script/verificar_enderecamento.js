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
});
