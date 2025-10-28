// =========================================================================
// FUNÇÕES ESSENCIAIS: MÁSCARA E ENVIO AJAX COM SWEETALERT
// =========================================================================

document.addEventListener('DOMContentLoaded', (event) => {
    
    // 1. CÓDIGO DA MÁSCARA (usando jQuery)
    // Aplica a máscara de dinheiro (R$) no campo com id="exampleInputValor"
    $(document).ready(function(){
        $('#exampleInputValor').mask('000.000.000,00', {
            reverse: true, 
            placeholder: "0,00" 
        });
    });

    // NOTA: Toda a lógica anterior para adicionar/remover características dinamicamente
    // foi removida, pois o HTML agora usa um campo <select multiple> simples.
    // O campo 'cadastro-caracteristicas' é enviado diretamente pelo FormData.


    // Lógica de envio AJAX (SweetAlert)
    const cadastroProdutoForm = document.getElementById('cadastroProdutoForm');
    if (cadastroProdutoForm) {
        cadastroProdutoForm.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            // O FormData captura todos os campos do formulário, 
            // incluindo as múltiplas seleções do <select multiple>
            const formData = new FormData(cadastroProdutoForm);

            // Exibe um alerta de carregamento enquanto aguarda a resposta
            Swal.fire({
                title: 'Processando...',
                text: 'Aguarde o cadastro do produto.',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading()
                }
            });

            // Envio AJAX
            fetch(cadastroProdutoForm.action, {
                method: 'POST', 
                body: formData 
            })
            .then(response => {
                if (!response.ok) {
                    // Se o status HTTP não for 2xx, lança um erro para o bloco .catch
                    return response.json().then(err => { throw new Error(err.message || 'Erro desconhecido no servidor.'); });
                }
                return response.json(); 
            })
            .then(data => {
                if (data.status === "success") {
                    Swal.fire({
                        title: 'Sucesso!',
                        text: `${data.message}`, 
                        icon: 'success',
                        timer: 1500, // Tempo suficiente para o usuário ler
                        timerProgressBar: true, 
                        showConfirmButton: false, 
                    }).then(() => { 
                        // Redireciona para recarregar o formulário (limpo)
                        window.location.href = "/cadastrar/produto"; 
                    });
                    
                } else {
                    // Exibe erro retornado pelo backend
                    Swal.fire({
                        title: 'Erro no Cadastro!',
                        text: data.message, 
                        icon: 'error',
                        confirmButtonText: 'Tentar Novamente'
                    });
                }
            })
            .catch(error => {
                console.error('Erro de comunicação ou validação:', error);
                // Fecha o alerta de processamento e mostra o erro
                Swal.close(); 
                Swal.fire({
                    title: 'Ops!',
                    text: `Ocorreu um erro: ${error.message || 'Erro inesperado de rede.'}`, 
                    icon: 'warning',
                    confirmButtonText: 'OK'
                });
            });
        });
    }
});
