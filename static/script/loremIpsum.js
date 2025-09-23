document.querySelector('#logoff').addEventListener('click',()=>{
    Swal.fire({
        title: "Deseja mesmo sair da sua conta?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim",
        cancelButtonText: "Não"
    }).then((result) => {
        if (result.isConfirmed) {
            requisicao_logoff();
        }
    });
});

async function requisicao_logoff(){
    try {
        const url = "https://tcc-logistica-1.onrender.com/logoff";
        const response = await fetch(url); // ✅ await aqui
        console.log(response); // ✅ agora mostra os dados reais
    } catch (erro) {
        console.error("Erro ao obter dados:", erro);
    }
} 