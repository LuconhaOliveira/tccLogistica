// --- Aplica evento no formulário de cadastro de estante --- //
const formEstante = document.getElementById('form-cadastro-estante');

if (formEstante) {

    formEstante.addEventListener('submit', function (event) {
        // Impede o comportamento padrão (reload da página)
        event.preventDefault();

        // Coleta os dados do formulário
        const formData = new FormData(formEstante);
        const nome = formData.get('nome');
        const codCategoria = formData.get('cod_categoria');

        // Validação simples no frontend
        if (!nome || !codCategoria || codCategoria === "") {
            Swal.fire({
                title: 'Preenchimento Necessário',
                text: 'Preencha o Nome e selecione a Categoria da estante.',
                icon: 'warning',
                confirmButtonText: 'Ok'
            });
            return;
        }

        // --- Requisição AJAX (Fetch) --- //
        fetch(formEstante.action || '/post/cadastro_estante/adicionar', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Se o status for 4xx ou 5xx, tenta ler o JSON mesmo assim
            if (!response.ok) {
                return response.json().then(data => {
                    // Sessão expirada (401)
                    if (response.status === 401 && data.redirect) {
                        Swal.fire({
                            title: data.titulo || 'Sessão Expirada',
                            text: data.mensagem || 'Por favor, faça login novamente.',
                            icon: 'error',
                            timer: 2000,
                            showConfirmButton: false,
                            timerProgressBar: true
                        }).then(() => {
                            window.location.href = data.redirect;
                        });
                        throw new Error('Sessão expirada');
                    }

                    // Outros erros (400, 500)
                    Swal.fire({
                        title: data.titulo || 'Erro HTTP',
                        text: data.mensagem || `Erro de Servidor: Status ${response.status}`,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                    throw new Error('Erro HTTP');
                });
            }

            // Caso 2xx, retorna o JSON normal
            return response.json();
        })
        .then(data => {
            // Se o JSON indicar sucesso
            if (data.status === "success") {
                Swal.fire({
                    title: data.titulo || 'Sucesso!',
                    text: `${data.mensagem}`,
                    icon: 'success',
                    timer: 1500,
                    timerProgressBar: true,
                    showConfirmButton: false
                }).then(() => {
                    window.location.href = "/principal";
                });

            } else {
                // Caso venha status "error" com status 2xx
                Swal.fire({
                    title: data.titulo || 'Erro!',
                    text: data.mensagem || 'Falha ao processar a requisição.',
                    icon: 'error',
                    confirmButtonText: 'Tentar Novamente'
                });
            }
        })
        .catch(error => {
            // Erros de rede ou JSON inválido
            console.error('Erro na requisição de cadastro de estante:', error);

            Swal.fire({
                title: 'Erro de Conexão',
                text: 'Não foi possível conectar ao servidor. Tente novamente.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        });
    });
}
