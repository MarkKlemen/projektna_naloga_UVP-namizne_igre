import csv
from bs4 import BeautifulSoup
import os
import shutil


mapa = "surovi_podatki"
for stran in os.listdir(mapa):
    stran_pot = os.path.join(mapa, stran)
    with open(stran_pot, encoding="utf-8") as d:
        juha = BeautifulSoup(d.read(), "html.parser")
        #rank
        rank = juha.find("span", class_="rank-value").get_text().strip()
        #žanr
        zanr = juha.find("span", class_="rank-title ng-binding").get_text().stip()
        #rating
        rating = juha.find("span", attrs={"itemprop": "ratingValue"}).get_text().stip()
        



if os.path.exists("podatki"):
    shutil.rmtree("podatki")
os.makedirs("podatki", exist_ok=True)

pot_do_csv = os.path.join("podatki", "podatki.csv")
with open("podatki/podatki.csv", "w", encoding="utf-8", newline="") as c:
