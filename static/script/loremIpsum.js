
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
        if (result.isConfirmed)  ()=>{
            console.log("sim");
        }
    });
});