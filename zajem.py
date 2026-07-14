from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os
import shutil
import re

def shrani_igre():
    driver = webdriver.Chrome()
    if os.path.exists("surovi_podatki"):
        shutil.rmtree("surovi_podatki") #zbrise mapo, ce obstaja
    os.makedirs("surovi_podatki", exist_ok=True) #jo ponovno ustvari
    driver.get("https://boardgamegeek.com/browse/boardgame/page/1?sort=numvoters&sortdir=desc")

    time.sleep(3)

    gumb_piskotki = driver.find_element(By.CSS_SELECTOR, "button.fc-cta-consent")
    gumb_piskotki.click()
    time.sleep(5) #cas za prijavo, da dopusti vec kot 10 strani podatkov, drugace je samo 953 iger

    vse_igre = set()

    for stran in range(1, 2):
        trenutni_url = f"https://boardgamegeek.com/browse/boardgame/page/{stran}?sort=numvoters&sortdir=desc"
        driver.get(trenutni_url)
        time.sleep(3)
        vsebina = driver.page_source
        igre = re.findall(r"boardgame/(\d+/[\w:-]+)", vsebina)
        time.sleep(2)
        
        for igra in igre:
            vse_igre.add(igra)
    print(vse_igre)
    print(len(vse_igre))

    for st, ime in enumerate(vse_igre):
        ime_datoteke = ime.replace("/", "_")
        pot = os.path.join("surovi_podatki", f"{ime_datoteke}.html")

        if os.path.exists(pot):
            continue
        if st > 0 and st % 50 == 0: #za napako spomina streznika
            driver.quit()
            time.sleep(2)
            driver = webdriver.Chrome()
            driver.get(f"https://boardgamegeek.com/boardgame/{ime}")
            time.sleep(3)
            gumb_piskotki = driver.find_elements(By.CSS_SELECTOR, "button.fc-cta-consent")
            if len(gumb_piskotki) > 0:
                gumb_piskotki[0].click()
                time.sleep(2)
      
        else:
            driver.get(f"https://boardgamegeek.com/boardgame/{ime}")
            time.sleep(3)

        html_igre = driver.page_source
        with open(pot, "w", encoding="utf-8") as d:
            d.write(html_igre)

    driver.quit()