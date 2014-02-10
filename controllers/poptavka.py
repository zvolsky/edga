# coding: utf8

def nova():
    return _edit_rp()

def edit():
    return _edit_rp()

def _edit_rp():
    response.view = 'poptavka/poptavka.html'
    form = SQLFORM.factory(
            Field('sirka', 'decimal(5,1)', default=20),
            Field('vyska', 'decimal(5,1)', default=30),
            Field('levy', 'decimal(5,1)'),
            Field('horni', 'decimal(5,1)'),
            Field('pravy', 'decimal(5,1)'),
            Field('dolni', 'decimal(5,1)'),
            Field('lista_cislo', 'string', length=10),
            #Field('lista_id', db.lista, writable=True),
            #Field('lista_text', 'string', default='', writable=False),
            Field('lista_poznamka', 'text'),            
            Field('lista2_cislo', 'string', length=10),
            Field('lista2_poznamka', 'text', default='a'),            
            Field('pasparta_cislo', 'string', length=10),
            Field('pasparta_poznamka', 'text'),            
            Field('pasparta2_cislo', 'string', length=10, default=61),
            Field('pasparta2_poznamka', 'text'),            
            Field('podklad_id', db.podklad,
                requires=IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else ' (x)'))),
            Field('podklad_poznamka', 'text'),            
            Field('podklad2_id', db.podklad,
                requires=IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else ' (x)'))),
            Field('podklad2_poznamka', 'text'),            
            Field('sklo_id', db.sklo,
                requires=IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else ' (x)'))),                
            Field('sklo_poznamka', 'text', default="a\nb\nc\nd"),
            Field('sklo2_id', db.sklo, default=2,
                requires=IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else ' (x)'))),                
            Field('sklo2_poznamka', 'text'),
            Field('poznamka', 'text', default="a\nb"),
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
        pass
    return dict(form=form)

def lista_get_text():
    '''voláno přes ajax()'''
    neexistuje = '-- taková lišta neexistuje --'
    nemame = '(x)'
    cena = 0
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
        else:
            retval = neexistuje
    else:
        retval = ''
    print retval
    return ("if ('%s'=='%s') alert('Nesprávné číslo lišty.');"
               "$('#lista%s_text').text('%s');"
               "if ('%s'.slice(-3)=='%s') alert('Lišta není skladem.');"
               "cena_lista%s=%s;cena();"
               % (retval, neexistuje, alt2, retval, retval, nemame, alt2, cena))

def pasparta_get_text():
    '''voláno přes ajax()'''
    neexistuje = '-- taková pasparta neexistuje --'
    nemame = '(x)'
    cena = 0
    alt2 = request.args and request.args[0] or '' # -- | 2
    pasparta_cislo = request.vars['pasparta%s_cislo' % alt2]
    if pasparta_cislo:
        pasparta = db(db.pasparta.cislo==pasparta_cislo).select().first()
        if pasparta:
            retval = '%s %s' % (
                    pasparta.cislo or '',
                    '' if pasparta.skladem else nemame)
            cena = pasparta.cena
        else:
            retval = neexistuje
    else:
        retval = ''
    return ("if ('%s'=='%s') alert('Nesprávné číslo pasparty.');"
               "$('#pasparta%s_text').text('%s');"
               "if ('%s'.slice(-3)=='%s') alert('Pasparta není skladem.');"
               "cena_pasparta%s=%s;cena();"
               % (retval, neexistuje, alt2, retval, retval, nemame, alt2, cena))

def podklad_get_cena():
    '''voláno přes ajax()'''
    cena = 0
    nemame = False
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
    cena = 0
    nemame = False
    alt2 = request.args and request.args[0] or '' # -- | 2
    sklo_id = request.vars['sklo%s_id' % alt2]
    if sklo_id:
        sklo = db.sklo[sklo_id]
        cena = sklo.cena
        nemame = not sklo.skladem
    return (("cena_sklo%s=%s;cena();" % (alt2, cena)) +
        (nemame and "alert('Sklo není skladem.');" or ""))
