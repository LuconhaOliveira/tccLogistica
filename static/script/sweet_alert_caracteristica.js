document.addEventListener('DOMContentLoaded', function() {
    
    // =========================================================================
    // 1. Lógica para Exclusão (SweetAlert de Confirmação)
    // =========================================================================
    
    // Função genérica para exibir o SweetAlert de confirmação
    function handleExclusao(e, title, text) {
        // Impede a navegação imediata do link
        e.preventDefault();

        // Armazena a URL de exclusão do atributo href do link clicado
        const deleteUrl = e.currentTarget.href;

        // Exibe o SweetAlert de confirmação
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6', // Vermelho para a exclusão
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sim, Excluir!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                // Se confirmado, redireciona para a URL de exclusão, acionando a rota Flask
                window.location.href = deleteUrl;
            }
        });
    }

    // --- Categoria ---
    const linksCategoria = document.querySelectorAll('.link--excluir-categoria');
    linksCategoria.forEach(link => {
        link.addEventListener('click', function(e) {
            handleExclusao(
                e, 
                'Excluir Categoria?', 
                "Esta categoria só será excluída caso nenhum tipo ou característica esteja associado a ela. Esta ação é irreversível"
            );
        });
    });

    // --- Tipo ---
    const linksTipo = document.querySelectorAll('.link--excluir-tipo');
    linksTipo.forEach(link => {
        link.addEventListener('click', function(e) {
            handleExclusao(
                e, 
                'Excluir Tipo?', 
                "Este tipo só será excluído caso nenhuma característica esteja associada a ela. Esta ação é irreversível."
            );
        });
    });

    // --- Característica ---
    const linksCaracteristica = document.querySelectorAll('.link--excluir-caracteristica');
    linksCaracteristica.forEach(link => {
        link.addEventListener('click', function(e) {
            handleExclusao(
                e, 
                'Excluir Característica?', 
                "Esta ação removerá permanentemente esta característica. Tem certeza?"
            );
        });
    });


    // =========================================================================
    // 2. Lógica Existente para Cadastro de Característica (Form Submit via AJAX)
    // =========================================================================

    // 1. Pega o formulário de cadastro de característica pelo seu ID
    const caracteristicaForm = document.getElementById('caracteristicaForm');

    // Verifica se o formulário existe na página antes de anexar o ouvinte
    if (caracteristicaForm) {
        
        // 2. Adiciona o 'ouvinte' para o evento 'submit'
        caracteristicaForm.addEventListener('submit', function(event) {

            // *** CRÍTICO: Previne o envio síncrono padrão do formulário ***
            event.preventDefault(); 

            // 3. Coleta os dados do formulário
            const formData = new FormData(caracteristicaForm);

            // 4. Inicia a requisição assíncrona (AJAX)
            fetch(caracteristicaForm.action, {
                method: 'POST', 
                body: formData 
            })
            .then(response => {
                // Trata a resposta HTTP, garantindo que pegamos o JSON interno.
                return response.json().then(data => ({
                    status: response.status,
                    data: data
                }));
            })
            .then(({ status, data }) => {
                // 5. Processa a resposta final do servidor
                
                // SUCESSO: Status HTTP 200 E status JSON 'success'
                if (status === 200 && data.status === "success") {
                    
                    // --- SWEET ALERT AUTOMÁTICO (TIMER) ---
                    Swal.fire({
                        title: data.titulo || 'Sucesso!',
                        text: `${data.mensagem}`, 
                        icon: 'success',
                        timer: 1500,                
                        timerProgressBar: true,     
                        showConfirmButton: false    
                    }).then(() => {
                        // Este bloco é executado quando o timer termina.
                        window.location.reload(); 
                    });

                } else {
                    // ERRO: 4xx, 5xx ou status 'error'
                    
                    Swal.fire({
                        title: 'Falha no Cadastro! 😥',
                        text: data.message || 'Erro desconhecido ao processar a requisição.', 
                        icon: 'error',
                        confirmButtonText: 'Tentar Novamente'
                    });
                }
            })
            .catch(error => {
                // Falhas de rede/conexão
                console.error('Erro de rede ou processamento:', error);
                
                Swal.fire({
                    title: 'Ops! Erro de Comunicação ⚠️',
                    text: 'Não foi possível conectar ao servidor. Tente novamente.', 
                    icon: 'warning',
                    confirmButtonText: 'Entendi'
                });
            });
        });
    }

});