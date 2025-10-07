// FUNÇÃO AUXILIAR: Exibe alertas padronizados do SweetAlert2
function exibirAlerta(titulo, mensagem, icone) {
    Swal.fire({
        title: titulo,
        text: mensagem,
        icon: icone, // 'success', 'error', 'warning', 'info', 'question'
        confirmButtonText: 'Ok'
    });
}


async function handleCadastroEstante(event) {
    // 1. Impede a submissão tradicional do formulário (que causaria o redirecionamento)
    event.preventDefault(); 

    const form = event.target;
    
    // Coletando dados pelos IDs dos campos no HTML
    const nome = document.getElementById('estante-nome')?.value;
    const codCategoria = document.getElementById('estante-cod-categoria')?.value;

    // 2. Validação simples no frontend
    if (!nome || !codCategoria || codCategoria === "") {
        exibirAlerta("Preenchimento Necessário", "Preencha o Nome e selecione a Categoria da estante.", 'warning');
        return;
    }

    // 3. Cria FormData para enviar os dados no formato de formulário (compatível com request.form do Flask)
    const formData = new FormData(form);
    
    try {
        // 4. Faz a requisição assíncrona
        const response = await fetch('/post/cadastro_estante/adicionar', {
            method: 'POST',
            body: formData 
        });

        // 5. Tenta ler a resposta JSON
        const data = await response.json();

        if (response.ok) { // Status 200/201 (Sucesso)
            exibirAlerta(data.titulo, data.mensagem, 'success');
            
            // Redireciona para a página principal após o sucesso
             setTimeout(() => {
                 window.location.href = '/pagina/principal'; 
             }, 1500); 

        } else { // Status 400/401/500 (Falha)
            // Usa a mensagem e título retornados pelo Flask
            exibirAlerta(data.titulo, data.mensagem, 'error');
            
            // Lógica de redirecionamento caso a sessão tenha expirado (status 401)
            if (response.status === 401 && data.redirect) {
                setTimeout(() => {
                    window.location.href = data.redirect; // Redireciona para o login
                }, 2000);
            }
        }

    } catch (error) {
        // Erro de rede ou falha na leitura do JSON de resposta
        console.error('Erro na requisição de cadastro de estante:', error);
        exibirAlerta('Erro de Conexão', 'Não foi possível conectar ao servidor.', 'error');
    }
}

// -----------------------------------------------------
// ANEXA O LISTENER AO DOM
// -----------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    // Busca o formulário pelo ID que definimos no HTML
    const estanteForm = document.getElementById('form-cadastro-estante');
    if (estanteForm) {
        // Anexa a função ao evento 'submit'
        estanteForm.addEventListener('submit', handleCadastroEstante);
        console.log("Listener de Cadastro de Estante anexado.");
    }
});
