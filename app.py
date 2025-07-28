
import streamlit as st

st.title("🚛 LKW Gewichtsanalyse")

st.header("🔧 Kalibrierung")

leer_volvo = st.number_input("Volvo-Anzeige (leer)", value=12.0)
leer_waage = st.number_input("Tatsächliches Gewicht (leer)", value=13.2)
voll_volvo = st.number_input("Volvo-Anzeige (voll)", value=40.0)
voll_waage = st.number_input("Tatsächliches Gewicht (voll)", value=41.5)

if voll_volvo != leer_volvo:
    faktor = (voll_waage - leer_waage) / (voll_volvo - leer_volvo)
else:
    faktor = 1.0

st.write(f"⚙️ Automatisch berechneter Korrekturfaktor: `{faktor:.3f}`")

st.header("📊 Unterwegs-Kontrolle")

aktuelle_volvo = st.number_input("Aktuelle Volvo-Anzeige", value=36.0)
geschaetztes_gewicht = leer_waage + (aktuelle_volvo - leer_volvo) * faktor

st.success(f"🚦 Geschätztes Gesamtgewicht: **{geschaetztes_gewicht:.2f} t**")
