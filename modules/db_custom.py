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
                requires=IS_EMPTY_OR(IS_IN_DB(db, db.postup.id, '%(nazev)s'))),
        ]

def after(db, Field, auth):
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

    db.define_table('pasparta',
            Field('cislo', default='', label=ttt('Číslo')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            )

    db.define_table('podklad',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            format='%(nazev)s',
            )

    db.define_table('sklo',
            Field('nazev', default='', label=ttt('Název')),
            Field('cena', 'decimal(8,2)', default=0.0, label=ttt('Cena')),
            Field('skladem', 'boolean', default=True, label=ttt('Skladem')),
            format='%(nazev)s',
            )
