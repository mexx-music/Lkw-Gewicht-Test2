import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

default_values = {
    "leer_volvo_antrieb": 4.7,
    "leer_real_antrieb": 7.5,
    "voll_volvo_antrieb": 11.0,
    "voll_real_antrieb": 11.5,
    "teilbeladung_volvo_antrieb": 0.0,
    "teilbeladung_real_antrieb": 0.0,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "voll_volvo_auflieger": 23.0,
    "voll_real_auflieger": 27.5,
    "teilbeladung_volvo_auflieger": 0.0,
    "teilbeladung_real_auflieger": 0.0
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f, indent=4)

def berechne_kalibrierung(volvo1, real1, volvo2, real2, optional_volvo=0.0, optional_real=0.0):
    if optional_volvo > 0 and optional_real > 0:
        x = [volvo1, optional_volvo, volvo2]
        y = [real1, optional_real, real2]
        xm = sum(x) / 3
        ym = sum(y) / 3
        a = sum((x[i] - xm)*(y[i] - ym) for i in range(3)) / sum((x[i] - xm)**2 for i in range(3))
        b = ym - a * xm
        return a, b
    elif volvo2 - volvo1 == 0:
        return 1.0, 0.0
    else:
        a = (real2 - real1) / (volvo2 - volvo1)
        b = real1 - a * volvo1
        return a, b

kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer, Voll, Teilbeladung")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer (Zugmaschine)", value=daten["leer_volvo_antrieb"])
    leer_real_antrieb = st.number_input("Waage leer (Zugmaschine)", value=daten["leer_real_antrieb"])
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll (Zugmaschine)", value=daten["voll_volvo_antrieb"])
    voll_real_antrieb = st.number_input("Waage voll (Zugmaschine)", value=daten["voll_real_antrieb"])
    teilbeladung_volvo_antrieb = st.number_input("Volvo Anzeige teilbeladen (Zugmaschine)", value=daten["teilbeladung_volvo_antrieb"])
    teilbeladung_real_antrieb = st.number_input("Waage teilbeladen (Zugmaschine)", value=daten["teilbeladung_real_antrieb"])

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten["leer_volvo_auflieger"])
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten["leer_real_auflieger"])
    voll_volvo_auflieger = st.number_input("Volvo Anzeige voll (Auflieger)", value=daten["voll_volvo_auflieger"])
    voll_real_auflieger = st.number_input("Waage voll (Auflieger)", value=daten["voll_real_auflieger"])
    teilbeladung_volvo_auflieger = st.number_input("Volvo Anzeige teilbeladen (Auflieger)", value=daten["teilbeladung_volvo_auflieger"])
    teilbeladung_real_auflieger = st.number_input("Waage teilbeladen (Auflieger)", value=daten["teilbeladung_real_auflieger"])

if st.button("💾 Kalibrierung speichern"):
    alle_daten[kennzeichen] = {
        "leer_volvo_antrieb": leer_volvo_antrieb,
        "leer_real_antrieb": leer_real_antrieb,
        "voll_volvo_antrieb": voll_volvo_antrieb,
        "voll_real_antrieb": voll_real_antrieb,
        "teilbeladung_volvo_antrieb": teilbeladung_volvo_antrieb,
        "teilbeladung_real_antrieb": teilbeladung_real_antrieb,
        "leer_volvo_auflieger": leer_volvo_auflieger,
        "leer_real_auflieger": leer_real_auflieger,
        "voll_volvo_auflieger": voll_volvo_auflieger,
        "voll_real_auflieger": voll_real_auflieger,
        "teilbeladung_volvo_auflieger": teilbeladung_volvo_auflieger,
        "teilbeladung_real_auflieger": teilbeladung_real_auflieger
    }
    speichere_daten(alle_daten)
    st.success("✅ Kalibrierung gespeichert")

st.header("📥 Eingabe aktueller Volvo-Werte")

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=voll_volvo_auflieger)

a1, b1 = berechne_kalibrierung(leer_volvo_antrieb, leer_real_antrieb, voll_volvo_antrieb, voll_real_antrieb, teilbeladung_volvo_antrieb, teilbeladung_real_antrieb)
a2, b2 = berechne_kalibrierung(leer_volvo_auflieger, leer_real_auflieger, voll_volvo_auflieger, voll_real_auflieger, teilbeladung_volvo_auflieger, teilbeladung_real_auflieger)

real_antrieb = volvo_now_antrieb * a1 + b1
real_auflieger = volvo_now_auflieger * a2 + b2
real_gesamt = real_antrieb + real_auflieger

st.header("📊 Ergebnis")

st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

# ✅ Antriebsachsen-Warnung
MAX_ANTRIEBSACHSE = 11.5
ueberladung_antrieb_kg = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) * 1000)
ueberladung_antrieb_pct = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) / MAX_ANTRIEBSACHSE * 100)

if ueberladung_antrieb_kg > 0:
    st.error(f"⚠️ Antriebsachse überladen: **{ueberladung_antrieb_kg:.0f} kg** / **{ueberladung_antrieb_pct:.1f} %**")
else:
    st.success("✅ Antriebsachse im grünen Bereich")

# ✅ Gesamtgewicht-Warnung
MAX_GESAMTGEWICHT = 40.0
ueberladung_gesamt_kg = max(0, (real_gesamt - MAX_GESAMTGEWICHT) * 1000)
ueberladung_gesamt_pct = max(0, (real_gesamt - MAX_GESAMTGEWICHT) / MAX_GESAMTGEWICHT * 100)

if ueberladung_gesamt_kg > 0:
    st.error(f"⚠️ Gesamtgewicht überladen: **{ueberladung_gesamt_kg:.0f} kg** / **{ueberladung_gesamt_pct:.1f} %**")
else:
    st.success("✅ Gesamtgewicht im grünen Bereich")

st.info("ℹ️ Hinweis: Teilbeladung ist optional – Felder leer lassen oder 0 eingeben, wenn keine Mittelwerte vorhanden sind.")
# Zusatzgewichte berücksichtigen
nutze_tank = st.checkbox("⛽ Tankfüllstand berücksichtigen?")
tank_kg = 0
if nutze_tank:
    tank_prozent = st.slider("Tankfüllstand (%)", 0, 100, 100)
    max_tankgewicht = 320  # z. B. 400 l Diesel ≈ 320 kg
    tank_kg = max_tankgewicht * (tank_prozent / 100)

nutze_paletten = st.checkbox("📦 Paletten im Palettenkorb?")
paletten_kg = 0
if nutze_paletten:
    paletten_anzahl = st.slider("Anzahl Paletten im Korb", 0, 36, 0)
    gewicht_pro_palette = 25  # kg pro Europalette
    paletten_kg = paletten_anzahl * gewicht_pro_palette

zusatzgewicht = (tank_kg + paletten_kg) / 1000  # Umrechnung in Tonnen
real_gesamt_korrigiert = real_gesamt + zusatzgewicht

st.subheader("📊 Ergebnis mit Zusatzgewichten")
st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
if nutze_tank:
    st.write(f"🔋 Tankgewicht: **{tank_kg:.0f} kg**")
if nutze_paletten:
    st.write(f"📦 Palettengewicht: **{paletten_kg:.0f} kg**")
st.write(f"📦 Gesamtgewicht (korrigiert): **{real_gesamt_korrigiert:.2f} t**")
