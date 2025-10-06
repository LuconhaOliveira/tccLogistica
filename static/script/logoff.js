document.querySelector('#logoff').addEventListener('click',()=>{
    Swal.fire({
        title: "Deseja mesmo sair da sua conta?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sim",
        cancelButtonText: "Não",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33"
    }).then((result) => {
        if (result.isConfirmed) {
            requisicao_logoff();
        }
    });
});

async function requisicao_logoff(){
    try {
        const url = "/logoff";
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    } catch (erro) {
        console.error("Erro ao obter dados:", erro);
    }
} 