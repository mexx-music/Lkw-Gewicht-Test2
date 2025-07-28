import streamlit as st

st.set_page_config(page_title="LKW Gewicht", page_icon="🚛")
st.title("🚛 LKW Gewicht (Einfachversion ohne Speicherung)")

# Voreingestellte Kalibrierwerte – basierend auf bisherigen Messungen
leer_volvo_antrieb = 4.7
leer_real_antrieb = 7.5
voll_volvo_antrieb = 7.9
voll_real_antrieb = 11.3

leer_volvo_auflieger = 6.6
leer_real_auflieger = 8.5
voll_volvo_auflieger = 19.0
voll_real_auflieger = 27.5

# Kalibrierfaktoren berechnen
def berechne_kalibrierung(volvo1, real1, volvo2, real2):
    if volvo2 - volvo1 == 0:
        return 1.0, 0.0
    a = (real2 - real1) / (volvo2 - volvo1)
    b = real1 - a * volvo1
    return a, b

a1, b1 = berechne_kalibrierung(leer_volvo_antrieb, leer_real_antrieb, voll_volvo_antrieb, voll_real_antrieb)
a2, b2 = berechne_kalibrierung(leer_volvo_auflieger, leer_real_auflieger, voll_volvo_auflieger, voll_real_auflieger)

# Eingabe der aktuellen Volvo-Werte
st.header("📥 Aktuelle Werte")
volvo_now_antrieb = st.number_input("Volvo Anzeige – Zugmaschine", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Volvo Anzeige – Auflieger", value=voll_volvo_auflieger)

# Berechnung der realen Werte
real_antrieb = volvo_now_antrieb * a1 + b1
real_auflieger = volvo_now_auflieger * a2 + b2
real_gesamt = real_antrieb + real_auflieger

# Ausgabe
st.header("📊 Ergebnis")
st.write(f"🚛 Zugmaschine (real): **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger (real): **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

# Überladung der Antriebsachse prüfen
MAX_ANTRIEBSACHSE = 11.5
ueberladung_kg = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) * 1000)
ueberladung_prozent = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) / MAX_ANTRIEBSACHSE * 100)

if ueberladung_kg > 0:
    st.error(f"⚠️ Antriebsachse überladen: **{ueberladung_kg:.0f} kg** / **{ueberladung_prozent:.1f} %**")
else:
    st.success("✅ Antriebsachse im grünen Bereich")
