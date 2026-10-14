📅 Calendario Unife
Un piccolo programma in Python che scarica l'orario delle lezioni da aule.unife.it (Università di Ferrara), lo converte in eventi iCalendar (`.ics`) e lo pubblica come calendario a cui iscriversi, ad esempio da Google Calendar.
L'orario si aggiorna in automatico ogni giorno: se una lezione cambia o viene annullata, il calendario lo riflette.
Come funziona
Il programma scarica le celle dell'orario dalla pagina AgendaStudenti di `aule.unife.it`.
Filtra gli insegnamenti scelti e scarta le lezioni annullate.
Trasforma ogni lezione in un evento calendario e genera il file `.ics`.
GitHub Actions esegue lo script ogni giorno e GitHub Pages pubblica il file aggiornato.
Il calendario, iscritto tramite URL, si aggiorna da solo sul tuo account.
Tecnologie
Python 3
`requests` per scaricare i dati
`icalendar` per creare gli eventi
GitHub Actions + GitHub Pages per automazione e pubblicazione
Installazione
```bash
git clone https://github.com/Lanfr4/calendario.git
cd calendario
pip install requests icalendar
```
Utilizzo
```bash
python main.py
```
> Sostituisci `main.py` con il nome effettivo del tuo script.
Al termine viene generato il file `.ics` con le lezioni.
Configurazione
Gli insegnamenti da includere si scelgono tramite il loro codice (ad esempio `EC674433`). Per aggiungere altre materie basta inserire i rispettivi codici nell'elenco dello script.
Iscriversi al calendario
Apri Google Calendar dal computer.
Vai su Altri calendari → Da URL.
Incolla l'indirizzo pubblico del file `.ics` su GitHub Pages (`https://lanfr4.github.io/calendario/<nome-file>.ics`).
Google Calendar ricontrolla il file periodicamente, quindi le modifiche possono impiegare qualche ora ad apparire.
Limiti noti
Alcuni insegnamenti, come i corsi a scelta in percorso comune, potrebbero non comparire con i parametri di ricerca attuali.
Il programma dipende dalla struttura della pagina di `aule.unife.it`: se il sito cambia, lo script potrebbe dover essere aggiornato.
Idee future
Supporto a tutte le materie del proprio corso di studi
Segnalare le variazioni rispetto all'orario precedente
Licenza
Progetto personale a scopo didattico.
