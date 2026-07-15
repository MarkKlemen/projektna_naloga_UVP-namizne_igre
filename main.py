from zajem import shrani_igre
from procesiranje import podrobnosti_o_igrah, zapisi_v_csv

def analiziraj_igre():
    shrani_igre()
    #tukaj se odpre okno kjer počakas da se zaprejo piskotki, potem pa se prijavis
    podatki = podrobnosti_o_igrah()
    zapisi_v_csv(podatki)

if __name__ == "__main__":
    analiziraj_igre()