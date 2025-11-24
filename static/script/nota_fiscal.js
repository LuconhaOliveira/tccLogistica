$(document).ready(function () {
    // Código de máscara existente
    $('#valor').mask('000.000.000,00', {
        reverse: true,
        placeholder: "0,00"
    });
    $('#total').mask('000.000.000,00', {
        reverse: true,
        placeholder: "0,00"
    });
});