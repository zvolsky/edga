# coding: utf8

def nova():
    return _form_rp(SQLFORM(db.rp, _class='poptavka', submit_button="Pokračovat"))

def edit():
    return _form_rp(SQLFORM(db.rp, request.args(0), _class='poptavka', submit_button="Uložit změny"))

def _form_rp(form):
    response.view = 'poptavka/rp.html'
    nemame = ' (x)'
    '''
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
            #Field('pasparta_id', db.pasparta,                                   default=2,
            #    requires=IS_IN_DB(db, db.pasparta.id, lambda r: r.typ)),
            #Field('pasparta_barva_id', db.barva, requires=IS_IN_SET([])),
            Field('pasparta_cislo', 'string', length=10),
            Field('pasparta_oken', 'integer', default=1),
            Field('pasparta_poznamka', 'text'),
            #Field('pasparta2_id', db.pasparta,
            #    requires=IS_IN_DB(db, db.pasparta.id, lambda r: r.typ)),
            #Field('pasparta2_barva_id', db.barva, requires=IS_IN_SET([(1,'bílá')])),
            Field('pasparta2_cislo', 'string', length=10),
            Field('pasparta2_oken', 'integer', default=1),
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
            Field('zaves_ks', 'integer', default=1),
            Field('zaves_id', db.zaves,
                requires=IS_IN_DB(db, db.zaves.id,
                lambda r: r.nazev + ('' if r.skladem else nemame))),
            Field('zaves_poznamka', 'text'),
            Field('ksmat_ks', 'integer', default=1),
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
    '''

    if form.process().accepted:
        if form.vars.poptavka_id:
            redirect(URL('poptavky', 'otevrene'))

        # nová poptávka
        bude_asi, firma_id = _priprav_nova_poptavka('rp')
        poptavka_id = db.poptavka.insert(bude_asi=bude_asi, firma_id=firma_id)
        db.rp[form.vars.id] = dict(poptavka_id=poptavka_id)
        redirect(URL('poptavka', 'poptavajici', args=poptavka_id))

    return dict(form=form)

def _priprav_nova_poptavka(firma_zkratka):
    ted = datetime.datetime.now()
    bude_asi = ted.replace(hour=11, minute=0, second=0, microsecond=0
          ) + datetime.timedelta(days=7+5-datetime.datetime.isoweekday(ted)) 

    firma = db(db.firma.zkratka==firma_zkratka).select(db.firma.id)
    if firma:
        firma_id = firma[0].id
    else:
        firma_id = None

    return bude_asi, firma_id 

def poptavajici():
    if not request.args(0):      # nesprávné volání
        redirect(URL('poptavky', 'otevrene'))

    # https://groups.google.com/forum/?fromgroups#!searchin/web2py/hidden$20field/web2py/XZEWSfgHHik/tMPqtl5pRlEJ
    #   ale zdá se, že to lze řešit snáze        
    form = SQLFORM.factory(
        Field('hledame', label="Vyber z existujících kontaktů"),
        hidden=dict(poptavajici_id='')
        )
    if form.process(onvalidation=_validate_form).accepted:
        db.poptavka[request.args(0)] = dict(poptavajici_id=form.vars.poptavajici_id)
        redirect(URL('poptavka', 'hlavicka_edit', args=request.args(0)))
    poptavaci = db().select(db.poptavajici.id,
            db.poptavajici.jmeno,
            db.poptavajici.telefon,
            db.poptavajici.telefon2,
            db.poptavajici.email,
          orderby=db.poptavajici.jmeno)
    for poptavac in poptavaci:
        poptavac.hledej = ' '.join((poptavac.jmeno,
                poptavac.telefon.replace(' ',''),
                poptavac.telefon2.replace(' ',''),
                poptavac.email))
        del poptavac.telefon       
        del poptavac.telefon2       
        del poptavac.email       
    return dict(form=form, poptavaci=poptavaci)

def _validate_form(form):
    if request.vars.poptavajici_id:
        form.vars.poptavajici_id = request.vars.poptavajici_id
    else:
        form.errors.hledame = "Zadáním textu nalezněte zákazníka"

def poptavajici_novy():
    if not request.args(0):      # nesprávné volání
        redirect(URL('poptavky', 'otevrene'))        
    form = SQLFORM.factory(
        Field('jmeno', label="Příjmení+Jméno / Název", requires=IS_NOT_EMPTY()),
        Field('telefon', length=16, label=ttt('Telefon')),
        Field('telefon2', length=16, label=ttt('Telefon (další)')),
        Field('email', length=64, label=ttt('E-mail')),
        Field('poznamka', 'text', label=ttt('Poznámka')),
        )
    if form.process().accepted:
        poptavajici_id = db.poptavajici.insert(
            jmeno=form.vars.jmeno,
            telefon=form.vars.telefon,
            telefon2=form.vars.telefon2,
            email=form.vars.email,
            poznamka=form.vars.poznamka,
            )
        db.poptavka[request.args(0)] = dict(poptavajici_id=poptavajici_id)
        redirect(URL('poptavka', 'hlavicka_edit', args=request.args(0)))        
    return dict(form=form)

def hlavicka_edit():
    if not request.args(0):      # nesprávné volání
        redirect(URL('poptavky', 'otevrene'))
    poptavka = db.poptavka[request.args(0)]        
    form = SQLFORM(db.poptavka, request.args(0), submit_button="Uložit změny")
    if form.process().accepted:
        redirect(URL('poptavky', 'otevrene'))
    return dict(form=form, poptavka=poptavka)

def lista_get_text():
    '''voláno přes ajax'''
    neexistuje = '-- taková lišta neexistuje --'
    nemame = '(x)'
    cena = 0
    sirka = 0
    alt2 = request.args and request.args[0] or '' # lista | lista2
    lista_cislo = request.vars['lista%s_cislo' % alt2]
    if lista_cislo:
        lista = db((db.lista.id==db.lista_bv.lista_id) &
                (db.lista_bv.cislo==lista_cislo)).select(
                db.lista.ALL, db.lista_bv.ALL).first()
        if lista:
            retval = '<b>%s</b> %s %s %s %s' % (lista.lista.typ or '',
                    lista.lista_bv.barva or '',
                    '%s cm'%lista.lista.sirka if lista.lista.sirka else '',
                    '' if lista.lista_bv.skladem else nemame)
            cena = lista.lista_bv.cena
            sirka = lista.lista.sirka
        else:
            retval = neexistuje
    else:
        retval = ''
    return ("if ('%s'=='%s') alert('Nesprávné číslo lišty.');"
               "$('#lista%s_text').html('%s');"
               "if ('%s'.slice(-3)=='%s') alert('Lišta není skladem.');"
               "cena_lista%s=%s;sirka_lista%s=%s;cena();"
               % (retval, neexistuje, alt2, retval, retval, nemame, alt2, cena, alt2, sirka))

def pasparta_get_text():
    '''voláno přes ajax()'''
    neexistuje = '-- taková pasparta neexistuje --'
    nemame = '(x)'
    cena = cena_okna = 0
    rozm = ''
    alt2 = request.args and request.args[0] or '' # pasparta | pasparta2
    pasparta_cislo = request.vars['pasparta%s_cislo' % alt2]
    if pasparta_cislo:
        pasparta = db((db.pasparta.id==db.pasparta_bv.pasparta_id) &
                  (db.pasparta_bv.cislo==pasparta_cislo)).select(
                  db.pasparta.ALL, db.pasparta_bv.ALL).first()
        if pasparta:
            cena_okna = pasparta.pasparta.cena_okna 
            retval = '<b>%s</b> %s %s' % (pasparta.pasparta.typ or '',
                    pasparta.pasparta_bv.barva or '',
                    '' if pasparta.pasparta_bv.skladem else nemame)
            pasparty_rozmer = db(db.pasparta_rozmer.pasparta_id==pasparta.pasparta.id
                  ).select(db.pasparta_rozmer.ALL, db.rozmer.ALL,
                  left=db.rozmer.on(db.rozmer.id==db.pasparta_rozmer.rozmer_id)
                  ).sort(lambda row: row.rozmer.sirka)
            if pasparty_rozmer:
                rozm_id=rozm_vyska=rozm_sirka=rozm_cena = ''
                for rozmer in pasparty_rozmer:
                    rozm_id += ','+str(rozmer.rozmer.id)
                    rozm_sirka += ','+str(rozmer.rozmer.sirka)
                    rozm_vyska += ','+str(rozmer.rozmer.vyska)
                    rozm_cena += ','+str(rozmer.pasparta_rozmer.cena)
                rozm = (rozm_id[1:]+';'+
                      rozm_sirka[1:]+';'+rozm_vyska[1:]+';'+rozm_cena[1:])
        else:
            retval = neexistuje
    else:
        retval = ''

    return ("if ('%s'=='%s') alert('Nesprávné číslo pasparty.');"
               "$('#pasparta%s_text').html('%s');"
               "if ('%s'.slice(-3)=='%s') alert('Pasparta není skladem.');"
               "var elem=$('#rp_pasparta%s_cislo')[0];"
               "$.data(elem, 'rozm', '%s');"
               "cena_okna%s=%s;"
               "pasparty();"
               "cena();"
               % (retval, neexistuje, alt2, retval, retval, nemame, alt2, rozm, alt2, cena_okna))

"""
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
            //? uz_vetsi = None # nebo False, ale níže přiřazuji obvykle None 
            for rozmer in pasparty_rozmer:
                rozm_id += ','+str(rozmer.rozmer.id)
                rozm_sirka += ','+str(rozmer.rozmer.sirka)
                rozm_vyska += ','+str(rozmer.rozmer.vyska)
                rozm_cena += ','+str(rozmer.pasparta_rozmer.cena)
            rozm = (rozm_id[1:]+';'+
                  rozm_sirka[1:]+';'+rozm_vyska[1:]+';'+rozm_cena[1:])
    return ("var elem=$('#rp_pasparta%s_id')[0];"
              "$.data(elem, 'rozm', '%s');"
              "$.data(elem, 'barv', '%s');"
              "$('#rp_pasparta%s_barva_id').html('%s');"
              "pasparty();"
              "cena();"
              % (alt2, rozm, barv, alt2, barvy))
    '''       "alert($.data(elem, 'rozm'));"
              "alert($.data(elem, 'barv'));"
    ladění vrácených informací o paspartě''' 
"""

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

def zaves_get_cena():
    '''voláno přes ajax()'''
    nemame = False
    cena = 0
    #alt2 = request.args and request.args[0] or '' # -- | 2
    zaves_id = request.vars['zaves_id']
    if zaves_id:
        zaves = db.zaves[zaves_id]
        cena = zaves.cena
        nemame = not zaves.skladem
    return (("cena_zaves=%s;cena();" % (cena)) +
        (nemame and "alert('Závěs není skladem.');" or ""))

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
