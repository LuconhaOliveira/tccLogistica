function exibirAlerta(titulo, mensagem, icone) {
    Swal.fire({
        title: titulo,
        text: mensagem,
        icon: icone, // 'success', 'error', 'warning', 'info', 'question'
        confirmButtonText: 'Ok'
    });
}

// Função principal do AJAX/Fetch
async function handleCadastroEstante(event) {
    // 1. Impede a submissão tradicional do formulário
    event.preventDefault(); 

    const form = event.target;
    
    // 2. Coleta dados CONSISTENTEMENTE do FormData
    const formData = new FormData(form);
    const nome = formData.get('nome');
    const codCategoria = formData.get('cod_categoria');


    // 3. Validação simples no frontend
    if (!nome || !codCategoria || codCategoria === "") {
        exibirAlerta("Preenchimento Necessário", "Preencha o Nome e selecione a Categoria da estante.", 'warning');
        return; 
    }

    try {
        // 4. Faz a requisição assíncrona
        const response = await fetch('/post/cadastro_estante/adicionar', {
            method: 'POST',
            body: formData 
        });
        
        // 5. Verifica se houve falha no nível HTTP (4xx ou 5xx)
        if (!response.ok) {
            // Tenta ler o JSON de erro (400, 401, 500)
            const data = await response.json();
            
            // Lógica de 401 (Sessão Expirada)
            if (response.status === 401 && data.redirect) {
                exibirAlerta(data.titulo, data.mensagem, 'error');
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 2000);
                return;
            }
            
            // Trata 400 e 500 (Erro no Banco de Dados, Campos Vazios, etc.)
            exibirAlerta(data.titulo || 'Erro HTTP', data.mensagem || `Erro de Servidor: Status ${response.status}`, 'error');
            return; 
        }

        // 6. Processa o Sucesso (Status 2xx, ou seja, response.ok é TRUE)
        const data = await response.json();
        
        // Verifica a chave "status" dentro do JSON (agora padronizada para "success")
        if (data.status === "success") { 
            
            // --- SUCESSO VÁLIDO ---
            exibirAlerta(data.titulo, data.mensagem, 'success');
            
            // Redireciona para a página principal após o sucesso
            setTimeout(() => {
                window.location.href = '/pagina/principal'; 
            }, 1500); 

        } else { 
            // Caso o Flask retorne 200/201, mas o status JSON seja 'error'
            exibirAlerta(data.titulo || 'Erro Desconhecido', data.mensagem || 'Falha ao processar a requisição.', 'error');
        }

    } catch (error) {
        // Erro de rede ou falha na leitura do JSON de resposta
        console.error('Erro na requisição de cadastro de estante:', error);
        exibirAlerta('Erro de Conexão', 'Não foi possível conectar ao servidor. Tente novamente.', 'error');
    }
}

// 7. ANEXAR A FUNÇÃO AO FORMULÁRIO (Certifique-se que o ID está correto)
const formEstante = document.getElementById('form-cadastro-estante'); // Use o ID do seu formulário
if (formEstante) {
        formEstante.addEventListener('submit', handleCadastroEstante);
}