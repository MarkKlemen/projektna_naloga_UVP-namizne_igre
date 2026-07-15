# Analiza podatkov o namiznih igrah

## Opis projektne naloge
Ta projektna naloga je namenjena zbiranju, obdelavi in anlizi podatkov namiznih iger s spletne strani BoardGameGeek.
Iz spletne strani so najprej zbrana imena spletnih strani posameznih iger, potem pa Selenium obišče še vsako od teh posebej in zbere podrobnosti.
Te podrobnosti so nato "očiščene" in zapisane v CSV datoteko podatki.
S pomočjo JupiterNotebook lahko potem s podatki iz CSV datoteke pripravimo zanimive tabele in grafe.
Poleg teh datotek je še datoteka uporaba_ui.md, kjer imam zapisane pogovore z AI, ki mi je občasno pomagal pri raznih težavah pri projektni nalogi.

## Zagon programa
Glavna datoteka projekta je main.py, ki zažene celoten proces. V terminal samo vpišeš: python main.py.

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

