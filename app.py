import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

# Startwerte – geschätzt
default_values = {
    "leer": {
        "zug": 4.7,
        "trailer": 6.6,
        "real_zug": 7.5,
        "real_trailer": 8.5
    },
    "voll": {
        "zug": 7.9,
        "trailer": 19.0,
        "real_zug": 11.3,
        "real_trailer": 27.5
    },
    "aktiv": True
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f, indent=4)

def berechne_kalibrierung(volvo1, real1, volvo2, real2):
    if volvo2 - volvo1 == 0:
        return 1.0, 0.0
    a = (real2 - real1) / (volvo2 - volvo1)
    b = real1 - a * volvo1
    return a, b

alle_daten = lade_daten()

with st.expander("🚚 Fahrzeugmodell auswählen / wechseln"):
    modelle = list(alle_daten.keys())
    if not modelle:
        st.warning("⚠️ Noch keine Modelle vorhanden. Bitte zuerst ein Modell eingeben und speichern.")
        aktuelles_modell = None
    else:
        aktuelles_modell = st.selectbox("Modell auswählen:", modelle)
        # Setze ausgewähltes Modell auf aktiv
        for modell in alle_daten:
            alle_daten[modell]["aktiv"] = (modell == aktuelles_modell)
        speichere_daten(alle_daten)

# Falls keine Modelle vorhanden sind, abbrechen
if not aktuelles_modell:
    st.stop()

daten = alle_daten[aktuelles_modell]

st.header("📥 Eingabe aktueller Volvo-Werte")

volvo_now_zug = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=daten["voll"]["zug"])
volvo_now_trailer = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=daten["voll"]["trailer"])

a1, b1 = berechne_kalibrierung(daten["leer"]["zug"], daten["leer"]["real_zug"],
                               daten["voll"]["zug"], daten["voll"]["real_zug"])
a2, b2 = berechne_kalibrierung(daten["leer"]["trailer"], daten["leer"]["real_trailer"],
                               daten["voll"]["trailer"], daten["voll"]["real_trailer"])

real_zug = volvo_now_zug * a1 + b1
real_trailer = volvo_now_trailer * a2 + b2
real_gesamt = real_zug + real_trailer

st.header("📊 Ergebnis")

st.write(f"🚛 Zugmaschine: **{real_zug:.2f} t**")
st.write(f"🛻 Auflieger: **{real_trailer:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

MAX_ANTRIEBSACHSE = 11.5
ueberladung_kg = max(0, (real_zug - MAX_ANTRIEBSACHSE) * 1000)
ueberladung_prozent = max(0, (real_zug - MAX_ANTRIEBSACHSE) / MAX_ANTRIEBSACHSE * 100)

if ueberladung_kg > 0:
    st.error(f"⚠️ Antriebsachse überladen: **{ueberladung_kg:.0f} kg** / **{ueberladung_prozent:.1f} %** über dem Limit!")
else:
    st.success("✅ Antriebsachse im grünen Bereich")
