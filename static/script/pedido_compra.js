$(document).ready(function () {
    // Código de máscara existente
    $('.valor').mask('000.000.000,00', {
        reverse: true,
        placeholder: "0,00"
    });
});

document.addEventListener('DOMContentLoaded', function() {

    // Função genérica para interceptar links e mostrar o SweetAlert
    function handleSweetAlert(selector, title, text, confirmText, icon, confirmColor) {
        
        // Seleciona todos os elementos com o seletor (classe)
        const links = document.querySelectorAll(selector);

        links.forEach(link => {
            link.addEventListener('click', function(e) {
                // 1. Impede a navegação imediata
                e.preventDefault();

                // Armazena a URL de destino
                const targetUrl = this.getAttribute('href');

                Swal.fire({
                    title: title,
                    text: text,
                    icon: icon,
                    showCancelButton: true,
                    confirmButtonColor: confirmColor,
                    cancelButtonColor: '#d33',
                    confirmButtonText: confirmText,
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // 2. Se confirmado, redireciona para a URL
                        window.location.href = targetUrl;
                    }
                });
            });
        });
    }
    
    // --- 1. Sweet Alert para Excluir Produto do Pedido ---
    handleSweetAlert(
        '.link--excluir-produto-pedido', 
        'Remover Produto?', 
        'Você deseja remover este item do seu pedido de compra?', 
        'Sim, Remover!', 
        'warning', 
        '#3085d6'
    );

    // --- 2. Sweet Alert para Finalizar Pedido ---
    handleSweetAlert(
        '.link--finalizar-pedido', 
        'Finalizar Pedido?', 
        'Ao finalizar, o pedido será concluído e o estoque será atualizado. Você confirma a compra?', 
        'Sim, Finalizar!', 
        'success', // Mudando para ícone de sucesso/info, pois é uma conclusão positiva
        '#28a745' // Cor verde para o botão de confirmação
    );

});