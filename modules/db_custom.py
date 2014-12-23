# -*- coding: utf-8 -*-

import datetime

#migrate=False,fake_migrate=True

from gluon.validators import IS_NOT_EMPTY, IS_IN_DB, IS_EMPTY_OR
from w2_mz import ttt

def before(db, Field, auth):
    db.define_table('postup',         # postupy = seznamy prací pro poptávky
            Field('nazev', label=ttt('Název'),
                    comment=ttt("název postupu - výčtu prací"),
                    requires=IS_NOT_EMPTY()),
            Field('hlavni', 'boolean', label=ttt('Předvolený postup'),
                    comment=ttt("postup se předvolí pro nové poptávky, není-li žádný nastaven pro uživatele")),
            singular="Postup", plural="Postupy",
            format='%(nazev)s',
            )
    '''
            Field('maska_id', 'string', label=ttt('div-id'),
                    comment=ttt("div-id této masky"),
                    writable=False),
            Field('maska', 'text', label=ttt('Maska'),
                    comment=ttt("HTML masky s procento_s"),
                    writable=False),
            Field('maska_flds', 'string', label=ttt('Pole v masce'),
                    comment=ttt("které údaje promítá maska (oddělit čárkami)"),
                    writable=False),                                
            Field('hardcoded_as', 'string', length=1, label=ttt('Hardkód HTML'),
                    comment=ttt("*|o|r|f pro hardkódované masky"),
                    writable=False),
            '''
    
    db.define_table('firma',
            Field('postup_id', db.postup, label=ttt('Hlavní postup'),
                    comment=ttt("pro firmu typický výrobní postup")),
            Field('zkratka', length=4, label=ttt('Zkratka')),
            Field('jmeno', label=ttt('Jméno'), requires=IS_NOT_EMPTY()),
            singular="Firma", plural="Firmy",
            format='%(jmeno)s',
            )
    '''
            Field('obprefix', length=3, label=ttt('Prefix číselné řady')),
            Field('obno', 'integer', default=0,
                    label=ttt('Poslední použité číslo řady')),
            Field('obrok', 'integer', default=0, label=ttt('Rok číslování řady')),
            Field('funkce', label=ttt('Funkce'),
                    comment=ttt("Pojmenování function pro kontrolér typypraci")),
            '''
    
    ## create all tables needed by auth if not custom tables
    auth.settings.extra_fields['auth_user'] = [
        Field('firma_id', db.firma, label=ttt('Firma')),
        Field('postup_id', db.postup, label=ttt('Obvyklý postup'),
                comment=ttt("předvolený výrobní postup (není-li uveden, vezme se podle firmy)"),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.postup.id, db.postup._format))),
        ]

def after(db, Field, auth):
    '''
    db.define_table('sada_barev',
            Field('nazev', 'string', length=40, label=ttt('Název sady barev')),
            singular="Sada barev", plural="Sady barev",
            format='%(nazev)s',
            )
    z barva: Field('sada_barev_id', db.sada_barev, label=ttt('Sada barev')),
    z pasparta: Field('sada_barev_id', db.sada_barev, label=ttt('Sada barev'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.sada_barev.id, db.sada_barev._format)),
                represent=lambda id, r=None: db.sada_barev._format % db.sada_barev(id) if id else '',
                ondelete='SET NULL'),

    db.define_table('barva_nelze',
            Field('pasparta_id', db.pasparta, label=ttt('Typ pasparty')),
            Field('barva_id', db.barva, label=ttt('Barva')),
            Field('rozmer_id', db.rozmer, label=ttt('Jen do max. rozměru'),
                comment=ttt('Je-li omezen formát, zadej největší, který se dodává'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.rozmer.id, db.rozmer._format)),
                represent=lambda id, r=None: db.rozmer._format % db.rozmer(id) if id else '',
                ondelete='SET NULL'),
            Field('skladem', 'boolean', default=False, label=ttt('Skladem'),
                comment=ttt('Ponechej nezaškrtnuté, jestliže ji právě nemáme v žádném rozměru')),
            singular="Nedostupná barva", plural="Nedostupné barvy",
            )
            # barva musí být ze sady barev dané pasparty
            # skladem.default=False a jen =False záznamy mají význam,
            #   a sice, že "tato barva pro tuto paspartu momentálně není"

    z lista_bv a z pasparta_bv:
    Field('barva', 'string', length=40, label=ttt('Název barvy')),
    '''

    db.define_table('barva_list',
            Field('barva', default='', label=ttt('Barva')),
            singular="Barva lišt", plural="Časté barvy lišt",
            format='%(barva)s',
            )

    db.define_table('barva_paspart',
            Field('barva', 'string', length=40, label=ttt('Název barvy')),
            singular="Barva paspart", plural="Časté barvy paspart",
            format='%(barva)s',
            )

    db.define_table('lista',
            Field('hlavni', 'boolean', default=False, readable=False, writable=False, label=ttt('Předvolený typ')),
            Field('typ', default='', label=ttt('Název')),
            Field('vyrobce', default='', label=ttt('Výrobce')),
            Field('tovarni', default='', label=ttt('Tovární číslo')),
            Field('sirka', 'decimal(6,1)', default=0.0, label=ttt('Šířka (tloušťka) [cm]')),
            Field('nakupni', 'decimal(8,2)', default=0.0, label=ttt('Nákupní cena')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('cena_plan', 'decimal(8,2)', readable=False, writable=False, default=0.0, label=ttt('Plánovaná cena')),


            Field('nazev', default='', readable=False, writable=False, label=ttt('Nazev')),
            Field('zobrazit', default='', readable=False, writable=False, label=ttt('Zobrazit text')),
            Field('maxsirka', 'decimal(6,1)', default=0.0, readable=False, writable=False, label=ttt('Max. šířka [cm]')),
            Field('maxdelka', 'decimal(6,1)', default=0.0, readable=False, writable=False, label=ttt('Max. délka [cm]')),
            Field('maxvyska', 'decimal(6,1)', default=0.0, readable=False, writable=False, label=ttt('Max. výška [cm]')),
            Field('cena2', 'decimal(8,2)', default=0.0, readable=False, writable=False, label=ttt('Cena 2 (okraje)')),
            Field('prorez', default='', readable=False, writable=False, label=ttt('Prořez')),
            Field('sirkaprofilu', 'decimal(6,1)', default=0.0, readable=False, writable=False,
                    label=ttt('Šířka profilu [cm]')),
            Field('vyskaprouzku', 'decimal(6,1)', default=0.0, readable=False, writable=False,
                    label=ttt('Výška proužku [cm]')),
            Field('samolepka', 'boolean', default=False, readable=False, writable=False, label=ttt('Samolepka')),
            Field('bezpecnasirka', 'decimal(6,1)', default=0.0, readable=False, writable=False,
                    label=ttt('Bezpečná šířka [cm]')),
            Field('bezpecnadelka', 'decimal(6,1)', default=0.0, readable=False, writable=False,
                    label=ttt('Bezpečná délka [mm]')),
            Field('bezpecnavyska', 'decimal(6,1)', default=0.0, readable=False, writable=False,
                    label=ttt('Bezpečná výška [cm]')),
            Field('kazeta', default='', readable=False, writable=False, label=ttt('Kazeta (vitrína)')),
            Field('gramaz', 'decimal(8,2)', default=0.0, readable=False, writable=False, label=ttt('Gramáž (gsm) [g/m2]')),

            Field('barva', default='', readable=False, writable=False, label=ttt('Barva')),
            Field('cislo', default='', readable=False, writable=False, label=ttt('Číslo')),
            Field('skladem', 'boolean', default=True, readable=False, writable=False, label=ttt('Skladem')),


            singular="Typ lišty", plural="Typy lišt",
            format='%(typ)s %(vyrobce)s %(tovarni)s (Kč %(cena)s)',
            )

    db.define_table('lista_bv',
            Field('lista_id', db.lista, writable=False, label=ttt('Typ lišty'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.lista.id, db.lista._format)),
                represent=lambda id, r=None: db.lista._format % db.lista(id) if id else '',
                ondelete='CASCADE'),
            Field('barva_list_id', db.barva_list, readable = False, writable = False, label=ttt('Barva'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.barva_list.id, db.barva_list._format)),
                represent=lambda id, r=None: db.barva_list._format % db.barva_list(id) if id else '',
                ondelete='SET NULL'),
            Field('barva', default='', label=ttt('Barva'), comment=ttt('neměň barvu! místo toho přidej novou a tuto označ, že není skladem')),
            Field('cislo', length=20, default='', label=ttt('Číslo')),
            Field('cislo_sort', length=20, readable=True, writable=True, label=ttt('Číslo(tříd.)'),
                compute=lambda r: (20*' '+r['cislo'])[-20:] if r['cislo'].isdigit() else r['cislo']),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Lišta", plural="Lišty (barev.varianty)",
            format='%(cislo)s %(barva)s',
            )

    db.define_table('pasparta',
            Field('typ', default='', label=ttt('Název')),
            Field('cena_okna', 'decimal(8,2)', default=0.0, label=ttt('Cena okna navíc')),
            singular="Typ pasparty", plural="Typy paspart",
            format='%(typ)s',
            )

    db.define_table('pasparta_bv',
            Field('pasparta_id', db.pasparta, writable=False, label=ttt('Typ pasparty'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.pasparta.id, db.pasparta._format)),
                represent=lambda id, r=None: db.pasparta._format % db.pasparta(id) if id else '',
                ondelete='CASCADE'),
            Field('barva_paspart_id', db.barva_paspart, readable=False, writable=False, label=ttt('Barva'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.barva_paspart.id, db.barva_paspart._format)),
                represent=lambda id, r=None: db.barva_paspart._format % db.barva_paspart(id) if id else '',
                ondelete='SET NULL'),
            Field('barva', default='', label=ttt('Barva'), comment=ttt('neměň barvu! místo toho přidej novou a tuto označ, že není skladem')),
            Field('cislo', length=20, default='', label=ttt('Číslo')),
            Field('cislo_sort', length=20, readable=True, writable=True, label=ttt('Číslo(tříd.)'),
                compute=lambda r: (20*' '+r['cislo'])[-20:] if r['cislo'].isdigit() else r['cislo']),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Pasparta", plural="Pasparty (barev.varianty)",
            format='%(cislo)s %(barva)s',
            )

    db.define_table('rozmer',
            Field('sirka', 'decimal(6,1)', default=0.0, label=ttt('Šířka')),
            Field('vyska', 'decimal(6,1)', default=0.0, label=ttt('Výška')),
            singular="Mezní rozměr", plural="Mezní rozměry",
            format='%(sirka)s x %(vyska)s',
            )

    db.define_table('pasparta_rozmer',
            Field('pasparta_id', db.pasparta, label=ttt('Typ pasparty')),
            Field('rozmer_id', db.rozmer, label=ttt('Do hraničního rozměru')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            singular="Cena podle rozměru", plural="Ceny podle rozměru",
            )

    db.define_table('podklad',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Podklad", plural="Podklady",
            format='%(nazev)s',
            )

    db.define_table('sklo',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Sklo", plural="Skla",
            format='%(nazev)s',
            )

    db.define_table('blintram',
            Field('nazev', default='', label=ttt('Název')),
            Field('vzpery_po', 'decimal(6,1)', default=70.0, label=ttt('Vzpěry po [cm]')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Blintrám lišta", plural="Blintrám lišty",
            format='%(nazev)s',
            )

    db.define_table('platno',
            Field('nazev', default='', label=ttt('Název')),
            Field('presah', 'decimal(6,1)', default=7.0, label=ttt('Přesah pro uchycení na rubu [cm]')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Plátno", plural="Plátna",
            format='%(nazev)s',
            )

    db.define_table('zaves',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Závěs", plural="Zavěšení",
            format='%(nazev)s',
            )

    db.define_table('ksmat',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            singular="Kusový doplněk", plural="Kusové doplňky",
            format='%(nazev)s',
            )

    db.define_table('kspasp',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            singular="Kusový doplněk paspart", plural="Kusové doplňky paspart",
            format='%(nazev)s',
            )

    #-----------------------------------------------------------
    db.define_table('poptavajici',
            Field('jmeno', length=128, label=ttt('Příjmení+Jméno nebo Název')),
            Field('telefon', length=16, label=ttt('Telefon')),
            Field('telefon2', length=16, label=ttt('Telefon (další)')),
            Field('email', length=64, label=ttt('E-mail')),
            Field('poznamka', 'text', label=ttt('Poznámka')),
            format='%(jmeno)s',
            )

    db.define_table('poptavka',
            Field('poptavajici_id', db.poptavajici, writable=False),
            Field('firma_id', db.firma),
            Field('zalozeno', 'datetime', default=datetime.datetime.now(), writable=False),            
            Field('pozastavit', 'boolean'),
            Field('bude_asi', 'datetime'),
            Field('hotovo', 'datetime'),
            Field('vyzvednuto', 'datetime'),
            Field('dosud_uhrazeno', 'integer'),
            Field('naposled_platil', 'datetime'),
            Field('poznamka', 'text'),
            Field('vyrizeno', 'boolean'),
            )

    nemame = ' (x)'
    db.define_table('rp',
            Field('poptavka_id', db.poptavka, default=None, writable=False),
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
            #Field('pasparta_id', db.pasparta,
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
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('podklad_poznamka', 'text'),
            Field('podklad2_id', db.podklad,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.podklad.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('podklad2_poznamka', 'text'),
            Field('sklo_id', db.sklo,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('sklo_poznamka', 'text'),
            Field('sklo2_id', db.sklo,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.sklo.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('sklo2_poznamka', 'text'),
            Field('blintram_id', db.blintram,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.blintram.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('blintram_vzper_sirka', 'integer', default=0),
            Field('blintram_vzper_vyska', 'integer', default=0),
            Field('blintram_poznamka', 'text'),
            Field('platno_id', db.platno,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.platno.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('platno_poznamka', 'text'),
            Field('zaves_ks', 'integer', default=1),
            Field('zaves_id', db.zaves,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.zaves.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
            Field('zaves_poznamka', 'text'),
            Field('ksmat_ks', 'integer', default=1),
            Field('ksmat_id', db.ksmat,
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.ksmat.id,
                lambda r: r.nazev + ('' if r.skladem else nemame)))),
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
            )