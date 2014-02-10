#!/usr/bin/env python
# -*- coding: utf8 -*-

u'''
import Pasparty, Podklady, Skla z FoxPro tabulky
script spustit příkazem: python web2py.py -a "pwd" -M -S edga -R applications/edga/import/ostatni.py

http://www.connectionstrings.com/
natvrdo c:\ramovani\data - případně vyedituj
(zde nepoužito, ale:) chci-li na 64b. mašině vytvářet DSN, musím pustit Odbcad32.exe z %systemdrive%\Windows\SysWoW64, jinak nevidím 32b. ovladače
FoxPro ODBC driver: http://download.microsoft.com/download/vfoxodbcdriver/Install/6.1/W9XNT4/EN-US/VFPODBC.msi
'''

folder_src = r"c:\python27\Lib\site-packages\web2py\applications\edga\import"
    # zadat relativně k web2py (viz spouštění: import.txt) se mi nepovedlo, proto absolutní cesta

import pyodbc
from decimal import Decimal

def fox_table(folder, table): 
    cnxn = pyodbc.connect(r"Driver={{Microsoft Visual FoxPro Driver}};SourceType=DBF;SourceDB={0};Exclusive=No;Collate=Machine;NULL=NO;DELETED=NO;BACKGROUNDFETCH=NO;".format(folder), autocommit=True) 
    # r"Driver={{Microsoft...}};DefaultDir={0}".format(r'c:\ramovani\data') 
        # pyodbc.connect(r"Driver={Microsoft Paradox Driver (*.db )};DriverID=538;Fil=Paradox 5.X;DefaultDir=c:\ramovani\data;Dbq=c:\ramovani\data;CollatingSequence=ASCII;", autocommit=True)
    cursor = cnxn.cursor()
    cursor.execute("select * from %s" % table)
    rows=cursor.fetchall()
    for i, row in enumerate(rows):
        for j, fld in enumerate(row):
            if isinstance(fld, str):
                # fld = fld.strip() nelze! immutable - založí jiný objekt
                rows[i][j] = fld.strip()
    # cnxn.commit()
    cnxn.close()
    return rows

def import_ostatni_rp():
    fox_1 = fox_table(folder_src, "pasparta")
    import_ostatni_1b(db.pasparta, fox_1)
    fox_1 = fox_table(folder_src, "podklad")
    import_ostatni_1(db.podklad, fox_1)
    fox_1 = fox_table(folder_src, "sklo")
    import_ostatni_1(db.sklo, fox_1)
    db.commit()
    
def import_ostatni_1(tbl, fox_rows):   # nazev
    tbl.truncate()
    for fox_row in fox_rows:
        # OZNACENI, CENA
        tbl.insert(
              nazev =(fox_row[0] or '').decode('cp1250'),
              cena = fox_row[1],
              skladem = True
              )    
def import_ostatni_1b(tbl, fox_rows):   # cislo
    tbl.truncate()
    for fox_row in fox_rows:
        # OZNACENI, CENA
        tbl.insert(
              cislo =(fox_row[0] or '').decode('cp1250'),
              cena = fox_row[1],
              skladem = True
              )    
    
if __name__=='__main__':
    import_ostatni_rp()
