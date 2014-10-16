# coding: utf8

'''vse() : truncate/naplní/inicializuje tabulky (seznam viz smaz_zaznamy())
dph() : sníží všechny ceny o dph (s cen s DPH udělá ceny bez DPH)
'''

dph_koef = 1.21

def dph():
    db(db.lista).update(cena=db.lista.cena/dph_koef)
    db(db.pasparta_rozmer).update(cena=db.pasparta_rozmer.cena/dph_koef)
    db(db.podklad).update(cena=db.podklad.cena/dph_koef)
    db(db.sklo).update(cena=db.sklo.cena/dph_koef)
    db(db.blintram).update(cena=db.blintram.cena/dph_koef)
    db(db.platno).update(cena=db.platno.cena/dph_koef)
    db.commit()

def vse():
    smaz_zaznamy()
    standard_barvy = sady_barev()
    barvy(standard_barvy)
    rozmery()
    pasparty(standard_barvy)
    pasparty_ceny()
    kusovky()

def smaz_zaznamy():
    db.sada_barev.truncate()
    db.barva.truncate()
    db.rozmer.truncate()
    db.pasparta.truncate()
    db.pasparta_rozmer.truncate()
    db.barva_nelze.truncate()  # neplním; ale s ohledem na možné změny ID
    db.kspasp.truncate()
    db.ksmat.truncate()
    db.commit()

def kusovky():
    db.kspasp.insert(nazev=ttt("okno navíc", cena=48.0))
    db.ksmat.insert(nazev=ttt("háček obyč."))
    db.ksmat.insert(nazev=ttt("závěs"))
    db.commit()

def sady_barev():
    standard_barvy = db.sada_barev.insert(nazev=ttt("standardní"))
    db.commit()
    return standard_barvy

def barvy(sada_barev):
    db.barva.insert(barva="bílá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="šedá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="černá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="červená", sada_barev_id=sada_barev)     
    db.barva.insert(barva="zelená", sada_barev_id=sada_barev)     
    db.barva.insert(barva="hnědá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="modrá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="žlutá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="oranžová", sada_barev_id=sada_barev)     
    db.barva.insert(barva="béžová", sada_barev_id=sada_barev)     
    db.barva.insert(barva="růžová", sada_barev_id=sada_barev)     
    db.barva.insert(barva="tyrkysová", sada_barev_id=sada_barev)     
    db.barva.insert(barva="světle hnědá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="světle modrá", sada_barev_id=sada_barev)     
    db.barva.insert(barva="světle zelená", sada_barev_id=sada_barev)     
    db.commit()

def rozmery():
    db.rozmer.insert(sirka=20.0, vyska=25.0)
    db.rozmer.insert(sirka=25.0, vyska=35.0)
    db.rozmer.insert(sirka=30.0, vyska=45.0)
    db.rozmer.insert(sirka=35.0, vyska=50.0)
    db.rozmer.insert(sirka=40.0, vyska=60.0)
    db.rozmer.insert(sirka=50.0, vyska=70.0)
    db.rozmer.insert(sirka=60.0, vyska=85.0)
    db.rozmer.insert(sirka=70.0, vyska=100.0)
    db.rozmer.insert(sirka=80.0, vyska=120.0)
    db.rozmer.insert(sirka=101.0, vyska=151.0)
    db.rozmer.insert(sirka=122.0, vyska=170.0)
    db.commit()
    
def pasparty(sada_barev):
    #db.pasparta.insert(typ="Fram", sada_barev_id=sada_barev)     
    db.pasparta.insert(typ="Nielsen", sada_barev_id=sada_barev)     
    db.pasparta.insert(typ="Obrazová pasparta", sada_barev_id=sada_barev)     
    db.pasparta.insert(typ="Lem+Sklo+Podklad", sada_barev_id=sada_barev)     
    db.pasparta.insert(typ="Komplet", sada_barev_id=sada_barev)     
    db.pasparta.insert(typ="Kliprám", sada_barev_id=sada_barev)     
    db.commit()

def pasparty_ceny():
    ceny = (
      (160.0, 195.0, 232.0, 290.0, 370.0, 414.0, 576.0, 620.0, 850.0, 0.0, 0.0),
      (79.0, 97.0, 130.0, 165.0, 210.0, 237.0, 320.0, 375.0, 400.0, 490.0, 0.0),
      (66.0, 79.0, 92.0, 105.0, 124.0, 131.0, 145.0, 156.0, 165.0, 275.0, 0.0),
      (187.0, 195.0, 260.0, 270.0, 335.0, 356.0, 456.0, 495.0, 550.0, 700.0, 0.0),
      (50.0, 60.0, 90.0, 100.0, 120.0, 120.0, 150.0, 210.0, 300.0, 500.0, 0.0),
      )
    for no, pasparta in enumerate(db(db.pasparta).select()):
        pasparta_ceny(pasparta.id, ceny[no])
    db.commit()

def pasparta_ceny(pasparta_id, ceny):
    for no, rozmer in enumerate(db(db.rozmer).select()):
        db.pasparta_rozmer.insert(
                pasparta_id=pasparta_id,
                rozmer_id=rozmer.id,
                cena=ceny[no])
