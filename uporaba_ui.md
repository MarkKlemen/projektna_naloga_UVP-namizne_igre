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


# 2. Kako ti lahko selenium najde tak element v html kodi: '<a href="/browse/boardgame/page/2" target="_self" title="next page"><b>Next »</b></a>'

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

# 3. Kako z beautiful soup najdes html element ki ima znacko span in nek class oziroma atribut?

Iskanje elementa span z določenim razredom (class) ali drugim atributom je z Beautiful Soup zelo preprosto. Za to se najpogosteje uporablja metoda find() (če iščeš samo prvi zadetek) ali find_all() (če želiš najti vse takšne elemente).

Tukaj so trije najpogostejši načini, kako to storiti.

1. Iskanje po razredu (Class)
Ker je beseda class v Pythonu rezervirana ključna beseda, Beautiful Soup za iskanje razredov uporablja argument class_ (s podčrtajem na koncu).

Python
from bs4 import BeautifulSoup

html = '<div class="vsebina"><span class="izpostavljeno">To je tekst</span></div>'
soup = BeautifulSoup(html, 'html.parser')

## Najde prvi span z razredom "izpostavljeno"
element = soup.find('span', class_='izpostavljeno')

print(element.text)  # Izpis: To je tekst
2. Iskanje po poljubnem atributu (npr. id, data-*, href)
Če želiš element poiskati po kakšnem drugem atributu, uporabi argument attrs, kamor podaš slovar (dictionary) z imenom in vrednostjo atributa.

Python
html = '<span data-kategorija="novice">Najnovejše novice...</span>'
soup = BeautifulSoup(html, 'html.parser')

## Iskanje preko slovarja atributov
element = soup.find('span', attrs={'data-kategorija': 'novice'})

print(element.text)
(Ta način deluje odlično tudi za class, npr. attrs={'class': 'izpostavljeno'}).

3. Uporaba CSS selektorjev (select in select_one)
Če si navajen/-a dela s CSS-om ali JavaScriptom, ti bo verjetno najbolj všeč metoda .select_one() (za en element) ali .select() (za seznam elementov). Tukaj uporabljaš klasično CSS sintakso.

Python
html = '<span class="zeleno" id="glavni-naslov">Pozdravljen svet!</span>'
soup = BeautifulSoup(html, 'html.parser')

## Iskanje s CSS selektorjem za razred (.)
element_class = soup.select_one('span.zeleno')

## Iskanje s CSS selektorjem za poljuben atribut ([atribut=vrednost])
element_attr = soup.select_one('span[id="glavni-naslov"]')

print(element_class.text)
Hitri povzetek:

Za iskanje enega elementa uporabi: soup.find('span', class_='ime-razreda')

Za iskanje vseh takšnih elementov uporabi: soup.find_all('span', class_='ime-razreda') (vrne seznam/list).

# 4. Kaj predlagas da naredim, ce mi ob zajemu podatkov s selenium cez nekaj casa vrne na spletni strani to napako: Koda napake: Out of Memory

Ta napaka (Out of Memory) je pri dolgotrajnem zajemanju podatkov (web scraping) s Seleniumom zelo pogosta težava. Pomeni, da je brskalnik (običajno Chrome ali Firefox, ki ga upravlja Selenium) porabil ves razpoložljiv sistemski pomnilnik (RAM).

Selenium sam po sebi ne sprošča pomnilnika samodejno, ampak z vsakim odprtim zavihkom, naloženo sliko, oglasom in javascriptom kopiči "smeti" v pomnilniku, dokler se brskalnik ne sesuje.

Tukaj je vrstni red korakov, s katerimi lahko to težavo trajno rešiš.

1. Najhitrejša in najbolj učinkovita rešitev: Periodično ponovno zaganjanje gonilnika (Driver Restart)
Namesto da imaš eno sejo brskalnika odprto več ur ali dni, proces razdeli na manjše dele.

Po določenem številu obiskanih strani (npr. na vsakih 100 ali 200 strani) popolnoma zapri brskalnik in odpri novega. S tem popolnoma sprostiš ves RAM, ki ga je brskalnik zasedel.

Python
## Primer v Pythonu:
import time
from selenium import webdriver

def run_scraping(urls):
    batch_size = 100  # Ponovni zagon po 100 straneh
    
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        
        # Zagon novega brskalnika za vsako serijo
        driver = webdriver.Chrome() 
        
        for url in batch:
            try:
                driver.get(url)
                # Tvoj kod za zajem podatkov...
            except Exception as e:
                print(f"Napaka pri {url}: {e}")
                
        # Ključno: .quit() zapre brskalnik in sprosti RAM (ne uporabljaj samo .close())
        driver.quit() 
        time.sleep(5)  # Kratka pavza, da sistem počisti procese
2. Onemogoči nepotrebne elemente (Slike, JavaScript, Oglaševanje)
Brskalnik porabi ogromno pomnilnika za nalaganje slik, oglasov in izvajanje težkih skript. Če za zajem podatkov potrebuješ le HTML strukturo ali tekst, te elemente onemogoči že ob zagonu.

Dodaj naslednje nastavitve (Chrome Options):

Python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

## 1. Zaženi v brezglavem načinu (headless) - porabi bistveno manj RAM-a
chrome_options.add_argument("--headless") 

## 2. Onemogoči GPU (grafično pospeševanje), ki rado pušča pomnilnik
chrome_options.add_argument("--disable-gpu")

## 3. Pomembno za okolja z omejenim RAM-om (npr. Docker ali manjši strežniki)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage") # Uporablja sistemski RAM namesto /dev/shm

## 4. Onemogoči nalaganje slik (ogromen prihranek RAM-a)
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
3. Prepreči kopičenje zgodovine in sej (Sessions & History)
Če znotraj iste seje obiščeš na tisoče strani, brskalnik v pomnilnik shranjuje zgodovino (History) in predpomnilnik (Cache).

Izogibaj se odpiranju novih zavihkov (target="_blank"): Če se odpirajo novi zavihki, jih sproti zapiraj z driver.close() in preklopi nazaj na glavni zavihek.

Redno briši piškotke: Med delovanjem lahko občasno pokličeš driver.delete_all_cookies(), kar lahko pomaga pri nekaterih straneh, ki agresivno sledijo sejam.

4. Alternativni pristop (Če Selenium ni nujen)
Selenium je odličen za strani, ki za prikaz vsebine nujno potrebujejo delovanje JavaScripta. Če pa opaziš, da se podatki na ciljni strani nalagajo preko statičnega HTML-ja ali pa jih stran pridobiva preko skritih API klicev (to preveriš v Network zavihku med orodji za razvijalce):

Uporabi requests in BeautifulSoup: To je svetlobno hitreje in porabi le drobec pomnilnika, saj sploh ne odpiraš pravega brskalnika.

Uporabi Playwright: Če še vedno potrebuješ brskalnik z JS podporo, je Playwright sodobnejša in pogosto bolje optimizirana alternativa Seleniumu, ki lažje upravlja s pomnilnikom.

Kaj predlagam za začetek?
Najprej poskusi v svoj kod dodati "Batching" (točko 1) in preveri, če se sesutja prenehajo. To običajno reši 95 % vseh "Out of Memory" težav pri Seleniumu.

# 5. Ali se lahko kako zazene funkcijo ki je znotraj datoteke main.py, samo da vpises v terminal ime datoteke?

Če imaš v main.py definirano funkcijo, je ne moreš neposredno zagnati samo z imenom datoteke. Če v terminal napišeš:

python main.py

se bo izvedla samo koda, ki je na vrhu nivoju datoteke (torej koda, ki ni znotraj funkcij), ne pa avtomatsko vse funkcije.

Primer:

main.py:

def pozdrav():
    print("Živjo!")

def sestej(a, b):
    return a + b

Če zaženeš:

python main.py

se ne bo zgodilo nič, ker nobena funkcija ni poklicana.

Običajen način je, da dodaš:

def main():
    pozdrav()
    print(sestej(2, 3))


if __name__ == "__main__":
    main()

Potem:

python main.py

zažene main() in posledično vse, kar je v njej.

Če pa želiš iz terminala poklicati točno določeno funkcijo, lahko uporabiš Python interpreter:

python -c "import main; main.pozdrav()"

To bo:

uvozilo main.py
našlo funkcijo pozdrav
jo zagnalo

Lahko tudi:

python -c "from main import sestej; print(sestej(5, 7))"

Za projektne naloge je najbolj običajno:

projekt/
│
├── main.py
├── podatki.py
├── analiza.py
└── README.md

in v main.py:

def main():
    # tukaj pokličeš vse funkcije
    ...


if __name__ == "__main__":
    main()

V README potem napišeš samo:

python main.py

in uporabniku ni treba vedeti, da obstaja funkcija main(). Zagon datoteke je dovolj.

# 6. Napisi primer kode za korelacijsko matriko za seznam podatkov v jupiter notebook

Tukaj je preprost, a izjemno uporaben primer, kako v Jupyter Notebooku pripraviš podatke, izračunaš korelacijsko matriko s knjižnico Pandas in jo vizualiziraš s čudovitim toplotnim zemljevidom (Heatmap) s pomočjo knjižnice Seaborn.

Za zagon te kode se prepričaj, da imaš nameščene knjižnice pandas, seaborn in matplotlib. Če jih nimaš, jih lahko v celici Jupyter Notebooka namestiš z ukazom:

Bash
!pip install pandas seaborn matplotlib
Koda za Jupyter Notebook
Celotno kodo lahko skopiraš neposredno v svojo celico v Jupyterju:

Python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## 1. Ustvarimo namišljene podatke (npr. o prodaji trgovine)
podatki = {
    'Oglaševanje_EUR': [1000, 1500, 2000, 2500, 3000, 3500, 4000],
    'Obisk_Spletne_Strani': [500, 600, 750, 900, 1100, 1200, 1400],
    'Prodaja_Kosov': [50, 55, 70, 85, 95, 110, 130],
    'Zunanje_Temperature_C': [15, 18, 22, 25, 28, 24, 20]
}

## Pretvorba v Pandas DataFrame (tabelo)
df = pd.DataFrame(podatki)

## 2. Izračun korelacijske matrike (uporablja se Pearsonov koeficient po privzetem)
korelacijska_matrika = df.corr()

## Prikaz matrike v lepi tabelarični obliki v Jupyterju
print("Korelacijska matrika v tabeli:")
display(korelacijska_matrika)

## 3. Vizualizacija s toplotnim zemljevidom (Heatmap)
## Nastavimo velikost grafa
plt.figure(figsize=(8, 6))

## Ustvarimo heatmap
sns.heatmap(
    korelacijska_matrika, 
    annot=True,          # Izpiše vrednosti koeficientov v kvadratke
    cmap='coolwarm',     # Barvna shema (modra za negativno, rdeča za pozitivno korelacijo)
    vmin=-1, vmax=1,     # Razpon vrednosti na barvni lestvici
    linewidths=0.5,      # Tanke črte med kvadratki za boljšo preglednost
    fmt=".2f"            # Zaokroževanje na 2 decimalni mesti
)

## Naslov grafa
plt.title('Toplotni zemljevid korelacijske matrike', fontsize=14, pad=15)
plt.show()
Hitra pomoč pri interpretaciji vrednosti:
Vrednost blizu 1: Močna pozitivna povezava (npr. več kot zapravimo za oglaševanje, več imamo obiska).

Vrednost blizu -1: Močna negativna povezava (ko ena vrednost raste, druga upada).

Vrednost blizu 0: Med podatki ni opazne linearne povezave (npr. zunanja temperatura morda nima posebne povezave s prodajo naših izdelkov).