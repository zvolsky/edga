#!/usr/bin/env python
# coding: utf8

from w2_mz import ttt
from gluon import URL

# toto je specifické pro zákazníka; v případě, že by se implementovalo dalšímu zákazníkovi,
#  najít volání edga (např. menu.py, default.py) a vhodným způsobem vyřešit větvení

# POZOR, musí být ošetřeno na opakovaný běh, protože se spustí minimálně 2x
def init_db(db):
    #if False:   # případně implementace jiné firmy podle nějakého kritéria
    #    if ještě_neinicializováno:
    #else:       # Rámy a pasparty - původní zákazník
    if db(db.postup).count() + db(db.firma).count()==0: # ještě neinicializováno
        p1_id = db.postup.insert(nazev="RP obvyklý", hlavni=True)
        p2_id = db.postup.insert(nazev="Obrázkárna obvyklý")
        p3_id = db.postup.insert(nazev="Fotonova obvyklý")
        db.firma.insert(jmeno="Rámy a pasparty", postup_id=p1_id)
        db.firma.insert(jmeno="Obrázkárna", postup_id=p2_id)
        db.firma.insert(jmeno="Fotonova", postup_id=p3_id)

def muj_postup(db, auth):
    muj = None
    if auth.user:
        muj = auth.user.postup_id
        if not muj and auth.user.firma_id:
            firma = db.firma[auth.user.firma_id]
            if firma:
                muj = firma.postup_id
    # jakýkoli pokus semknout vše do jednoho výrazu ztroskotal,
    #    např. při vynuceném logoutu po smazání databáze - je auth.user.firma_id, ale firma==None
    if not muj:
        hlavni = db(db.postup.hlavni==True).select().first()
        if hlavni:
            muj = hlavni.id
    return muj
                     
def menu_postupy(db, postup_id):
    postupy = db(db.postup).select()
    if postup_id:
        muj = postupy.find(lambda row: row.id==postup_id).first()
    else:
        muj = None
        
    ostatni_postupy = []
    for postup in postupy:
        ostatni_postupy.append((postup.nazev, False, URL('poptavka', 'nova', args=postup.id), []))
    
    lbl = ttt("nová poptávka")  # záměrně malé první písmeno - jen v jednom případě dále .capitalize()
    if muj:
        menu_postupy = [lbl + ': ' + muj.nazev, False, URL('poptavka', 'nova', args=muj.id), ostatni_postupy]
    else:
        menu_postupy = [lbl.capitalize(), False, None, ostatni_postupy]
    return menu_postupy
