$(document).ready(function () {
    // Código de máscara existente
    $('.list-group-item span').mask('000.000.000,00', {
        reverse: true,
        placeholder: "0,00"
    });
});