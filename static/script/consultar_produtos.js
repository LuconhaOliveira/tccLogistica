document.addEventListener('DOMContentLoaded', function() {
    // --- Lógica para Limpar Produtos ---
    const btnLimpar = document.getElementById('btn-limpar-produtos');
    if (btnLimpar) {
        btnLimpar.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            
            Swal.fire({
                title: 'Tem certeza?',
                text: "Esta ação removerá TODOS os produtos desta estante!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sim, Limpar Produtos!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Se confirmado, redireciona para a rota Flask de exclusão
                    window.location.href = url;
                }
            });
        });
    }

    // --- Lógica para Excluir Estante ---
    const btnExcluir = document.getElementById('btn-excluir-estante');
    if (btnExcluir) {
        btnExcluir.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            
            Swal.fire({
                title: 'Tem certeza?',
                text: "Ao excluir a estante, todos os produtos nela também serão removidos permanentemente!",
                icon: 'error', // Usando 'error' ou 'warning' para maior impacto
                showCancelButton: true,
                confirmButtonColor: '#3085d6', // Vermelho para a exclusão
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sim, Excluir Estante!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Se confirmado, redireciona para a rota Flask de exclusão
                    window.location.href = url;
                }
            });
        });
    }
});