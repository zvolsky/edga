* http://www.connectionstrings.com/
* natvrdo c:\ramovani\data - p��padn� vyedituj
* (zde nepou�ito, ale:) chci-li na 64b. ma�in� vytv��et DSN, mus�m pustit Odbcad32.exe z %systemdrive%\Windows\SysWoW64, jinak nevid�m 32b. ovlada�e

* tabulky jsou jednotliv� soubory, tak�e m�sto SQLTABLES se sta�� pod�vat na seznam soubor� v adres��i

CLEAR ALL
SET SAFETY OFF
SET EXACT OFF

hnd=SQLSTRINGCONNECT("Driver={Microsoft Paradox Driver (*.db )};DriverID=538;Fil=Paradox 5.X;DefaultDir=c:\ramovani\data;Dbq=c:\ramovani\data;CollatingSequence=ASCII;")
SQLTABLES(m.hnd, '', 'tabulky')
BROWSE
BROWSE FOR NOT LOWER(Table_name)='zkz'
SCAN FOR NOT LOWER(Table_name)='zkz'
	SQLEXEC(m.hnd, 'SELECT * FROM '+ALLTRIM(Table_name))
	BROWSE TITLE ALLTRIM(tabulky.Table_name)
ENDSCAN

SQLDISCONNECT(m.hnd)
