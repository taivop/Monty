Monty

Autorid: Anti Ingel, Taivo Pungas, Oliver Viljamaa
Tartu �likool, 2014

Monty on 2014. aasta kevadsemestril aine Automaadid, keeled ja translaatorid (MTAT.05.085) raames tehtud projekt, mille eesm�rgiks on lihtsustada programmeerimise �ppimist.

Programm kujutab endast analoogselt Scratchile v�i Code.org-ile ala, millele kindlate funktsioonidega klotse vedades ja omavahel kombineerides koostatakse vastav programmijupp, mida k�rvalaknas ka kuvatakse. See muudab tutvumise nii programmeerimisega kui ka konkreetselt keelega Python lihtsamaks ja l�busamaks.

Eeldused:
* Python 3.1.1 - allalaetav: https://www.python.org/download/releases/3.1.1
* Pygame 1.9.1 for Python 3.1 - allalaetav: http://pygame.org/download.shtml
(Muud Python 3 või Pygame versioonid võivad töötada, aga ei ole testitud.)

Kasutamine:

1. Monty k�ivitamiseks tuleb Pythoni 3.1 versioonis jooksutada faili gui/monty.py.
2. Programmi kasutamine:
	* vasakul servas on erinevad nupud, mis on jaotatud gruppidesse
	* esimese grupi klotsidele vajutades v�i nendelt vedades ilmub alale vastava funktsiooniga klots
	  (klotse saab tekitada ka funktsiooniklahvidega)
	* teise grupi klotsid on analoogsed, kuid vastavad Pythoni turtle joonistusteegi lihtsamatele k�skudele
	* kolmanda grupi klotsid kujutavad endast �ldiseid k�ske programmi salvestamiseks, stseeni vahetuseks
	  (et hallata saaks mitut programmijuppi), tagasiliikumiseks, ekraani klotsidest t�hjendamiseks ning v�ljumiseks
	* klotsid tuleb programmi osaks tegemiseks lohistada ekraani �lalosas olevate kolmnurkadeni
	* klotsidel olevaid kaste saab t�ita vastavate v��rtustega, n�iteks kordusts�kli ehk for-ts�kli puhul
	  v��rtustatud muutujaga v�i t�isarvuga
	* aktiivse tekstikasti tunneb kasutaja �ra valge ��re j�rgi ning kahe kastiga klotsidel t��tab kastivahetuseks TAB-nupp
	* klotse �ksteise peale lohistades klotsid haakuvad ning grupi k�ige �lemisest klotsist vedades liiguvad k�ik
	* klotsi kustutamiseks v�ib aktiivse klotsi (klotsi, millel olev kast on valge) kustutada vajutades DELETE-nuppu
	  v�i lohistades selle all paremas nurgas oleva pr�gikastini
	* paremal �leval nurgas kuvatakse klotsidest valmistatud programmile vastavat Python-koodi, mida uuendatakse iga muutuse j�rel
	* vajutades nuppu "K�ivita!" v�i vajutades ENTER-klahvi kuvatakse ka vastava programmi v�ljundit v�i vea puhul lihtsaid soovitusi
	* programmist saab v�ljuda kas vasakul all servas olevat "V�lju" nuppu vajutades, ESC-klahvi vajutades v�i programmi ristist sulgedes

Koodist:

* programmi kood on k�ttesaadav GitHubi repositooriumist aadressil https://github.com/taivop/Monty
* kood ja erinevad lisafailid on jaotatud erinevatesse kaustadesse vastavalt faili t��pidele ja sisule


Tehniline pool:

P�rast sisendikontrolli genereerib Monty igale klotsile vastava koodirea. Neid ridu n�idatakse kasutajale ekraanil ja nupu "K�ivita!" vajutamisel proovib Monty programmi k�ivitama hakata.
K�ivitamise protsess n�eb v�lja selline:
	1. Pythoni AST teegi abil teeb Monty programmikoodist abstraktse s�ntaksipuu.
	2. Abstraktne s�ntaksipuu kompileeritakse...
	3. ...ja seej�rel k�ivitatakse.
Kui �ksk�ik millises neist sammudest tekib erind, p��ab Monty selle kinni ja annab kasutajale erindist teada programmi v�ljundikastis.v�ljundi kastis punase tekstiga.

Monty l�htekood on jaotatud kahte moodulisse. Moodul gui tegeleb kogu graafilise liidese joonistamise ja haldamisega - see moodustab suurema osa programmi koodist. Moodulist language olevad klassid, peamiselt CodeRunner, tegelevad koodi jooksutamisega.

Koodi lugemist v�ib alustada klassist gui/blocks.py - seal on defineeritud k�ik kasutatavad klotsid ning nende v�ljastatav kood. Graafilist liidest haldav kood on gui/monty.py-s, erinevad graafilised objektid ja nendega seotud meetodid on vastava nimega kastides. Failis CodeBox.py on kood, mille abil genereeritakse ja joonistatakse rakenduse parempoolses ribas olev programmi kood ja programmi v�ljund.
