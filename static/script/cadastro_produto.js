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
                    text: `${data.message} Redirecionando...`, 
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

document.addEventListener('DOMContentLoaded', (event) => {
    // 1. CÓDIGO DA MÁSCARA (usando jQuery)
    // O jQuery só é carregado após o DOM, então colocamos o código de máscara aqui
    
    // A função 'ready' do jQuery garante que o código só é executado após o carregamento completo da página
    $(document).ready(function(){
        // Aplica a máscara de dinheiro (R$) no campo com id="exampleInputValor"
        // '000.000.000,00' é o formato base (pode ser ajustado)
        // {reverse: true} faz com que a digitação comece da direita para a esquerda, ideal para moeda.
        $('#exampleInputValor').mask('000.000.000,00', {
            reverse: true, 
            placeholder: "0,00" // Define o que será exibido no campo vazio
        });
    });


    // 2. CÓDIGO DO SWEETALERT (JÁ REVISADO)
    const fileInput = document.getElementById('exampleInputPhoto');
    const MAX_SIZE_BYTES = 15 * 1024 * 1024; // 16MB
    const MAX_SIZE_MB = MAX_SIZE_BYTES / (1024 * 1024); 

    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0]; 

            if (file && file.size > MAX_SIZE_BYTES) {
                Swal.fire({
                    icon: 'error',
                    title: 'Ops! 😥 Arquivo Muito Grande',
                    text: `O tamanho máximo permitido para a imagem é de ${MAX_SIZE_MB} MB. Por favor, selecione um arquivo menor.`,
                    timer: 3000,
                    showConfirmButton: false
                });
                event.target.value = ''; 
            }
        });
    }
});