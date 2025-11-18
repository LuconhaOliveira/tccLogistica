$(document).ready(function () {
    // Código de máscara existente
    $('#valor').mask('000.000.000,00', {
        reverse: true,
        placeholder: "0,00"
    });

    // ----------------------------------------------------------------------
    // NOVO: SweetAlert para Confirmação de Exclusão de Produto
    // ----------------------------------------------------------------------

    // Seleciona o link de exclusão pela classe
    $('.link--deletar-produto').on('click', function (e) {
        // 1. Impede a navegação imediata do link
        e.preventDefault();

        // 2. Armazena a URL de exclusão do atributo href
        const deleteUrl = $(this).attr('href');

        // 3. Exibe o SweetAlert de confirmação
        Swal.fire({
            title: "Tem certeza?",
            text: "Você não poderá reverter a exclusão deste produto!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6", 
            cancelButtonColor: "#d33",
            confirmButtonText: "Sim, excluir!",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            // 4. Se o usuário confirmar (clicar em "Sim, excluir!")
            if (result.isConfirmed) {
                // Redireciona para a URL de exclusão
                window.location.href = deleteUrl;
            }
        });
    });
});