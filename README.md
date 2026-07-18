# Analiza podatkov o namiznih igrah

## Opis projektne naloge
Ta projektna naloga je namenjena zbiranju, obdelavi in analizi podatkov namiznih iger s spletne strani BoardGameGeek.
Iz spletne strani so najprej zbrana imena spletnih strani posameznih iger, potem pa Selenium obišče še vsako od teh posebej in zbere podrobnosti.
Te podrobnosti so nato "očiščene" in zapisane v CSV datoteko podatki.csv.
S pomočjo Jupyter Notebook lahko potem s podatki iz CSV datoteke pripravimo zanimive tabele in grafe.
Poleg teh datotek je še datoteka uporaba_ui.md, kjer imam zapisane pogovore z UI, ki mi je občasno pomagal pri raznih težavah pri projektni nalogi.

## Zagon programa
Glavna datoteka projekta je main.py, ki zažene celoten proces. V terminal samo vpišeš: python main.py.
Pomembno: po tem ko se program zažene, in se odpre prva spletna stran, počakajte, da selenium klikne piškotke, potem pa se nujno prijavite, saj sicer program ne bo deloval.
Pred tem je seveda treba imeti že ustvarjen profil na tej spletni strani.

## Podatki

Za vsako igro so shranjeni naslednji podatki:
- id
- ime
- rank
- žanr
- uporabniška ocena
- število ocen
- leto izdaje
- razpon primerne starosti
- zahtevnost na lestvici do 5
- razpon primernega števila igralcev
- razpon časa igranja
- najmanjša cena

## Analiza
Analiza je prikazana v datoteki analiza.ipynyb, kjer so prikazane razne tabele in grafi, glede na nek nabor podatkov.

## Avtor
Mark Klemen

