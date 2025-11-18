document.addEventListener('DOMContentLoaded', function() {
    const formHistorico = document.getElementById('form-limpar-historico');

    if (formHistorico) {
        formHistorico.addEventListener('submit', function(e) {
            // 1. Impede o envio padrão do formulário
            e.preventDefault();

            Swal.fire({
                title: 'Limpar Histórico?',
                text: "Esta ação é irreversível e apagará todos os registros de alteração!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sim, Apagar!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // 2. Se confirmado, envia o formulário
                    formHistorico.submit();
                }
            });
        });
    }
});