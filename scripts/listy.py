# -*- coding: utf-8 -*-

__all__ = ['preved2bv']

def preved2bv():
    '''vybere unikátní lišty podle vyrobce,typ,cena,sirka
    poté smaž (v definici db_custom.py) pole cislo,nazev,skladem
    '''
    
    db.lista_bv.truncate()
    db.barva_list.truncate()
    db.commit()
    
    barvy = db(db.barva_list).select()
    mbarvy = {}
    for barva in barvy:
        mbarvy[barva.barva] = barva.id
 
    listy = db(db.lista).select()
    zustanou = {}
    for lista in listy:
        lista_id = __ktera(lista, zustanou)
        if lista_id:
            del db.lista[lista.id]
        else:
            lista_id = lista.id
            
        barva_id = mbarvy.get(lista.nazev)
        if not barva_id:
            barva_id = db.barva_list.insert(barva=lista.nazev)
            mbarvy[lista.nazev] = barva_id 
            
        db.lista_bv.insert(
                lista_id=lista_id,
                cislo=lista.cislo,
                tovarni=lista.tovarni,
                barva_list_id=barva_id,
                barva=lista.nazev,
                skladem=lista.skladem,
                )
        koren = db.lista[lista_id]
        if koren.tovarni and koren.tovarni!=lista.tovarni:
            db.lista[lista_id] = dict(tovarni='')
        if not koren.nakupni and lista.nakupni:
            db.lista[lista_id] = dict(nakupni=lista.nakupni)             
    db.commit()

def __ktera(lista, zustanou):
    '''už je v zustanou: vrátit id ze zustanou
    není v zustanou: přidat do zustanou a vrátit 0
    '''
    o_liste = '%s %s %s %s' % (lista.vyrobce, lista.typ, lista.cena, lista.sirka)
    hash_lista = hash(o_liste)
    if zustanou.get(hash_lista):
        return zustanou[hash_lista]
    else:
        zustanou[hash_lista] = lista.id
        return 0

if __name__=="__main__":
    preved2bv()