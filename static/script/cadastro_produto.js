// 1. Pega o formulário de cadastro de produto pelo seu ID
const cadastroProdutoForm = document.getElementById('cadastroProdutoForm');

// 2. Verifica se o formulário existe na página
if (cadastroProdutoForm) {
    
    // 3. Adiciona o 'ouvinte' para o evento 'submit'
    cadastroProdutoForm.addEventListener('submit', function(event) {

        // ESSENCIAL: Impede que o navegador envie o formulário da maneira tradicional (o que causa a tela preta de JSON)
        event.preventDefault(); 
        
        // 4. Coleta todos os dados, incluindo a imagem
        const formData = new FormData(cadastroProdutoForm);

        // 5. Envio assíncrono via fetch
        fetch(cadastroProdutoForm.action, {
            method: 'POST', 
            body: formData 
        })
        .then(response => {
            // Trata erros de HTTP antes de ler o JSON
            if (!response.ok) {
                // Se o servidor retornar 404, 500 etc.
                throw new Error('Erro de servidor com status: ' + response.status);
            }
            // Retorna o JSON da resposta do Flask
            return response.json(); 
        })
        .then(data => {
            
            // 6. Processa a resposta JSON
            if (data.status === "success") {
                // SUCESSO
                Swal.fire({
                    title: 'Sucesso!',
                    text: `${data.message}! Redirecionando...`, 
                    icon: 'success',
                    timer: 1000, 
                    timerProgressBar: true, 
                    showConfirmButton: false, 
                }).then(() => { 
                    // Redireciona para recarregar o formulário (limpo)
                    window.location.href = "/pagina/principal"; 
                });
                
            } else {
                // ERRO
                Swal.fire({
                    title: 'Erro no Cadastro!',
                    text: data.message, 
                    icon: 'error',
                    confirmButtonText: 'Tentar Novamente'
                });
            }
        })
        .catch(error => {
            // 7. Trata erros de rede ou processamento do JSON
            console.error('Erro de rede ou processamento:', error);
            
            Swal.fire({
                title: 'Ops!',
                text: 'Ocorreu um erro de comunicação inesperado. Tente novamente.', 
                icon: 'warning',
                confirmButtonText: 'OK'
            });
        });
    });
}