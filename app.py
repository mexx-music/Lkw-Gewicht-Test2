import streamlit as st
import json

# JSON-Datei laden
with open("kalibrierung.json", "r") as f:
    kalibrierung = json.load(f)

# Fahrzeugmodell auswählen
modell = st.selectbox("🚛 Fahrzeugmodell auswählen / wechseln", list(kalibrierung.keys()))
daten = kalibrierung[modell]

st.header("📬 Eingabe aktueller Volvo-Werte")

# Eingabe aktuelle Volvo-Werte
volvo_now_zug = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=0.0)
volvo_now_trailer = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=0.0)

# Kalibrierungswerte laden
leer_volvo_zug = daten["leer_volvo_antrieb"]
leer_real_zug = daten["leer_real_antrieb"]
voll_volvo_zug = daten["voll_volvo_antrieb"]
voll_real_zug = daten["voll_real_antrieb"]

leer_volvo_trailer = daten["leer_volvo_auflieger"]
leer_real_trailer = daten["leer_real_auflieger"]
voll_volvo_trailer = daten["voll_volvo_auflieger"]
voll_real_trailer = daten["voll_real_auflieger"]

# Umrechnungsformel (lineare Interpolation)
def berechne_gewicht(volvo_wert, leer_volvo, leer_real, voll_volvo, voll_real):
    if voll_volvo == leer_volvo:
        return leer_real
    return leer_real + (voll_real - leer_real) * ((volvo_wert - leer_volvo) / (voll_volvo - leer_volvo))

# Gewichte berechnen
gewicht_zug = berechne_gewicht(volvo_now_zug, leer_volvo_zug, leer_real_zug, voll_volvo_zug, voll_real_zug)
gewicht_trailer = berechne_gewicht(volvo_now_trailer, leer_volvo_trailer, leer_real_trailer, voll_volvo_trailer, voll_real_trailer)
gesamtgewicht = gewicht_zug + gewicht_trailer

# Ergebnis anzeigen
st.header("📊 Ergebnis")
st.markdown(f"🚛 Zugmaschine: **{gewicht_zug:.2f} t**")
st.markdown(f"🚚 Auflieger: **{gewicht_trailer:.2f} t**")
st.markdown(f"📦 Gesamtgewicht: **{gesamtgewicht:.2f} t**")

# Überladung prüfen
grenze = 11.5  # Antriebsachse max 11.5 t
if gewicht_zug > grenze:
    ueber = gewicht_zug - grenze
    prozent = (ueber / grenze) * 100
    st.error(f"⚠️ Antriebsachse überladen: {ueber*1000:.0f} kg / {prozent:.1f} % über dem Limit!")
else:
    st.success("✅ Antriebsachse im grünen Bereich.")
