# 1. Kako v pythonu naredis novo mapo in kako lahko to mapo ob klicu funkcije najprej zbirses ter jo nato ponovno ustvaris? Ali za to obstaja kaksna knjiznica?

V Pythonu je delo z mapami (imeniki) zelo preprosto. Za to imamo na voljo dve odlični vgrajeni knjižnici: os (klasična pot) in pathlib (modernejša, bolj intuitivna pot). Za brisanje map, ki niso prazne, pa poleg njiju uporabimo še knjižnico shutil.

Za tvoj primer (izbriši, če obstaja, in nato ustvari znova) je najbolj elegantna uporaba knjižnice pathlib v kombinaciji s shutil.

Tukaj je celoten postopek in koda, kako to narediš.

Rešitev z modernim pathlib in shutil
To je trenutno najbolj priporočljiv način v Pythonu, saj z mapami delaš kot z objekti, koda pa je zelo čitljiva.

Python
from pathlib import Path
import shutil

def ponovno_ustvari_mapo(ime_mape: str):
    # Ustvarimo objekt Path za našo mapo
    pot = Path(ime_mape)
    
    # 1. Preverimo, če mapa že obstaja
    if pot.exists():
        # Če obstaja, jo izbrišemo (tudi če vsebuje datoteke)
        shutil.rmtree(pot)
        print(f"Mapa '{ime_mape}' je bila uspešno izbrisana.")
    
    # 2. Ustvarimo popolnoma novo, prazno mapo
    # parents=True omogoča, da ustvari vmesne mape, če ne obstajajo
    # exist_ok=True prepreči napako, če bi mapa slučajno že obstajala
    pot.mkdir(parents=True, exist_ok=True)
    print(f"Mapa '{ime_mape}' je bila uspešno ustvarjena.")

## Primer klica funkcije
ponovno_ustvari_mapo("moja_nova_mapa")
Alternativa s klasično knjižnico os
Če ti je bolj všeč klasični pristop, kjer z mapami upravljaš preko nizov (teksta), lahko uporabiš modul os. Logika ostaja popolnoma ista:

Python
import os
import shutil

def ponovno_ustvari_mapo_os(ime_mape: str):
    # 1. Preverimo in izbrišemo, če obstaja
    if os.path.exists(ime_mape):
        shutil.rmtree(ime_mape)
        print(f"Mapa '{ime_mape}' izbrisana.")
        
    # 2. Ustvarimo mapo znova
    os.makedirs(ime_mape, exist_ok=True)
    print(f"Mapa '{ime_mape}' ustvarjena.")

## Primer klica
ponovno_ustvari_mapo_os("stara_sola_mapa")
Ključne funkcije, ki si jih velja zapomniti:
shutil.rmtree(): Ključna funkcija, saj navadni os.rmdir() ali Path.rmdir() javita napako, če mapa ni popolnoma prazna. rmtree (remove tree) pa brez milosti pobriše mapo in vso njeno vsebino (datoteke in podmape).

exist_ok=True: Zelo koristen parameter pri ustvarjanju map, ki prepreči, da bi Python vrgel napako (FileExistsError), če mapa iz kakršnega koli razloga v tistem trenutku že obstaja.


# 2. Kako ti lahko selenium najde tak element v html kodi: <a href="/browse/boardgame/page/2" target="_self" title="next page"><b>Next »</b></a>

Za iskanje tega elementa v Seleniumu imaš na voljo več odličnih načinov, odvisno od tega, kaj je najbolj stabilno v tvojem sistemu. Ker gre za povezavo, ki vodi na naslednjo stran (next page), imamo nekaj zelo elegantnih rešitev.

Tukaj so najboljši načini, zapisani v jeziku Python (ki se najpogosteje uporablja s Seleniumom):

1. Preko besedila v povezavi (Najbolj preprosto)
Če veš, da bo na gumbu vedno pisalo "Next »", lahko uporabiš iskanje preko besedila. Ker je znotraj značke <a> še krepki tisk <b>, je najbolj varno uporabiti PARTIAL_LINK_TEXT (delno ujemanje).

Python
from selenium.webdriver.common.by import By

element = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
2. Preko XPath-a (Najbolj fleksibilno)
XPath ti omogoča, da element poiščeš glede na njegove atribute (npr. title ali href).

Glede na naslov (title="next page"):
To je odlična izbira, saj je naslov zelo specifičen.

Python
element = driver.find_element(By.XPATH, "//a[@title='next page']")
Glede na del poti v povezavi (href):
Če se številka strani spreminja (stran 2, stran 3 ...), lahko iščeš element, ki vsebuje začetni del povezave:

Python
element = driver.find_element(By.XPATH, "//a[contains(@href, '/browse/boardgame/page/')]")
Glede na natančno besedilo:

Python
element = driver.find_element(By.XPATH, "//a[contains(., 'Next')]")
3. Preko CSS selektorja (Najhitreje)
CSS selektorji so pogosto hitrejši in bolj čitljivi kot XPath.

Glede na atribut title:

Python
element = driver.find_element(By.CSS_SELECTOR, "a[title='next page']")
Glede na delni href (začne se z...):
Znak ^= pomeni "se začne z".

Python
element = driver.find_element(By.CSS_SELECTOR, "a[href^='/browse/boardgame/page/']")
💡 Nasvet za prakso: Če delaš paginacijo (klikanje skozi strani), je Metoda 2a (//a[@title='next page']) ponavadi najbolj stabilna, saj se atribut title="next page" verjetno ne bo spreminjal, medtem ko se bo številka strani v href ob vsakem kliku povečala.