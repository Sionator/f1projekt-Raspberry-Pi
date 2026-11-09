import sqlite3


def verbindung():
    return sqlite3.connect('f1.db')


def rennstart():
    con = verbindung()
    start = con.execute("SELECT MIN(datum) FROM positionen").fetchone()[0]
    con.close()
    return start


def rangliste(zeit):
    con = verbindung()
    daten = con.execute("""
        SELECT nummer, platz, MAX(datum)
        FROM positionen
        WHERE datum <= ?
        GROUP BY nummer
        ORDER BY platz
    """, (zeit,)).fetchall()
    con.close()
    return daten


def flagge_bei(zeit):
    con = verbindung()
    meldungen = con.execute("""
        SELECT kategorie, flagge, bereich, text
        FROM meldungen
        WHERE datum <= ?
        ORDER BY datum
    """, (zeit,)).fetchall()
    con.close()

    aktuelle_flagge = "GREEN"
    for kategorie, flagge, bereich, text in meldungen:
        if kategorie == "Flag" and bereich == "Track":
            aktuelle_flagge = flagge
        elif kategorie == "SafetyCar" and "VIRTUAL" in text:
            aktuelle_flagge = "VSC"
        elif kategorie == "SafetyCar" and "DEPLOYED" in text:
            aktuelle_flagge = "SC"
        elif kategorie == "SafetyCar" and "ENDING" in text:
            aktuelle_flagge = "GREEN"

    if aktuelle_flagge == "CLEAR":
        aktuelle_flagge = "GREEN"
    return aktuelle_flagge

def aktuelle_runde(zeit):
    con = verbindung()
    runde = con.execute("""
        SELECT MAX(runde)
        FROM rundenzeiten
        WHERE datum <= ?
    """, (zeit,)).fetchone()[0]
    con.close()
    return runde

def abstaende_bei(zeit):
    con = verbindung()
    daten = con.execute("""
        SELECT nummer, abstand_leader, abstand_vorne, MAX(datum)
        FROM abstaende
        WHERE datum <= ?
        GROUP BY nummer
    """, (zeit,)).fetchall()
    con.close()
    return daten
def reifen_bei(zeit):
    runde = aktuelle_runde(zeit)
    if runde is None:
        return []
    con = verbindung()
    daten = con.execute("""
        SELECT nummer, reifen, alter_start, runde_start
        FROM stints
        WHERE runde_start <= ? AND (runde_ende >= ? OR runde_ende IS NULL)
    """, (runde, runde)).fetchall()
    con.close()

    ergebnis = []
    for nummer, reifen, alter_start, runde_start in daten:
        alter = (alter_start or 0) + (runde - runde_start)
        ergebnis.append((nummer, reifen, alter))
    return ergebnis


def orte_bei(zeit):
    con = verbindung()
    daten = con.execute("""
        SELECT nummer, x, y, MAX(datum)
        FROM ort
        WHERE datum <= ?
        GROUP BY nummer
    """, (zeit,)).fetchall()
    con.close()
    return daten
if __name__ == "__main__":
    zeit = "2026-09-06T13:30:00"
    print("Start:", rennstart())

    zeit = "2026-09-06T13:30:00"
    print("Start:", rennstart())
    print("Flagge:", flagge_bei(zeit))
    print("Runde:", aktuelle_runde(zeit))
    print("Rangliste:", rangliste(zeit))
    print("Abstände:", abstaende_bei(zeit))
    print("Reifen:", reifen_bei(zeit))
    print("Orte:", orte_bei(zeit))