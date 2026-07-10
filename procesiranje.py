import csv
from bs4 import BeautifulSoup
import os
import shutil
import re


mapa = "surovi_podatki"
for stran in os.listdir(mapa):
    stran_pot = os.path.join(mapa, stran)
    with open(stran_pot, encoding="utf-8") as d:
        juha = BeautifulSoup(d.read(), "html.parser")
        #rank
        rank = juha.find("span", class_="rank-value").get_text().strip()
        #žanr
        zanr = juha.find("span", class_="rank-title ng-binding").get_text().strip()
        #rating
        rating = juha.find("span", attrs={"itemprop": "ratingValue"}).get_text().strip()
        #stevilo ratingov
        re_ratingi = juha.find("a", attrs={"ui-sref": "geekitem.ratings({rated:1,comment:'',status:''})"}).get_text().strip()
        ratingi = re.search(r"\d+[A_Z]?\b")
        #leto izdaje
        leto_izdaje = juha.find("span", class_="game-year ng-binding ng-scope").get_text().strip().replace("(", "").replace(")", "")
        #predlagana starost
        starost = juha.find("span", attrs={"itemprop": "suggestedMinAge"}).get_text().strip()
        starost += "+"
        #težavnost
        tezavnost = juha.find("span", class_="ng-binding gameplay-weight-meduim").get_text().strip()
        tezavnost += "/5"
        #predlagano število igralcev
        st_igralcev = juha.find("span", attrs={"ng-show": "::geekitemctrl.geekitem.data.item.polls.userplayers.totalvotes > 0"}).get_text().strip()
        #čas igranja
        spodnje = juha.find("span", attrs={"ng-if": "min > 0"})
        zgornje = juha.find("span", attr={"ng-if": "max>0 && min != max"})
        if spodnje:
            min = spodnje.get_text().strip()
            if zgornje:
                max = zgornje.get_text().strip()
            else:
                max = ""
            cas = min + max


if os.path.exists("podatki"):
    shutil.rmtree("podatki")
os.makedirs("podatki", exist_ok=True)

pot_do_csv = os.path.join("podatki", "podatki.csv")
with open("podatki/podatki.csv", "w", encoding="utf-8", newline="") as c:
