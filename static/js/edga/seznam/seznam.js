// pro seznam/seznam.html view

var minula_cena = $('#minula_cena').attr('data-cena') || 0.0
var minula_nakupni = $('#minula_cena').attr('data-nakupni') || 0.0

$(document).ready(function() {
    if (parseFloat($('#lista_bv_cena').val())<=0.0) {
        $('#lista_bv_cena').val(minula_cena)
    }
    if (parseFloat($('#lista_bv_nakupni').val())<=0.0) {
        $('#lista_bv_nakupni').val(minula_nakupni)
    }
});
