import requests
from bs4 import BeautifulSoup
from icalendar import   Calendar  , Event
from datetime import date


# 1 Recuperare i Dati
oggi = date.today()
#date_paramter = oggi.strftime("%d-%m-%Y")
date_paramter = "5-10-2026"
"""
r = requests.get("https://aule.unife.it/AgendaStudenti/index.php"
       "?view=easycourse&form-type=corso&include=corso"
       "&txtcurr=2+-+Percorso+Comune&anno=2026&corso=3252"
       "&anno2%5B%5D=PDS0%7C2"
       f"&date={date_paramter}"
       "&periodo_didattico=&_lang=it&list=&week_grid_type=-1"
       "&ar_codes_=&ar_select_=&col_cells=0&empty_box=0"
       "&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0"
       )"""
parametri = {
    "view": "easycourse",
    "form-type": "corso",
    "include": "corso",
    "txtcurr": "2 - Percorso Comune",
    "anno": "2026",
    "corso": "3252",
    "anno2[]": ["PDS0|2"],
    "date": date_paramter,
}
r = requests.post("https://aule.unife.it/AgendaStudenti/grid_call.php", data=parametri)
dati = r.json()
print(dati["data"], dati["first_day"], dati["last_day"])
print(len(dati["celle"]))
with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(r.text)
print(r)
print(r.headers["Content-Type"])
print(len(r.text))
print("operativi" in r.text.lower())
print("operativi" in r.text)

# 2 Estrazione dati 




# 3 


