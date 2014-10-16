# coding: utf8

def otevrene():
    poptavky = db(db.poptavka.vyrizeno==False).select(
          db.poptavka.ALL,
              db.poptavajici.id, db.poptavajici.jmeno,
              db.firma.zkratka,
          orderby=~db.poptavka.bude_asi,
          left=(db.poptavajici.on(db.poptavajici.id==db.poptavka.poptavajici_id),
              db.firma.on(db.firma.id==db.poptavka.firma_id))
          )
    return dict(poptavky=poptavky)
