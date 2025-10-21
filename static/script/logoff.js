document.querySelector('#logoff').addEventListener('click', (event) => {
    // 1. Previne o comportamento padrão do link (#)
    event.preventDefault(); 
    
    // 2. SweetAlert de CONFIRMAÇÃO
    Swal.fire({
        title: "Deseja mesmo sair da sua conta?",
        // icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sim",
        cancelButtonText: "Não",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33"
    }).then((result) => {
        if (result.isConfirmed) {
            // Se confirmado, inicia o processo de logoff
            requisicao_logoff()
                .then(data => {
                    if (data && data.redirect) {
                        // 3. Logoff BEM-SUCEDIDO: Mostra o SweetAlert de SUCESSO
                        Swal.fire({
                            icon: 'success',
                            title: 'Desconectado!',
                            text: 'Você saiu da sua conta com sucesso.',
                            showConfirmButton: false,
                            timer: 1500 // Redireciona após 1.5 segundos
                        }).then(() => {
                            // 4. REDIRECIONA APÓS O ALERTA
                            window.location.href = data.redirect;
                        });
                    }
                })
                .catch(erro => {
                    // 5. Trata ERROS de rede ou erro HTTP (e mostra SweetAlert de erro)
                    console.error("Erro no logoff:", erro);
                    Swal.fire({
                        icon: 'error',
                        title: 'Erro!',
                        text: erro.message || 'Não foi possível realizar o logout. Tente novamente.',
                    });
                });
        }
    });
});

async function requisicao_logoff() {
    const url = "/logoff";
    try {
        const response = await fetch(url, {
            method: 'POST',
            // Adicione headers se o seu Flask exigir (como 'X-CSRFToken')
        });
        
        if (!response.ok) {
            // Lança um erro se o status HTTP não for 2xx
            throw new Error(`Falha no logoff: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data; 
        
    } catch (erro) {
        // Propaga o erro para ser pego pelo .catch no listener
        throw erro;
    }
}