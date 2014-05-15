# -*- coding: utf-8 -*-

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

    db.define_table('barva',
            Field('barva', 'string', length=40, label=ttt('Název barvy')),
            singular="Barva", plural="Barvy",
            format='%(barva)s',
            )

    db.define_table('lista',
            Field('hlavni', 'boolean', default=False, label=ttt('Předvolený typ')),
            Field('vyrobce', default='', label=ttt('Výrobce')),
            Field('typ', default='', label=ttt('Typ')),
            Field('nazev', default='', label=ttt('Název')),
            Field('cislo', default='', label=ttt('Číslo')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('tovarni', default='', label=ttt('Tovární číslo')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            Field('sirka', 'decimal(6,1)', default=0.0, label=ttt('Šířka (tloušťka) [cm]')),
            Field('nakupni', 'decimal(8,2)', default=0.0, label=ttt('Nákupní cena')),
            singular="Lišta", plural="Lišty",
            format='%(cislo)s %(typ)s %(nazev)s %(vyrobce)s %(tovarni)s (Kč %(cena)s)',
            )
    '''
            Field('zobrazit', default='', label=TFu('Zobrazit text')),
            Field('maxsirka', 'decimal(6,1)', default=0.0, label=TFu('Max. šířka [cm]')),
            Field('maxdelka', 'decimal(6,1)', default=0.0, label=TFu('Max. délka [cm]')),
            Field('maxvyska', 'decimal(6,1)', default=0.0, label=TFu('Max. výška [cm]')),
            Field('cena2', 'decimal(8,2)', default=0.0, label=TFu('Cena 2 (okraje)')),
            Field('prorez', default='', label=TFu('Prořez')),
            Field('sirkaprofilu', 'decimal(6,1)', default=0.0,
                    label=TFu('Šířka profilu [cm]')),
            Field('vyskaprouzku', 'decimal(6,1)', default=0.0,
                    label=TFu('Výška proužku [cm]')),
            Field('samolepka', 'boolean', default=False, label=TFu('Samolepka')),
            Field('bezpecnasirka', 'decimal(6,1)', default=0.0,
                    label=TFu('Bezpečná šířka [cm]')),
            Field('bezpecnadelka', 'decimal(6,1)', default=0.0,
                    label=TFu('Bezpečná délka [mm]')),
            Field('bezpecnavyska', 'decimal(6,1)', default=0.0,
                    label=TFu('Bezpečná výška [cm]')),
            Field('kazeta', default='', label=TFu('Kazeta (vitrína)')),
            Field('gramaz', 'decimal(8,2)', default=0.0, label=TFu('Gramáž (gsm) [g/m2]')),
            '''

    db.define_table('lista_bv',
            Field('lista_id', db.lista, label=ttt('Typ lišty'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.lista.id, db.lista._format)),
                represent=lambda id, r=None: db.lista._format % db.lista(id) if id else '',
                ondelete='SET NULL'),
            Field('barva_id', db.barva, label=ttt('Barva'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.barva.id, db.barva._format)),
                represent=lambda id, r=None: db.barva._format % db.barva(id) if id else '',
                ondelete='NO ACTION'),
            Field('cislo', default='', label=ttt('Číslo')),
            singular="Lišta (bar.varianty)", plural="Lišty (bar.varianty)",
            format='%(cislo)s %(barva)s',
            )

    db.define_table('pasparta',
            Field('typ', default='', label=ttt('Typ')),
            singular="Pasparta", plural="Pasparty",
            format='%(typ)s',
            )

    db.define_table('pasparta_bv',
            Field('pasparta_id', db.pasparta, label=ttt('Typ pasparty'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.pasparta.id, db.pasparta._format)),
                represent=lambda id, r=None: db.pasparta._format % db.pasparta(id) if id else '',
                ondelete='SET NULL'),
            Field('barva_id', db.barva, label=ttt('Barva'),
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.barva.id, db.barva._format)),
                represent=lambda id, r=None: db.barva._format % db.barva(id) if id else '',
                ondelete='NO ACTION'),
            Field('cislo', default='', label=ttt('Číslo')),
            singular="Pasparta (bar.varianty)", plural="Pasparty (bar.varianty)",
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
