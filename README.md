# 📅 Calendario Unife

Un piccolo programma in Python che scarica l'orario delle lezioni da [aule.unife.it](https://aule.unife.it) (Università di Ferrara), lo converte in eventi iCalendar (`.ics`) e lo pubblica come calendario a cui iscriversi, ad esempio da Google Calendar.

L'orario si aggiorna in automatico ogni giorno: se una lezione cambia o viene annullata, il calendario lo riflette.

## Come funziona

1. Il programma scarica le celle dell'orario dalla pagina *AgendaStudenti* di `aule.unife.it`.
2. Filtra gli insegnamenti scelti e scarta le lezioni annullate.
3. Trasforma ogni lezione in un evento calendario e genera il file `.ics`.
4. **GitHub Actions** esegue lo script ogni giorno e **GitHub Pages** pubblica il file aggiornato.
5. Il calendario, iscritto tramite URL, si aggiorna da solo sul tuo account.

## Tecnologie

- Python 3
- [`requests`](https://requests.readthedocs.io/) per scaricare i dati
- [`icalendar`](https://icalendar.readthedocs.io/) per creare gli eventi
- GitHub Actions + GitHub Pages per automazione e pubblicazione

## Installazione

```bash
git clone https://github.com/Lanfr4/calendario.git
cd calendario
pip install requests icalendar
```

## Utilizzo

```bash
python scraper.py
```

> Sostituisci `main.py` con il nome effettivo del tuo script.

Al termine viene generato il file `.ics` con le lezioni.
