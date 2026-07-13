import csv
from bs4 import BeautifulSoup
import os
import shutil
import re


def podrobnosti_o_igrah():
    vsi_podatki = []
    mapa = "surovi_podatki"
    for stran in os.listdir(mapa):
        stran_pot = os.path.join(mapa, stran)
        with open(stran_pot, encoding="utf-8") as d:
            juha = BeautifulSoup(d.read(), "html.parser")
            #ime
            j_ime = juha.find("span", attrs={"itemprop": "name"})
            ime = j_ime.get_text().strip() if j_ime else "None"
            #rank
            j_rank = juha.find("span", class_="rank-number")
            rank = j_rank.get_text().strip() if j_rank else "None"
            #žanr
            vsi_zanri = juha.find_all("span", class_="rank-title ng-binding") #vec moznih, hocemo prvega, a ne "Overall", saj je to za rank
            zanr = "None"
            for i in vsi_zanri:
                trenutni = i.get_text().strip()
                if trenutni == "Overall":
                    continue
                else:
                    zanr = trenutni
                    break
            #rating
            j_rating = juha.find("span", attrs={"itemprop": "ratingValue"})
            rating = j_rating.get_text().strip() if j_rating else "None"
            #stevilo ratingov
            j_st_ratingov = juha.find("a", attrs={"ui-sref": "geekitem.ratings({rated:1,comment:'',status:''})"})
            if j_st_ratingov:
                tekst_ratingov = j_st_ratingov.get_text().strip()
                re_ratingi = re.search(r"\d+[A-Z]?\b", tekst_ratingov) #ta regex je za to, ce je namesto 1000 napisano "K", ali pa namesto 1000000 napisano "M"
                st_ratingov = re_ratingi.group() if re_ratingi else "None"
            else:
                st_ratingov = "None"
            #leto izdaje
            j_leto_izdaje = juha.find("span", class_="game-year ng-binding ng-scope")
            leto_izdaje = j_leto_izdaje.get_text().strip().replace("(", "").replace(")", "") if j_leto_izdaje else "None"
            #predlagana starost
            j_starost = juha.find("span", attrs={"itemprop": "suggestedMinAge"})
            starost = j_starost.get_text().strip() if j_starost else "None"
            starost += "+"
            #težavnost
            j_tezavnost = juha.find("span", class_="ng-binding gameplay-weight")
            tezavnost = j_tezavnost.get_text().strip() if j_tezavnost else "None"
            tezavnost += "/5"
            #predlagano število igralcev
            j_igralci = juha.find("span", attrs={"ng-show": "::geekitemctrl.geekitem.data.item.polls.userplayers.totalvotes > 0"})
            igralci = j_igralci.get_text().strip() if j_igralci else "None"
            #čas igranja
            spodnje = juha.find("span", attrs={"ng-if": "min > 0"})
            zgornje = juha.find("span", attrs={"ng-if": "max>0 && min != max"})

            min_cas = spodnje.get_text().strip() if spodnje else ""
            max_cas = zgornje.get_text().strip() if zgornje else ""

            if min_cas and max_cas:
                cas = f"{min_cas}{max_cas} min" #vezaj je ze vkljucen
            elif min_cas:
                cas = f"{min_cas} min"
            else:
                cas = "None"
            #cena
            j_cena = juha.find("a", attrs={"ui-sref": "geekitem.marketplace.ebay"})
            cena = j_cena.get_text().replace("from", "").replace("–", "").replace("eBay", "").strip() if j_cena else "None"

            vsi_podatki.append({
                "ime": ime,
                "rank": rank,
                "žanr": zanr,
                "rating": rating,
                "število rating-ov": st_ratingov,
                "leto izdaje": leto_izdaje,
                "predlagana starost": starost,
                "težavnost": tezavnost,
                "predlagano število igralcev": igralci,
                "čas igranja": cas,
                "cena": cena
            })
    return vsi_podatki


if os.path.exists("podatki"):
    shutil.rmtree("podatki")
os.makedirs("podatki", exist_ok=True)
pot_do_csv = os.path.join("podatki", "podatki.csv")
koncni_podatki = podrobnosti_o_igrah()

with open("podatki/podatki.csv", "w", encoding="utf-8", newline="") as c:
    pisatelj = csv.writer(c)
    pisatelj.writerow(
        [
            "ime",
            "rank",
            "žanr",
            "rating",
            "število rating-ov",
            "leto izdaje",
            "predlagana starost",
            "težavnost",
            "predlagano število igralcev",
            "čas igranja",
            "cena"
        ]
    )

    for igra in koncni_podatki:
        pisatelj.writerow(
            [
                igra["ime"],
                igra["rank"],
                igra["žanr"],
                igra["rating"],
                igra["število rating-ov"],
                igra["leto izdaje"],
                igra["predlagana starost"],
                igra["težavnost"],
                igra["predlagano število igralcev"],
                igra["čas igranja"],
                igra["cena"]
            ]
        )
