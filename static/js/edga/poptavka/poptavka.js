// pro poptavka/poptavka.html view
// funkce volání ajaxu (protože obsahují templating {{..}}) jsou definovány ve view

var koefDPH = 1.21;
// inicializace cen
var cena_lista=0;
var cena_lista2=0;
var sirka_lista=0;
var sirka_lista2=0;
var cena_pasparta=0;
var cena_pasparta2=0;
var cena_podklad=0;
var cena_podklad2=0;
var cena_sklo=0;
var cena_sklo2=0;
var cena_ksmat=0;
var blintram_vzpery_po=0;
var blintram_vzpery_pricne=0;
var blintram_vzpery_podelne=0;
var platno_presah=0;
var cena_blintram=0;
var cena_platno=0;

function rozmery() {
    return [
        +$('#no_table_sirka').val()||0,
        +$('#no_table_vyska').val()||0,
        +$('#no_table_levy').val()||0,
        +$('#no_table_horni').val()||0,
        +$('#no_table_pravy').val()||0,
        +$('#no_table_dolni').val()||0
    ];
}

function cena() {
    /* při umístění do document.ready() nespočte cenu napoprvé */
    var rozm = rozmery(); // [šíř,výš, lev,hor,pr,dol]
    var sirka = rozm[0];
    var vyska = rozm[1];
    var levy = rozm[2];
    var horni = rozm[3];
    var pravy = rozm[4];
    var dolni = rozm[5];
    var obvod_vnitrni = ((sirka + vyska) / 50).toFixed(3);
    var obvod_vnejsi = ((sirka + vyska + levy + horni + pravy + dolni) / 50
                        ).toFixed(3);
    var plocha_vnitrni = (sirka*vyska*0.0001).toFixed(4);
    var plocha_vnejsi = ((sirka+levy+pravy)*(vyska+horni+dolni)*0.0001).toFixed(4);
    var ksmat_ks = +$('#no_table_ksmat_ks').val()||0;
    var cena_mat1 = cena_lista*(obvod_vnejsi + 8*sirka_lista) +
                    cena_lista2*(obvod_vnejsi + 8*sirka_lista2) +
                    cena_pasparta + cena_pasparta2 +
                    (cena_podklad + cena_podklad2)*plocha_vnejsi +
                    (cena_sklo + cena_sklo2)*plocha_vnejsi +
                    ksmat_ks*cena_ksmat;
    $('#cena_mat1').text(cena_mat1.toFixed(2));
    var cena1 = cena_mat1 + parseFloat($('#no_table_priplatek1').val());
    $('#cena1').text(cena1.toFixed(0));
    var sdph = (cena1 * parseFloat($('#no_table_ks').val()) * koefDPH).toFixed(0);
    var celkem = (Math.floor((sdph/koefDPH)*100)/100).toFixed(2);
    $('#sdph').text(sdph);
    $('#celkem').text(celkem);
    var dph = (sdph - celkem).toFixed(2);
    $('#dph').text(dph);
          /*$('#xx').text(parseInt($('#xx').text())+1); ladění počtu spuštění*/
}

function pasparty() {
    var rozm = rozmery(); // [šíř,výš, lev,hor,pr,dol]
    var sirka_celkova = rozm[0]+rozm[2]+rozm[4];
    var vyska_celkova = rozm[1]+rozm[3]+rozm[5];
    var mensi = Math.min(sirka_celkova, vyska_celkova);
    var vetsi = Math.max(sirka_celkova, vyska_celkova);
    var pasparta1 = $('#no_table_pasparta_id')[0];
    var pasparta2 = $('#no_table_pasparta2_id')[0];
    var rozm1 = $.data(pasparta1, 'rozm'); //id,id,,;sirky,,;vysky,,;ceny,,
    var rozm2 = $.data(pasparta2, 'rozm');
    var barv1 = $.data(pasparta1, 'barv'); //id,id,,;mame(0|1),,;0|max_rozm_id,,
    var barv2 = $.data(pasparta2, 'barv');
    cena_pasparta = pasp_cena(rozm1, mensi, vetsi); 
    cena_pasparta2 = pasp_cena(rozm2, mensi, vetsi); 
}

function pasp_cena(rozm, mensi, vetsi) {
  //string "rozm" z ajaxu pasparta_get_more(), menší rozměr, větší rozměr
  //string "rozm": id,id,,;sirky,,;vysky,,;ceny,,
    if (!rozm) return 0.0;
    var plocha = mensi*vetsi;
    var casti = rozm.split(';'); // [0]id, [1]sirky, [2]vysky, [3]ceny
    /* nově volba rozměru tak, aby se vešla plošně */
    var sirky = casti[1].split(',');
    var vysky = casti[2].split(',');
    for (var i=0; i < Math.min(sirky.length, vysky.length); i++) {
        if (plocha<=sirky[i]*vysky[i]) break;
    }
    return parseFloat(casti[3].split(',')[i]); 

        /* původně volba rozměru tak, aby se vešla do obou rozměrů
        var i = Math.max(vejde_se(mensi, casti[1]), vejde_se(vetsi, casti[2]));
        function vejde_se(rozmer, rozmery) {
          //pořadí čísla v rozmery (r1,r2,..), do kterého se vejde rozmer
            var arozmery = rozmery.split(','); 
            for (var i=0; i < arozmery.length; i++) {
                if (rozmer<=arozmery[i]) break;
            }
            return i;
        }
        */
} 

$(document).ready(function() {
    $('#no_table_sirka').focus();
    /* $('form:first *:input[type!=hidden]:first').focus();
       $('*:input:visible:enabled:first').focus();
       $("form:first *:input,select,textarea").filter(":not([readonly='readonly']):not([disabled='disabled']):not([type='hidden'])").first().focus(); */
      
    var priplatek='#priplatek_duvod, #priplatek_castka, #vysledna_cena';
    if ($('#priplatek_castka').val()!=0) {$(priplatek).show()};
    $('#priplatek').click(function() {
        if ($('#no_table_priplatek1').val()==0) {
            $(priplatek).slideToggle();
        } else {
            if (confirm('Stiskni OK pro odstranění příplatku.')) {
                if ($('#no_table_priplatek_duvod').val()!='') {
                    $('#no_table_priplatek_duvod').val($('#no_table_priplatek_duvod').val()+'\nPříplatek '+$('#no_table_priplatek1').val()+' Kč byl zrušen.')
                }
                $('#no_table_priplatek1').val(0);
                cena();
                $(priplatek).hide();
            } else {
                $(priplatek).show();
            }
        }
    });
      
    $('#no_table_sirka, #no_table_vyska').change(function() {
        if ($('#no_table_sirka').val()>$('#no_table_vyska').val()) {
            $('#orientace').fadeIn();
        } else {
            $('#orientace').fadeOut();
        }
    });
       
    $('#no_table_levy').change(function() {
  	    if ($('#no_table_levy').val()<=0) { 
            $('#no_table_levy').val(0);
        }
        if ($('#no_table_pravy').val()<=0) { 
 	          $('#no_table_pravy').val(+$(this).val());
        }
        if ($('#no_table_horni').val()<=0) { 
            $('#no_table_horni').val(+$(this).val());
        }
        if ($('#no_table_dolni').val()<=0) { 
            $('#no_table_dolni').val(+$(this).val()+1.0);
        }
    });
      
    $('#no_table_lista_cislo').change(function() {
                                                 //$('#b5').text('xxxxxxxxx');
        lista_cislo_change();
    });
    $('#no_table_lista2_cislo').change(function() {
        lista2_cislo_change();
    });
  
    $('#no_table_pasparta_id').change(function() {
        pasparta_id_change();
    });
    $('#no_table_pasparta2_id').change(function() {
        pasparta2_id_change();
    });
  
    $('#no_table_podklad_id').change(function () {
        podklad_change();
    });
    $('#no_table_podklad2_id').change(function () {
        podklad2_change();
    });
  
    $('#no_table_sklo_id').change(function () {
        sklo_change();
    });
    $('#no_table_sklo2_id').change(function () {
        sklo2_change();
    });
  
    $('#no_table_ram_id').change(function () {
        blintram_change();
    });
    $('#no_table_platno_id').change(function () {
        platno_change();
    });

    $('#no_table_ksmat_id').change(function () {
        ksmat_change();
    });
  
    lista_cislo_change(); 
    lista2_cislo_change(); 
    pasparta_id_change();
    pasparta2_id_change();
    podklad_change();
    podklad2_change();
    sklo_change(); 
    sklo2_change(); 
    blintram_change();
    platno_change();
    ksmat_change();
  
    $('.paspa').change(function() {
        pasparty();
        cena();
    });
    $('input').change(function() {
        cena();
    });
    
    /* časem možná zkusit toto úplně vyhodit, protože se při inicializaci
        zřejmě vždy volá opakovaně */
    pasparty(); /* určení ceny a barev pasparty */
    cena(); /* jistota; ale zavolá se vícekrát přes ajax, např. u lišty */
  
    /* automaticky přizpůsobovat výšku textarea; v kombinaci s style overflow:hidden */
    function textAreaAdjust(o) {
        o.style.height = "1px";
        o.style.height = (o.scrollHeight)+"px"; /* lze (o.scrollHeight+/-nnn) */
    }
    $('div.detail textarea').keyup(function() {
        textAreaAdjust(this);
    });
  
    $('.druhak').click(function() {
        $(this).parent().parent().parent().children('div.grp2').show();
        $(this).hide();
        return false;
    });

    $('.blintram__ukaz_a').click(function() {
        $('#blintram_skryty').show();
        $(this).parent().hide();
        return false;
    });
  
    $('.poznamka_dil').click(function() {
        var detail = $(this).parent().parent().children('div.detail');
        var txt = detail.children('textarea');
        if (detail.css('display')=='none') {
            detail.show(); /* .slideUp trhalo s obrazem */
            detail.children('textarea').focus();
        } else if (!txt.val()) {
            detail.slideUp();
        } else if (confirm('Pomocí OK smažeš text poznámky.')) {
            txt.val(null);
            detail.slideUp();
        }
        return false;
    });
  
    function show_poznamka(o){
        if (o.val()) {
            o.parent().show();
            o.height((14*o.val().match(/\n?[^\n]{1,80}|\n/g).length)+'px');
        }
    }
  
    show_poznamka($('#no_table_lista_poznamka'));
    show_poznamka($('#no_table_lista2_poznamka'));
    show_poznamka($('#no_table_pasparta_poznamka'));
    show_poznamka($('#no_table_pasparta2_poznamka'));
    show_poznamka($('#no_table_podklad_poznamka'));
    show_poznamka($('#no_table_podklad2_poznamka'));
    show_poznamka($('#no_table_sklo_poznamka'));
    show_poznamka($('#no_table_sklo2_poznamka'));
    show_poznamka($('#no_table_poznamka'));
  
    function show_grp2(o,p) {
        if (o.val()||p.val()) {
            o.parent().parent().show();
        }
    }
  
    show_grp2($('#no_table_lista2_cislo'), $('#no_table_lista2_poznamka'));
    show_grp2($('#no_table_pasparta2_cislo'), $('#no_table_pasparta2_poznamka'));
    show_grp2($('#no_table_podklad2_id'), $('#no_table_podklad2_poznamka'));
    show_grp2($('#no_table_sklo2_id'), $('#no_table_sklo2_poznamka'));
  
});
