Djangoproject.cz -- ceske preklady oficialni dokumentace frameworku Django.

Pro rozjeti aplikace je treba:

* na urovni adresare `djcz` vytvorit adresar `docs` s obsahem oficialni dokumentace Djanga
  (https://github.com/django/django/tree/master/docs)
* v adresari `djcz/` vytvorit soubor `local_settings.py` s udaji pro pripojeni k databazi,
  konstantu `AKISMET_API_KEY` pro ochranu komentaru pred SPAMem, konstanty `ADMINS`, 
	`MANAGERS` a `SECRET_KEY` (viz oficialni Django dokumentace) a konstantu `SPAMMER_IP` se
	seznamem IP adres, kterym se uplne zamezi vstup na stranky (toto byla reakce na masivni
	SPAMovani z Ruska)

Po syncnuti aplikace s databazi je mozne do ni nalit obsah ze souboru `djcz/data.json`
(obsah ofiko webu k 12.10.2012 bez komentaru). Pristupova hesla vsech uzivatelu jsou 
nastavena na 'heslo'.

Upozorneni
==========

Projekt [djangoproject.cz](http://djangoproject.cz) vznikl v roce 2008, v dobe, kdy 
zdrojove kody Djanga byly spravovany verzovacim systemem SVN. Model `Translation` s touto
vazbou primo pocita (uchovava cislo revize prelozeneho dokumentu). Pretaveni projektu
na praci s Gitem si proto vyzada upravy.
