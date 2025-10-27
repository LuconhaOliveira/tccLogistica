// Conteúdo do sweet_alert_caracteristica.js, AGORA AQUI
        
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
                    title: 'Cadastro Realizado com Sucesso!',
                    text: `${data.message}`,
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