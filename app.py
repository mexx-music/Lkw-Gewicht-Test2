import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

with st.expander("ℹ️ App-Info / Anleitung"):
    st.markdown("""
    ### ℹ️ LKW-Gewichtsrechner – Anleitung

    **Was kann die App?**
    - Schätzt dein aktuelles Gesamtgewicht anhand der Volvo-Anzeigen.
    - Unterstützt Tankfüllstand & Paletten als Zusatzgewicht.
    - Warnt bei Überschreitung der Achslast oder des Gesamtgewichts.

    **Wie kalibrieren?**
    1. Leer fahren → Werte eintragen unter 🟢 **„Leer eingeben“**
    2. Voll beladen (z. B. auch 39,3 t reicht) → 🔵 **„Voll eingeben“**
    3. Optional auch 🟡 **„Teilbeladen eingeben“**

    Die App berechnet daraus automatisch eine Gewichtskurve.

    **Hinweise:**
    - Je größer der Unterschied zwischen „leer“ und „voll“, desto genauer die Berechnung.
    - Die App ersetzt keine offizielle (geeichte) Fahrzeugwaage.
    - Kalibrierung wird automatisch pro Kennzeichen gespeichert.
    """)



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
        nenner = sum((x[i] - xm)**2 for i in range(3))
        if nenner == 0:
            return 1.0, 0.0
        a = sum((x[i] - xm)*(y[i] - ym) for i in range(3)) / nenner
        b = ym - a * xm
        return a, b
    else:
        if volvo2 - volvo1 == 0:
            return 1.0, 0.0
        a = (real2 - real1) / (volvo2 - volvo1)
        b = real1 - a * volvo1
        return a, b

kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=daten["voll_volvo_antrieb"])
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=daten["voll_volvo_auflieger"])

nutze_tank = st.checkbox("⛽ Tankfüllstand berücksichtigen?")
tank_kg = 0
if nutze_tank:
    tank_prozent = st.slider("Tankfüllstand", 0, 100, 100, step=10)
    max_tankgewicht = 320
    tank_kg = max_tankgewicht * (tank_prozent / 100)

nutze_paletten = st.checkbox("📦 Paletten im Palettenkorb berücksichtigen?")
paletten_kg = 0
if nutze_paletten:
    paletten_anzahl = st.slider("Anzahl Paletten im Korb", 0, 36, 0)
    gewicht_pro_palette = 25
    paletten_kg = paletten_anzahl * gewicht_pro_palette

a1, b1 = berechne_kalibrierung(daten["leer_volvo_antrieb"], daten["leer_real_antrieb"],
                               daten["voll_volvo_antrieb"], daten["voll_real_antrieb"],
                               daten["teilbeladung_volvo_antrieb"], daten["teilbeladung_real_antrieb"])
a2, b2 = berechne_kalibrierung(daten["leer_volvo_auflieger"], daten["leer_real_auflieger"],
                               daten["voll_volvo_auflieger"], daten["voll_real_auflieger"],
                               daten["teilbeladung_volvo_auflieger"], daten["teilbeladung_real_auflieger"])

real_antrieb = volvo_now_antrieb * a1 + b1
real_auflieger = volvo_now_auflieger * a2 + b2
real_gesamt = real_antrieb + real_auflieger
zusatzgewicht = (tank_kg + paletten_kg) / 1000
real_gesamt_korrigiert = real_gesamt + zusatzgewicht

st.header("📊 Ergebnis")
st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"⚙️ Zusatzgewicht: **{zusatzgewicht:.2f} t**")
st.write(f"📦 Gesamtgewicht (inkl. Zusatz): **{real_gesamt_korrigiert:.2f} t**")

MAX_ANTRIEBSACHSE = 11.5
MAX_GESAMT = 40.0
ueber_antrieb = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) * 1000)
ueber_antrieb_pct = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) / MAX_ANTRIEBSACHSE * 100)
ueber_gesamt = max(0, (real_gesamt_korrigiert - MAX_GESAMT) * 1000)
ueber_gesamt_pct = max(0, (real_gesamt_korrigiert - MAX_GESAMT) / MAX_GESAMT * 100)

if ueber_antrieb > 0:
    st.error(f"⚠️ Antriebsachse überladen: **{ueber_antrieb:.0f} kg** / **{ueber_antrieb_pct:.1f}%**")
else:
    st.success("✅ Antriebsachse im grünen Bereich")

if ueber_gesamt > 0:
    st.error(f"⚠️ Gesamtgewicht überladen: **{ueber_gesamt:.0f} kg** / **{ueber_gesamt_pct:.1f}%**")
else:
    st.success("✅ Gesamtgewicht im grünen Bereich")

st.header("🛠 Geführte Kalibrierung (Leer / Teil / Voll)")

if "active_kalibrierung" not in st.session_state:
    st.session_state["active_kalibrierung"] = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 Leer eingeben"):
        st.session_state["active_kalibrierung"] = "leer"
with col2:
    if st.button("🟡 Teilbeladen eingeben"):
        st.session_state["active_kalibrierung"] = "teil"
with col3:
    if st.button("🔵 Voll eingeben"):
        st.session_state["active_kalibrierung"] = "voll"

auswahl = st.session_state.get("active_kalibrierung")
if auswahl:
    st.markdown(f"### 📥 Bitte Werte für **{auswahl.upper()}** eingeben:")
    volvo_zug = st.number_input("📟 Volvo-Anzeige Zugmaschine (t)", key=f"{auswahl}_volvo_zug")
    waage_zug = st.number_input("⚖️ Waagewert Zugmaschine (t)", key=f"{auswahl}_waage_zug")
    volvo_trailer = st.number_input("📟 Volvo-Anzeige Auflieger (t)", key=f"{auswahl}_volvo_trailer")
    waage_trailer = st.number_input("⚖️ Waagewert Auflieger (t)", key=f"{auswahl}_waage_trailer")
    if st.button("💾 Speichern", key=f"{auswahl}_save"):
        daten[f"{auswahl}_volvo_antrieb"] = volvo_zug
        daten[f"{auswahl}_real_antrieb"] = waage_zug
        daten[f"{auswahl}_volvo_auflieger"] = volvo_trailer
        daten[f"{auswahl}_real_auflieger"] = waage_trailer
        alle_daten[kennzeichen] = daten
        speichere_daten(alle_daten)
        st.success(f"✅ Kalibrierung '{auswahl.upper()}' gespeichert!")

    if st.button("❌ Fenster schließen", key=f"{auswahl}_close"):
        st.session_state["active_kalibrierung"] = None
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
