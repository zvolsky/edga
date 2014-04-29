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
var blintram_vzpery_sirka_last=0;
var blintram_vzpery_vyska_last=0;
var platno_presah=0;
var plocha_platno=0;
var cena_blintram=0;
var cena_platno=0;

function rozmery() {
    var sirka = +$('#no_table_sirka').val()||0;
    var vyska = +$('#no_table_vyska').val()||0;
    var levy = +$('#no_table_levy').val()||0;
    var horni = +$('#no_table_horni').val()||0;
    var pravy = +$('#no_table_horni').val()||0;
    var dolni = +$('#no_table_dolni').val()||0;
    $('#crozmer_sirka').text(sirka + levy + pravy);   
    $('#crozmer_vyska').text(vyska + horni + dolni);   
    return [sirka, vyska, levy, horni, pravy, dolni];
}

function blintram() {
    var blintram_vzpery_sirka = 0;
    var blintram_vzpery_vyska = 0;
    if (blintram_vzpery_po>0) {
        blintram_vzpery_sirka = Math.floor(
              (+$('#no_table_vyska').val() - 1) / blintram_vzpery_po );
        blintram_vzpery_vyska = Math.floor(
              (+$('#no_table_sirka').val() - 1) / blintram_vzpery_po );
    }
    if ((blintram_vzpery_sirka_last!=blintram_vzpery_sirka) ||
              (blintram_vzpery_vyska_last!=blintram_vzpery_vyska)) {
        if ((+$('#no_table_blintram_vzper_sirka').val()==0) &&
            (+$('#no_table_blintram_vzper_vyska').val()==0) ||
            confirm("Nově vypočtený počet vzpěr rámu:\nvodorovně: " +
                  blintram_vzpery_sirka + ', ' + "svisle: " +
                  blintram_vzpery_vyska + '\n\n' + "Změnit ?")) {
            $('#no_table_blintram_vzper_sirka').val(blintram_vzpery_sirka);
            $('#no_table_blintram_vzper_vyska').val(blintram_vzpery_vyska);
        }
        blintram_vzpery_sirka_last = blintram_vzpery_sirka;
        blintram_vzpery_vyska_last = blintram_vzpery_vyska;
    }
}

function cena() {
    /* při umístění do document.ready() nespočte cenu napoprvé */
    var rozm = rozmery(); // [šíř,výš, lev,hor,pr,dol] a zobrazí celkový rozměr
    var sirka = rozm[0];
    var vyska = rozm[1];
    var levy = rozm[2];
    var horni = rozm[3];
    var pravy = rozm[4];
    var dolni = rozm[5];
    var obvod_vnitrni = +((sirka + vyska) / 50).toFixed(3);  // 50 = 2 * .. / 100
    var obvod_vnejsi = +((sirka + vyska + levy + horni + pravy + dolni) / 50
                        ).toFixed(3);
    var plocha_vnitrni = +(sirka*vyska*0.0001).toFixed(4);
    var sirka_cela = +((sirka+levy+pravy) / 100).toFixed(3);
    var vyska_cela = +((vyska+horni+dolni) / 100).toFixed(3);
    var plocha_vnejsi = +(sirka_cela*vyska_cela).toFixed(4);
    if (platno_presah>0) {
        plocha_platno = +((sirka_cela+platno_presah/50)*(vyska_cela+platno_presah/50)).toFixed(4);
    } else {
        plocha_platno = plocha_vnejsi;
    }
    var ksmat_ks = +$('#no_table_ksmat_ks').val()||0;
    var vzper_sirka = +$('#no_table_blintram_vzper_sirka').val()||0;
    var vzper_vyska = +$('#no_table_blintram_vzper_vyska').val()||0;
    var cena_mat1 = cena_lista*(obvod_vnejsi + 8*sirka_lista) +
                    cena_lista2*(obvod_vnejsi + 8*sirka_lista2) +
                    cena_pasparta + cena_pasparta2 +
                    (cena_podklad + cena_podklad2)*plocha_vnejsi +
                    (cena_sklo + cena_sklo2)*plocha_vnejsi +
                    cena_blintram*
                      ((2+vzper_sirka)*sirka_cela + (2+vzper_vyska)*vyska_cela) +
                    cena_platno*plocha_platno +
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
  
    $('#no_table_blintram_id').change(function () {
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
