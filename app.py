import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
import datenquelle as dq

app = Flask(__name__)

@app.route("/")
def startseite():
    return render_template("index.html")

# Replay-Uhr: startet beim Rennstart
START = datetime.fromisoformat("2026-09-06T13:00:00")
uhr = {"echt_start": time.time(), "rennzeit_start": START, "tempo": 1, "pause": False}


def rennzeit():
    if uhr["pause"]:
        return uhr["rennzeit_start"]
    vergangen = (time.time() - uhr["echt_start"]) * uhr["tempo"]
    return uhr["rennzeit_start"] + timedelta(seconds=vergangen)


def zeit_text():
    return rennzeit().strftime("%Y-%m-%dT%H:%M:%S")


def uhr_neu_setzen():
    uhr["rennzeit_start"] = rennzeit()
    uhr["echt_start"] = time.time()


@app.route("/api/status")
def status():
    z = zeit_text()
    return jsonify({
        "zeit": z,
        "runde": dq.aktuelle_runde(z),
        "flagge": dq.flagge_bei(z),
        "tempo": uhr["tempo"],
        "pause": uhr["pause"],
    })


@app.route("/api/rangliste")
def rangliste():
    z = zeit_text()
    con = dq.verbindung()
    fahrer = {n: (k, t, f) for n, k, t, f in con.execute("SELECT nummer, kuerzel, team, farbe FROM fahrer")}
    con.close()

    abstand = {n: (l, v) for n, l, v, _ in dq.abstaende_bei(z)}
    reifen = {n: (r, a) for n, r, a in dq.reifen_bei(z)}

    liste = []
    for nummer, platz, _ in dq.rangliste(z):
        kuerzel, team, farbe = fahrer.get(nummer, ("?", "?", "888888"))
        liste.append({
            "platz": platz,
            "nummer": nummer,
            "kuerzel": kuerzel,
            "team": team,
            "farbe": farbe,
            "abstand_leader": abstand.get(nummer, (None, None))[0],
            "abstand_vorne": abstand.get(nummer, (None, None))[1],
            "reifen": reifen.get(nummer, (None, None))[0],
            "reifenalter": reifen.get(nummer, (None, None))[1],
        })
    return jsonify(liste)


@app.route("/api/karte")
def karte():
    z = zeit_text()
    return jsonify([{"nummer": n, "x": x, "y": y} for n, x, y, _ in dq.orte_bei(z)])


@app.route("/api/pause", methods=["POST"])
def pause():
    uhr_neu_setzen()
    uhr["pause"] = not uhr["pause"]
    return jsonify({"pause": uhr["pause"]})


@app.route("/api/tempo/<int:wert>", methods=["POST"])
def tempo(wert):
    uhr_neu_setzen()
    uhr["tempo"] = wert
    return jsonify({"tempo": wert})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, render_template