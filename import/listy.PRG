* http://www.connectionstrings.com/
* natvrdo c:\ramovani\data - p��padn� vyedituj
* (zde nepou�ito, ale:) chci-li na 64b. ma�in� vytv��et DSN, mus�m pustit Odbcad32.exe z %systemdrive%\Windows\SysWoW64, jinak nevid�m 32b. ovlada�e

CLEAR ALL
SET SAFETY OFF

hnd=SQLSTRINGCONNECT("Driver={Microsoft Paradox Driver (*.db )};DriverID=538;Fil=Paradox 5.X;DefaultDir=c:\ramovani\data;Dbq=c:\ramovani\data;CollatingSequence=ASCII;")
SQLEXEC(m.hnd,'SELECT * FROM Listy')
COPY TO c:\ramovani\data\fox\listy
SQLDISCONNECT(m.hnd)

use c:\ramovani\data\fox\listy

REPLACE ALL TYP WITH STRTRAN(Typ,'oevo','�evo')

REPLACE ALL Nazev WITH PROPER(Nazev)
REPLACE ALL Nazev WITH STRTRAN(Nazev,'x',' x ') FOR 'x'$LOWER(nazev) AND NOT 'lox'$LOWER(nazev)
REPLACE ALL Nazev WITH STRTRAN(Nazev,'X',' x ') FOR 'x'$LOWER(nazev) AND NOT 'lox'$LOWER(nazev)
REPLACE ALL Nazev WITH STRTRAN(Nazev,'  ',' ')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'  ',' ')

REPLACE ALL Nazev WITH STRTRAN(Nazev,'oech','�ech')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'ao�','a��')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'to�bro','t��bro')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'lu?','lu�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'omerane','omeran�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'kooic','ko�ic')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'o�rod','��rod')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'eer','�er')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'to�br','t��br')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'mavi','mav�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'vitl','v�tl')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'pal�eek','pal��ek')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'oen','o�n')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'Modo','Mod�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'modo','mod�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'ostiek','osti�k')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'ovi ','ov� ')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'oevin','�ev�n')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'niton','nit�n')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'�minn','�m�nn')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'ilen','�len')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'to�r','t��br')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'oev','�ev')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'oe�eo','�e�e�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'7eero','7 �er�')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'Eer','�er')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'hnid','hn�d')
REPLACE ALL Nazev WITH STRTRAN(Nazev,'Hnid','Hn�d')
