import json
import requests
from pathlib import Path
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("Europe/Rome")
CODICE_INSEGNAMENTO = "EC674433"
URL = "https://aule.unife.it/AgendaStudenti/grid_call.php"
SETTIMANE = 8
FILE_STATO = Path("stato.json")
FILE_ICS = Path("lezioni.ics")


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
    r = requests.post(URL, data=parametri, timeout=10)
    r.raise_for_status()
    return r.json()["celle"]


def filtra_lezioni(celle):
    """Tiene solo le celle del tuo insegnamento, non annullate."""
    return [
        c for c in celle
        if c.get("codice_insegnamento") == CODICE_INSEGNAMENTO
        and c.get("Annullato") == "0"
    ]


def crea_evento(cella):
    """Trasforma una cella in un Event di icalendar."""
    formato = "%d-%m-%Y %H:%M"
    inizio = datetime.strptime(f'{cella["data"]} {cella["ora_inizio"]}', formato).replace(tzinfo=FUSO)
    fine = datetime.strptime(f'{cella["data"]} {cella["ora_fine"]}', formato).replace(tzinfo=FUSO)

    evento = Event()
    evento.add("summary", cella["nome_insegnamento"])
    evento.add("dtstart", inizio)
    evento.add("dtend", fine)
    evento.add("dtstamp", datetime.now(FUSO))
    evento.add("uid", f"{CODICE_INSEGNAMENTO}-{inizio:%Y%m%dT%H%M}@unife-orario")
    return evento


def raccogli_eventi():
    """Scarica le prossime SETTIMANE e restituisce {uid: evento}."""
    eventi = {}
    giorno = date.today()
    for _ in range(SETTIMANE):
        celle = scarica_celle(giorno.strftime("%d-%m-%Y"))
        for cella in filtra_lezioni(celle):
            evento = crea_evento(cella)
            eventi[str(evento["uid"])] = evento
        giorno += timedelta(days=7)
    return eventi


def leggi_stato():
    if FILE_STATO.exists():
        return json.loads(FILE_STATO.read_text(encoding="utf-8"))
    return {}


def salva_stato(eventi):
    stato = {
        uid: {
            "titolo": str(ev["summary"]),
            "inizio": ev["dtstart"].dt.strftime("%Y-%m-%dT%H:%M"),
            "fine": ev["dtend"].dt.strftime("%H:%M"),
        }
        for uid, ev in eventi.items()
    }
    FILE_STATO.write_text(json.dumps(stato, indent=2, ensure_ascii=False), encoding="utf-8")
    return stato


def descrivi(info):
    return f'{info["titolo"]} {info["inizio"].replace("T", " ")}-{info["fine"]}'


def stampa_cambiamenti(vecchio, nuovo):
    # del vecchio stato guardo solo le lezioni da oggi in poi
    oggi = date.today().isoformat()
    vecchio = {u: i for u, i in vecchio.items() if i["inizio"] >= oggi}

    aggiunte = nuovo.keys() - vecchio.keys()
    rimosse = vecchio.keys() - nuovo.keys()

    if not aggiunte and not rimosse:
        print("Nessun cambiamento.")
        return
    for uid in sorted(rimosse):
        print("RIMOSSA/SPOSTATA:", descrivi(vecchio[uid]))
    for uid in sorted(aggiunte):
        print("NUOVA:", descrivi(nuovo[uid]))


def main():
    vecchio = leggi_stato()
    eventi = raccogli_eventi()

    cal = Calendar()
    cal.add("prodid", "-//Orario Unife//IT")
    cal.add("version", "2.0")
    for uid in sorted(eventi):
        cal.add_component(eventi[uid])
    FILE_ICS.write_bytes(cal.to_ical())

    nuovo = salva_stato(eventi)
    if vecchio:
        stampa_cambiamenti(vecchio, nuovo)
    else:
        print(f"Prima esecuzione: {len(nuovo)} lezioni salvate in {FILE_ICS}")


if __name__ == "__main__":
    main()