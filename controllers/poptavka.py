# coding: utf8

def nova():
    return _edit_rp()

def edit():
    return _edit_rp()

def _edit_rp():
    response.view = 'poptavka/poptavka.html'
    nemame = ' (x)'
    form = SQLFORM.factory(
            Field('sirka', 'decimal(5,1)',                                      default=20),
            Field('vyska', 'decimal(5,1)',                                      default=30),
            Field('levy', 'decimal(5,1)'),
            Field('horni', 'decimal(5,1)'),
            Field('pravy', 'decimal(5,1)'),
            Field('dolni', 'decimal(5,1)'),
            Field('lista_cislo', 'string', length=10),
            #Field('lista_id', db.lista, writable=True),
            #Field('lista_text', 'string', default='', writable=False),
            Field('lista_poznamka', 'text'),
            Field('lista2_cislo', 'string', length=10),
            Field('lista2_poznamka', 'text'),
            Field('pasparta_id', db.pasparta,                                   default=2,
                requires=IS_IN_DB(db, db.pasparta.id, lambda r: r.typ)),
            Field('pasparta_barva_id', db.barva, requires=IS_IN_SET([])),
            Field('pasparta_poznamka', 'text'),
            Field('pasparta2_id', db.pasparta,
                requires=IS_IN_DB(db, db.pasparta.id, lambda r: r.typ)),
            Field('pasparta2_barva_id', db.barva, requires=IS_IN_SET([(1,'bílá')])),
            Field('pasparta2_poznamka', 'text'),
            Field('podklad_id', db.podklad,
                requires=IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('podklad_poznamka', 'text'),
            Field('podklad2_id', db.podklad,
                requires=IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('podklad2_poznamka', 'text'),
            Field('sklo_id', db.sklo,
                requires=IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('sklo_poznamka', 'text'),
            Field('sklo2_id', db.sklo,
                requires=IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('sklo2_poznamka', 'text'),
            Field('blintram_id', db.blintram,
                requires=IS_IN_DB(db, db.blintram.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('blintram_vzper_sirka', 'integer', default=0),
            Field('blintram_vzper_vyska', 'integer', default=0),
            Field('blintram_poznamka', 'text'),
            Field('platno_id', db.platno,
                requires=IS_IN_DB(db, db.platno.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('platno_poznamka', 'text'),
            Field('ksmat_ks', 'integer'),
            Field('ksmat_id', db.ksmat,
                requires=IS_IN_DB(db, db.ksmat.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('ksmat_poznamka', 'text'),
            Field('poznamka', 'text'),
            Field('cena_mat1', 'integer', default=0, writable=False),
            Field('priplatek1', 'integer', default=0),
            Field('cena1', 'integer', default=0, writable=False),
            Field('ks', 'integer', default=1),
            Field('celkem', 'decimal(6,2)', default=0, writable=False),
            Field('dph', 'decimal(6,2)', default=0, writable=False),
            Field('sdph', 'integer', default=0, writable=False),
            Field('priplatek_duvod', 'text'),
            _class='poptavka',
            )
    if form.validate():
        pass   # uložení do více tabulek db schématu
    return dict(form=form)

def lista_get_text():
    '''voláno přes ajax()'''
    neexistuje = '-- taková lišta neexistuje --'
    nemame = '(x)'
    cena = 0
    sirka = 0
    alt2 = request.args and request.args[0] or '' # lista | lista2
    lista_cislo = request.vars['lista%s_cislo' % alt2]
    if lista_cislo:
        lista = db(db.lista.cislo==lista_cislo).select().first()
        if lista:
            retval = '%s %s %s %s %s' % (lista.typ or '',
                    lista.nazev or '',
                    lista.vyrobce or '',
                    '%s cm'%lista.sirka if lista.sirka else '',
                    '' if lista.skladem else nemame)
            cena = lista.cena
            sirka = lista.sirka
        else:
            retval = neexistuje
    else:
        retval = ''
    return ("if ('%s'=='%s') alert('Nesprávné číslo lišty.');"
               "$('#lista%s_text').text('%s');"
               "if ('%s'.slice(-3)=='%s') alert('Lišta není skladem.');"
               "cena_lista%s=%s;sirka_lista%s=%s;cena();"
               % (retval, neexistuje, alt2, retval, retval, nemame, alt2, cena, alt2, sirka))

def pasparta_get_more():
    '''voláno přes ajax()'''
    pasparty_rozmer = barvy_nelze = None
    rozm=barv = '' # co sdělíme frontendu o vybrané paspartě
        # rozm (id; šířky; výšky; ceny), barv (id;1|0=máme;rozmer_max_id)
    barvy = '<option value=""></option>' 
    alt2 = request.args and request.args[0] or '' # -- | 2
    pasparta_id = request.vars['pasparta%s_id' % alt2]
    if pasparta_id:
        pasparta = db.pasparta(pasparta_id)
        if pasparta:
            pasparty_rozmer = db(db.pasparta_rozmer.pasparta_id==pasparta_id
                  ).select(db.pasparta_rozmer.ALL, db.rozmer.ALL,
                  left=db.rozmer.on(db.rozmer.id==db.pasparta_rozmer.rozmer_id)
                  ).sort(lambda row: row.rozmer.sirka)
            barvy_nelze = db(db.barva_nelze.pasparta_id==pasparta_id).select()
            barv_id=barv_mame=barv_max = ''
            if pasparta.sada_barev_id: 
                for barva in db(db.barva.sada_barev_id==pasparta.sada_barev_id
                              ).select():
                    nemame=rozmer_max_id = ''
                    # jasně definované chování je pro jediný nebarva záznam
                    #   k dané barvě; nicméně dělám for..: a z případných více
                    #   záznamů poberu důležité údaje
                    for nebarva in barvy_nelze.find(
                                  lambda row: row.barva_id==barva.id):
                        rozmer_max_id = rozmer_max_id or nebarva.rozmer_id
                        nemame = nemame or not nebarva.skladem and ' (x)' or ''
                    barvy += '<option class="pasp_barva" id="b%s" value="%s">%s</option>' % (
                              barva.id, barva.id, barva.barva)
                    barv_id += ','+str(barva.id)
                    barv_mame += ','+(nemame and '0' or '1')
                    barv_max += ','+str(rozmer_max_id or 0) 
                barv = barv_id[1:]+';'+barv_mame[1:]+';'+barv_max[1:]
            rozm_id=rozm_vyska=rozm_sirka=rozm_cena = ''
            uz_vetsi = None # nebo False, ale níže přiřazuji obvykle None 
            for rozmer in pasparty_rozmer:
                rozm_id += ','+str(rozmer.rozmer.id)
                rozm_sirka += ','+str(rozmer.rozmer.sirka)
                rozm_vyska += ','+str(rozmer.rozmer.vyska)
                rozm_cena += ','+str(rozmer.pasparta_rozmer.cena)
            rozm = (rozm_id[1:]+';'+
                  rozm_sirka[1:]+';'+rozm_vyska[1:]+';'+rozm_cena[1:])
    return ("var elem=$('#no_table_pasparta%s_id')[0];"
              "$.data(elem, 'rozm', '%s');"
              "$.data(elem, 'barv', '%s');"
              "$('#no_table_pasparta%s_barva_id').html('%s');"
              "pasparty();"
              "cena();"
              % (alt2, rozm, barv, alt2, barvy))
    '''       "alert($.data(elem, 'rozm'));"
              "alert($.data(elem, 'barv'));"
    ladění vrácených informací o paspartě''' 

def podklad_get_cena():
    '''voláno přes ajax()'''
    nemame = False
    cena = 0
    alt2 = request.args and request.args[0] or '' # -- | 2
    podklad_id = request.vars['podklad%s_id' % alt2]
    if podklad_id:
        podklad = db.podklad[podklad_id]
        cena = podklad.cena
        nemame = not podklad.skladem
    return (("cena_podklad%s=%s;cena();" % (alt2, cena)) +
        (nemame and "alert('Podklad není skladem.');" or ""))

def sklo_get_cena():
    '''voláno přes ajax()'''
    nemame = False
    cena = 0
    alt2 = request.args and request.args[0] or '' # -- | 2
    sklo_id = request.vars['sklo%s_id' % alt2]
    if sklo_id:
        sklo = db.sklo[sklo_id]
        cena = sklo.cena
        nemame = not sklo.skladem
    return (("cena_sklo%s=%s;cena();" % (alt2, cena)) +
        (nemame and "alert('Sklo není skladem.');" or ""))

def blintram_get_cena():
    '''voláno přes ajax()'''
    vzpery_po = 0
    nemame = False
    cena = 0
    ram_id = request.vars['blintram_id']
    if ram_id:
        ram = db.blintram[ram_id]
        vzpery_po = ram.vzpery_po
        cena = ram.cena
        nemame = not ram.skladem
    return (("blintram_vzpery_po=%s;cena_blintram=%s;blintram();cena();" % (vzpery_po, cena)) +
        (nemame and "alert('Rám není skladem.');" or ""))

def platno_get_cena():
    '''voláno přes ajax()'''
    presah = 7
    nemame = False
    cena = 0
    platno_id = request.vars['platno_id']
    if platno_id:
        platno = db.platno[platno_id]
        presah = platno.presah
        cena = platno.cena
        nemame = not platno.skladem
    return (("platno_presah=%s;cena_platno=%s;cena();" % (presah, cena)) +
        (nemame and "alert('Plátno není skladem.');" or ""))

def ksmat_get_cena():
    '''voláno přes ajax()'''
    nemame = False
    cena = 0
    #alt2 = request.args and request.args[0] or '' # -- | 2
    ksmat_id = request.vars['ksmat_id']
    if ksmat_id:
        ksmat = db.ksmat[ksmat_id]
        cena = ksmat.cena
        nemame = not ksmat.skladem
    return (("cena_ksmat=%s;cena();" % (cena)) +
        (nemame and "alert('Doplněk není skladem.');" or ""))
