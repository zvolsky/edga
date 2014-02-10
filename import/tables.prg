* http://www.connectionstrings.com/
* natvrdo c:\ramovani\data - pøípadnì vyedituj
* (zde nepoužito, ale:) chci-li na 64b. mašinì vytváøet DSN, musím pustit Odbcad32.exe z %systemdrive%\Windows\SysWoW64, jinak nevidím 32b. ovladaèe

* tabulky jsou jednotlivé soubory, takže místo SQLTABLES se staèí podívat na seznam souborù v adresáøi

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
