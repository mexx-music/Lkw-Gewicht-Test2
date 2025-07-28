import streamlit as st
import json

st.set_page_config(page_title="LKW-Gewicht Rechner", page_icon="🚛")

# Kalibrierdaten laden
with open("kalibrierung.json", "r") as f:
    kalibrierungen = json.load(f)

modelle = list(kalibrierungen.keys())
modell = st.selectbox("🚛 Fahrzeugmodell auswählen / wechseln", modelle)

daten = kalibrierungen[modell]

volvo_now_zug = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=0.0)
volvo_now_trailer = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=0.0)

leer_volvo_antrieb = daten["leer_volvo_antrieb"]
leer_real_antrieb = daten["leer_real_antrieb"]
voll_volvo_antrieb = daten["voll_volvo_antrieb"]
voll_real_antrieb = daten["voll_real_antrieb"]

leer_volvo_auflieger = daten["leer_volvo_auflieger"]
leer_real_auflieger = daten["leer_real_auflieger"]
voll_volvo_auflieger = daten["voll_volvo_auflieger"]
voll_real_auflieger = daten["voll_real_auflieger"]

# Lineare Umrechnung
def berechne_gewicht(volvo_wert, leer_volvo, leer_real, voll_volvo, voll_real):
    if voll_volvo == leer_volvo:
        return 0
    faktor = (voll_real - leer_real) / (voll_volvo - leer_volvo)
    return round(leer_real + faktor * (volvo_wert - leer_volvo), 2)

gewicht_zug = berechne_gewicht(volvo_now_zug, leer_volvo_antrieb, leer_real_antrieb, voll_volvo_antrieb, voll_real_antrieb)
gewicht_trailer = berechne_gewicht(volvo_now_trailer, leer_volvo_auflieger, leer_real_auflieger, voll_volvo_auflieger, voll_real_auflieger)
gesamtgewicht = round(gewicht_zug + gewicht_trailer, 2)

st.markdown("## 📊 Ergebnis")
st.markdown(f"🚚 Zugmaschine: **{gewicht_zug} t**")
st.markdown(f"🚛 Auflieger: **{gewicht_trailer} t**")
st.markdown(f"📦 Gesamtgewicht: **{gesamtgewicht} t**")

if gewicht_zug > 11.5:
    overload = round((gewicht_zug - 11.5) * 1000)
    st.error(f"⚠️ Antriebsachse überladen: {overload} kg / {round(overload / 11500 * 100, 1)} % über dem Limit!")
