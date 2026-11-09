const tabelle = document.getElementById("tabelle");
const vorlage = document.getElementById("karten-vorlage");

function baueKarte(f) {
    const karte = vorlage.content.cloneNode(true).querySelector(".karte");
    karte.style.setProperty("--team", "#" + f.farbe);
    karte.querySelector(".platz").textContent = f.platz;
    karte.querySelector(".kuerzel").textContent = f.kuerzel;
    karte.querySelector(".reifen").textContent = `${f.reifen} ${f.reifenalter} RD.`;
    karte.querySelector(".foto").src = `/static/fahrer/${f.nummer}.png`;
    return karte;
}

async function ladeTabelle() {
    const antwort = await fetch("/api/rangliste");
    const fahrer = await antwort.json();
    tabelle.replaceChildren(...fahrer.map(baueKarte));
}

ladeTabelle();
setInterval(ladeTabelle, 2000)