from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os
import shutil
import re

driver = webdriver.Chrome()
if os.path.exists("surovi_podatki"):
    shutil.rmtree("surovi_podatki") #zbrise mapo, ce obstaja
os.makedirs("surovi_podatki", exist_ok=True) #jo ponovno ustvari
driver.get("https://boardgamegeek.com/browse/boardgame/page/1")

time.sleep(3)

gumb_piskotki = driver.find_element(By.CSS_SELECTOR, "button.fc-cta-consent")
gumb_piskotki.click()
time.sleep(5)

vse_igre = set()

for stran in range(1, 11):
    trenutni_url = f"https://boardgamegeek.com/browse/boardgame/page/{stran}"
    driver.get(trenutni_url)
    time.sleep(3)
    vsebina = driver.page_source
    igre = re.findall(r"boardgame/(\d+/[\w:-]+)", vsebina)
    time.sleep(2)
    for igra in igre:
        vse_igre.add(igra)
print(vse_igre)
print(len(vse_igre))

for ime in vse_igre:
    driver.get(f"https://boardgamegeek.com/boardgame/{ime}")
    time.sleep(3)
    html_igre = driver.page_source
    ime = ime.replace("/", "_")
    pot = os.path.join("surovi_podatki", f"{ime}.html")
    with open(pot, "w", encoding="utf-8") as d:
        d.write(html_igre)
driver.quit()