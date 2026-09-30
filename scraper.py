import requests
from icalendar import   Calendar  , Event
from datetime import date, datetime 
from zoneinfo import ZoneInfo


# 1 Recuperare i Dati
oggi = date.today()
date_paramter = oggi.strftime("%d-%m-%Y")



def scarica_celle(data):
    """Fa la POST e restituisce la lista delle celle."""
    parametri = {
        "view": "easycourse",
        "form-type": "corso",
        "include": "corso",
        "txtcurr": "2 - Percorso Comune",
        "anno": "2026",
        "corso": "3252",
        "anno2[]": ["PDS0|2"],
        "date": data,
    }
    r = requests.post("https://aule.unife.it/AgendaStudenti/grid_call.php", data=parametri)
    dati = r.json()

    return dati["celle"]


def filtra_lezioni(celle):
    """Tiene solo le celle del tuo insegnamento, non annullate."""

    risultato = []

    for cella in celle:
        if  cella["codice_insegnamento"] == "EC674433" and cella["Annullato"] == "0":
            risultato.append(cella)

    return risultato


def crea_evento(cella):
    """Trasforma una cella in un Event di icalendar."""
    testo = cella["data"] + " "+ cella["ora_inizio"]
    inizio = datetime.strptime(testo,  "%d-%m-%Y %H:%M")
    print(inizio)
    testo = cella["data"] + " "+ cella["ora_fine"]
    fine = datetime.strptime(testo,  "%d-%m-%Y %H:%M")
    print(fine)

    evento = Event()
    evento.add("summary", cella["nome_insegnamento"])
    evento.add("dtstart", inizio)
    evento.add("dtend", fine)

    return evento


def main():
    celle = scarica_celle("05-10-2026")
    lezioni = filtra_lezioni(celle)
    crea_evento(lezioni[0])
    evento = crea_evento(lezioni[0])
    print(evento["summary"])
    print(len(lezioni))  

if __name__ == "__main__":
    main()