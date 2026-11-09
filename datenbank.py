import sqlite3
import requests
import time

SESSION = 11361      # Monza 2026, Rennen
API = "https://api.openf1.org/v1"

con = sqlite3.connect('f1.db')

fahrer = requests.get(f"{API}/drivers?session_key={SESSION}").json()

con.execute("DROP TABLE IF EXISTS fahrer")
con.execute("""
    CREATE TABLE fahrer (
        nummer INTEGER,
        kuerzel TEXT,
        team TEXT,
        farbe TEXT
    )
""")
for f in fahrer:
    con.execute(
        "INSERT INTO fahrer (nummer, kuerzel, team, farbe) VALUES (?, ?, ?, ?)",
        (f['driver_number'], f['name_acronym'], f['team_name'], f['team_colour'])
    )

stints = requests.get(f"{API}/stints?session_key={SESSION}").json()

con.execute("DROP TABLE IF EXISTS stints")
con.execute("""
    CREATE TABLE stints(
        name TEXT,
        nummer INTEGER,
        stint INTEGER,
        reifen TEXT,
        runde_start INTEGER,
        runde_ende INTEGER,
        alter_start INTEGER
    )
    """)

name_von = {f['driver_number']: f['last_name'] for f in fahrer}


for s in stints:
    con.execute(
               "INSERT INTO stints (name, nummer, stint, reifen, runde_start, runde_ende, alter_start) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name_von[s['driver_number']], s['driver_number'], s['stint_number'], s['compound'], s['lap_start'], s['lap_end'], s['tyre_age_at_start'])
    )
positionen = requests.get(f"{API}/position?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS positionen")
con.execute("""
    CREATE TABLE positionen (
        nummer INTEGER,
        platz INTEGER,
        datum TEXT
        )
""")
for p in positionen:
    con.execute(
        'INSERT INTO positionen (nummer, platz, datum) VAlUES(?,?,?)',
        (p['driver_number'], p['position'], p['date'])
        )

time.sleep(1)
abstaende = requests.get(f"{API}/intervals?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS abstaende")
con.execute("""
    CREATE TABLE abstaende (
        nummer INTEGER,
        abstand_leader TEXT,
        abstand_vorne TEXT,
        datum TEXT
    )
""")

for a in abstaende:
    con.execute(
        'INSERT INTO abstaende (nummer, abstand_leader, abstand_vorne, datum) VAlUES(?,?,?,?)',
        (a['driver_number'], a['gap_to_leader'], a['interval'], a['date'])
        )
    
time.sleep(1)
meldungen = requests.get(f"{API}/race_control?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS meldungen")
con.execute("""
    CREATE TABLE meldungen (
        runde INTEGER,
        kategorie TEXT,
        flagge TEXT,
        datum TEXT,
        bereich TEXT,
        text TEXT
    )
""")
for m in meldungen:
    con.execute(
        'INSERT INTO meldungen (runde, kategorie, flagge, datum, bereich, text) VAlUES(?,?,?,?,?,?)',
        (m['lap_number'], m['category'], m['flag'], m['date'], m['scope'], m['message'])
        )

time.sleep(1)
rundenzeiten = requests.get(f"{API}/laps?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS rundenzeiten")
con.execute("""
    CREATE TABLE rundenzeiten(
        nummer INTEGER,
        runde INTEGER,
        zeit REAL,
        sektor1 REAL,
        sektor2 REAL,
        sektor3 REAL,
        boxenausfahrt INTEGER,
        datum TEXT
    )
""")
for r in rundenzeiten:
    con.execute(
        'INSERT INTO rundenzeiten (nummer, runde, zeit, sektor1, sektor2, sektor3, boxenausfahrt, datum) VAlUES(?, ?, ?, ?, ?, ?, ?, ?)',
        ((r['driver_number'], r['lap_number'], r['lap_duration'], r['duration_sector_1'], r['duration_sector_2'], r['duration_sector_3'], r['is_pit_out_lap'], r['date_start'])
        )
    )


con.execute("DROP TABLE IF EXISTS ort")
con.execute("""
    CREATE TABLE ort (
        nummer INTEGER,
        x REAL,
        y REAL,
        datum TEXT
     )
 """)
for f in fahrer:
    time.sleep(1)
    punkte = requests.get(f"{API}/location?session_key={SESSION}&driver_number={f['driver_number']}").json()
    for o in punkte [::5]:
        con.execute(
            'INSERT INTO ort (nummer, x, y, datum) VAlUES(?,?,?,?)',
            (o['driver_number'], o['x'], o['y'], o['date'])
        )

time.sleep(1)
wetter = requests.get(f"{API}/weather?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS wetter")
con.execute("""
    CREATE TABLE wetter(
        luft REAL,
        strecke REAL,
        feuchtigkeit REAL,
        regen INTEGER,
        wind REAL,
        windrichtung INTEGER,
        datum TEXT
    )
""")
for w in wetter:
    con.execute(
        'INSERT INTO wetter (luft, strecke, feuchtigkeit, regen, wind, windrichtung, datum) VAlUES(?, ?, ?, ?, ?, ?, ?)',
        (w['air_temperature'], w['track_temperature'], w['humidity'], w['rainfall'], w['wind_speed'], w['wind_direction'], w['date'])        )
time.sleep(1)
box = requests.get(f"{API}/pit?session_key={SESSION}").json()
con.execute("DROP TABLE IF EXISTS box")
con.execute("""
    CREATE TABLE box(
        nummer INTEGER,
        runde INTEGER,
        boxengasse REAL,
        standing_time REAL,
        datum TEXT
    )
""")
for b in box:
    con.execute(
        'INSERT INTO box (nummer, runde, boxengasse, standing_time, datum) VAlUES(?, ?, ?, ?, ?)',
        ((b['driver_number'], b['lap_number'], b['lane_duration'], b['stop_duration'], b['date'])
        )
    )


con.commit()
con.close()
print("Tabelle fahrer erstellt")