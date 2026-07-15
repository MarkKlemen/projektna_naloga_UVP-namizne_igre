import csv
from bs4 import BeautifulSoup
import os
import re


def podrobnosti_o_igrah():
    vsi_podatki = []
    mapa = "surovi_podatki"
    for stran in os.listdir(mapa):
        stran_pot = os.path.join(mapa, stran)
        with open(stran_pot, encoding="utf-8") as d:
            juha = BeautifulSoup(d.read(), "html.parser")
            #id
            id_igre = re.match(r"\d+", stran).group() #group vrne niz od tega kar je najdeno z match
            #ime
            j_ime = juha.find("span", attrs={"itemprop": "name"})
            ime = j_ime.get_text().strip() if j_ime else None
            #rank
            j_rank = juha.find("span", class_="rank-number")
            rank = int(j_rank.get_text().strip().replace(",", "")) if j_rank else None
            #žanr (samo najbolj relevanten)
            vsi_zanri = juha.find_all("span", class_="rank-title ng-binding") #vec moznih, hocemo prvega, a ne "Overall", saj je to za rank
            zanr = None
            for i in vsi_zanri:
                trenutni = i.get_text().strip()
                if trenutni == "Overall":
                    continue
                else:
                    zanr = trenutni
                    break
            #rating
            j_rating = juha.find("span", attrs={"itemprop": "ratingValue"})
            rating = float(j_rating.get_text().strip()) if j_rating else None
            #stevilo ratingov
            j_st_ratingov = juha.find("a", attrs={"ui-sref": "geekitem.ratings({rated:1,comment:'',status:''})"})
            if j_st_ratingov:
                tekst_ratingov = j_st_ratingov.get_text().strip()
                re_ratingi = re.search(r"\d+(?:[.,]\d+)?[KM]?\b", tekst_ratingov) #ta regex je za to, ce je namesto 1000 napisano "K", ali pa namesto 1000000 napisano "M"
                #?: je za nezajemalne oklepaje v regex
                st_ratingov = re_ratingi.group() if re_ratingi else None
            else:
                st_ratingov = None
            if st_ratingov:
                if "K" in st_ratingov:
                    st_ratingov = int(float(st_ratingov[:-1].replace(",", ".")) * 1000)
                elif "M" in st_ratingov:
                    st_ratingov = int(float(st_ratingov[:-1].replace(",", ".")) * 1000000)
                else:
                    st_ratingov = int(st_ratingov)
            #leto izdaje
            j_leto = juha.find("span", class_="game-year ng-binding ng-scope")
            leto = int(j_leto.get_text().strip().replace("(", "").replace(")", "")) if j_leto else None
            #najmanjša starost
            j_starost = juha.find("span", attrs={"itemprop": "suggestedMinAge"})
            starost = int(j_starost.get_text().strip()) if j_starost else None
            #zahtevnost / 5
            j_zahtevnost = juha.find("span", attrs={"item-poll-button": "boardgameweight"})
            zahtevnost = float(j_zahtevnost.get_text().replace("/ 5 Complexity Rating", "").strip()) if j_zahtevnost else None
            #predlagano število igralcev
            j_igralci = juha.find("span", attrs={"ng-show": "::geekitemctrl.geekitem.data.item.polls.userplayers.totalvotes > 0"})
            min_igralci = None
            max_igralci = None
            if j_igralci:
                igralci = j_igralci.get_text().strip()
                igralci = igralci.replace("-", "–") #ce bi slucajno bil "-" namesto "–"
                if "," in igralci or igralci.lower() == "none":
                    min_igralci = None
                    max_igralci = None
                elif "–" in igralci:
                    min_igralci, max_igralci = igralci.split("–")
                    min_igralci = int(min_igralci)
                    if "+" in max_igralci:
                        max_igralci = None
                    else:
                        max_igralci = int(max_igralci)
                elif "+" in igralci:
                    min_igralci = int(igralci.replace("+", ""))
                else:
                    min_igralci = int(igralci)
                    max_igralci = int(igralci)
            #čas igranja
            j_cas = juha.find("span", attrs={"min": "::geekitemctrl.geekitem.data.item.minplaytime"})
            min_cas = None
            max_cas = None
            if j_cas:
                cas = j_cas.get_text().strip()
                cas = cas.replace("-", "–")
                if "–" in cas:
                    min_cas, max_cas = cas.split("–")
                    min_cas = int(min_cas)
                    max_cas = int(max_cas)
                elif "+" in cas:
                    min_cas = int(cas.replace("+", ""))
                else:
                    min_cas = int(cas)
                    max_cas = int(cas)
            #cena
            j_cena = juha.find("a", attrs={"ui-sref": "geekitem.marketplace.ebay"})
            cena = None
            if j_cena:
                tekst_cena = (j_cena.get_text().replace("from", "")
                              .replace("–", "").replace("eBay", "").replace(",", "").strip())
                tekst_cena = tekst_cena[1:] #da se znebimo valut
                if tekst_cena:
                    cena = float(tekst_cena)

            vsi_podatki.append({
                "id": id_igre,
                "ime": ime,
                "rank": rank,
                "žanr": zanr,
                "rating": rating,
                "število rating-ov": st_ratingov,
                "leto": leto,
                "starost": starost,
                "zahtevnost/5": zahtevnost,
                "najmanj igralcev": min_igralci,
                "največ igralcev": max_igralci,
                "najkrajši čas": min_cas,
                "najdaljši čas": max_cas,
                "cena": cena
            })
    return vsi_podatki

def zapisi_v_csv(podatki):
    os.makedirs("podatki", exist_ok=True)
    pot_do_csv = os.path.join("podatki", "podatki.csv")

    with open(pot_do_csv, "w", encoding="utf-8", newline="") as c:
        pisatelj = csv.writer(c)
        pisatelj.writerow(
            [
                "id",
                "ime",
                "rank",
                "žanr",
                "rating",
                "število rating-ov",
                "leto izdaje",
                "najmanjša starost",
                "zahtevnost /5",
                "najmanj igralcev",
                "največ igralcev",
                "najkrajši čas",
                "najdaljši čas",
                "najnižja cena ($)"
            ]
        )

        for igra in podatki:
            pisatelj.writerow(
                [
                    igra["id"],
                    igra["ime"],
                    igra["rank"],
                    igra["žanr"],
                    igra["rating"],
                    igra["število rating-ov"],
                    igra["leto"],
                    igra["starost"],
                    igra["zahtevnost/5"],
                    igra["najmanj igralcev"],
                    igra["največ igralcev"],
                    igra["najkrajši čas"],
                    igra["najdaljši čas"],
                    igra["cena"]
                ]
            )
