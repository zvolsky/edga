* http://www.connectionstrings.com/
* natvrdo c:\ramovani\data - p��padn� vyedituj
* (zde nepou�ito, ale:) chci-li na 64b. ma�in� vytv��et DSN, mus�m pustit Odbcad32.exe z %systemdrive%\Windows\SysWoW64, jinak nevid�m 32b. ovlada�e

* tabulky jsou jednotliv� soubory, tak�e m�sto SQLTABLES se sta�� pod�vat na seznam soubor� v adres��i

CLEAR ALL
SET SAFETY OFF
SET EXCLUSIVE ON
SET EXACT OFF
SET DELETED OFF

LOCAL hnd, tbl, podklad
LOCAL ARRAY aCeny[1]

ERASE pasparta.dbf
ERASE podklad.dbf
ERASE sklo.dbf
CREATE TABLE pasparta FREE (Oznaceni C(20), Cena N(8,2))
CREATE TABLE podklad FREE (Oznaceni C(20), Cena N(8,2))
CREATE TABLE sklo FREE (Oznaceni C(20), Cena N(8,2))

hnd=SQLSTRINGCONNECT("Driver={Microsoft Paradox Driver (*.db )};DriverID=538;Fil=Paradox 5.X;DefaultDir=c:\ramovani\data;Dbq=c:\ramovani\data;CollatingSequence=ASCII;")
SQLEXEC(m.hnd, 'SELECT * FROM Ceny')
* v�echny ceny jsou narv�ny v prvn�m z�znamu; je tam je�t� druh�, ale v n�m t�m�� v�hradn� NULL
FOR i=1 TO AFIELDS(aCeny)
	DO CASE
		CASE aCeny(i,1)='PASP'
			tbl = 'pasparta'
			jmeno = SUBSTR(aCeny(i,1), 5)
		CASE aCeny(i,1)='PODKLAD'
			tbl = 'podklad'
			jmeno = SUBSTR(aCeny(i,1), 8)
		CASE aCeny(i,1)='SKLO'
			tbl = 'sklo'
			jmeno = SUBSTR(aCeny(i,1), 5)
		OTHERWISE
			LOOP
	ENDCASE
	nVal = EVALUATE(ALIAS()+'.'+aCeny(i,1))
	IF	NOT ISNULL(m.nVal)
		IF	EMPTY(m.jmeno)
			jmeno = 'Normal'
		ENDIF
		INSERT INTO (m.tbl) (Oznaceni, Cena) VALUES (m.jmeno, m.nVal)
	ENDIF
ENDFOR

SQLDISCONNECT(m.hnd)

SELECT pasparta
BROWSE
PACK
SELECT podklad
BROWSE
PACK
SELECT sklo
BROWSE
PACK
