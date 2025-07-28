import streamlit as st

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

# Standard-Kalibrierwerte aus realen Messungen
VOLVO_ANTRIEB_LEER = 4.7
REAL_ANTRIEB_LEER = 7.5
VOLVO_ANTRIEB_VOLL = 7.9
REAL_ANTRIEB_VOLL = 11.3

VOLVO_AUFLIEGER_LEER = 6.6
REAL_AUFLIEGER_LEER = 8.5
VOLVO_AUFLIEGER_VOLL = 19.0
REAL_AUFLIEGER_VOLL = 27.5

# Kalibrierformel
def kalibriere(volvo_wert, v1, r1, v2, r2):
    a = (r2 - r1) / (v2 - v1)
    b = r1 - a * v1
    return volvo_wert * a + b

st.subheader("Eingabe der Volvo-Anzeigen:")
volvo_antrieb = st.number_input("Volvo Antrieb (t)", value=VOLVO_ANTRIEB_VOLL)
volvo_auflieger = st.number_input("Volvo Auflieger (t)", value=VOLVO_AUFLIEGER_VOLL)

real_antrieb = kalibriere(volvo_antrieb, VOLVO_ANTRIEB_LEER, REAL_ANTRIEB_LEER, VOLVO_ANTRIEB_VOLL, REAL_ANTRIEB_VOLL)
real_auflieger = kalibriere(volvo_auflieger, VOLVO_AUFLIEGER_LEER, REAL_AUFLIEGER_LEER, VOLVO_AUFLIEGER_VOLL, REAL_AUFLIEGER_VOLL)
real_gesamt = real_antrieb + real_auflieger

st.subheader("Ergebnisse:")
st.write(f"Antriebsachse (geschätzt): **{real_antrieb:.2f} t**")
st.write(f"Auflieger (geschätzt): **{real_auflieger:.2f} t**")
st.write(f"Gesamtgewicht (geschätzt): **{real_gesamt:.2f} t**")

# Überladung
MAX_ANTRIEBSACHSE = 11.5
if real_antrieb > MAX_ANTRIEBSACHSE:
    diff = (real_antrieb - MAX_ANTRIEBSACHSE) * 1000
    st.error(f"⚠️ Überladung Antriebsachse: {diff:.0f} kg über dem Limit!")
else:
    st.success("✅ Antriebsachse im grünen Bereich.")
