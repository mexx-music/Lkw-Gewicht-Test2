import streamlit as st

# 🚛 LKW Gewicht App mit Backup-Faktor und Beispielprofil WL782GW

st.set_page_config(page_title="LKW Gewicht (Schätzung)", page_icon="🚛")
st.title("🚛 LKW Gewicht berechnen – mit Backup-Kalibrierung")

# Beispiel-Daten für WL782GW
default_profile = {
    "leer_volvo_antrieb": 5.5,
    "leer_real_antrieb": 8.0,
    "voll_volvo_antrieb": 11.0,
    "voll_real_antrieb": 12.7,
    "leer_volvo_auflieger": 6.5,
    "leer_real_auflieger": 9.0,
    "voll_volvo_auflieger": 24.0,
    "voll_real_auflieger": 27.3
}

# Backup-Faktor, wenn keine Kalibrierung vorhanden (35 t Anzeige = 40 t real)
BACKUP_FACTOR = 40 / 35

# Eingabe
kennzeichen = st.text_input("Kennzeichen eingeben", value="WL782GW")

volvo_now_antrieb = st.number_input("Volvo Anzeige – Zugmaschine (Antriebsachse)", value=11.0)
volvo_now_auflieger = st.number_input("Volvo Anzeige – Auflieger (gesamt)", value=24.0)

# Auswahl ob exakte Kalibrierung verwendet werden soll (nur für WL782GW)
if kennzeichen == "WL782GW":
    a1 = (default_profile["voll_real_antrieb"] - default_profile["leer_real_antrieb"]) / (default_profile["voll_volvo_antrieb"] - default_profile["leer_volvo_antrieb"])
    b1 = default_profile["leer_real_antrieb"] - a1 * default_profile["leer_volvo_antrieb"]
    a2 = (default_profile["voll_real_auflieger"] - default_profile["leer_real_auflieger"]) / (default_profile["voll_volvo_auflieger"] - default_profile["leer_volvo_auflieger"])
    b2 = default_profile["leer_real_auflieger"] - a2 * default_profile["leer_volvo_auflieger"]

    real_antrieb = volvo_now_antrieb * a1 + b1
    real_auflieger = volvo_now_auflieger * a2 + b2
    methode = "Profil WL782GW verwendet"
else:
    real_antrieb = volvo_now_antrieb * BACKUP_FACTOR
    real_auflieger = volvo_now_auflieger * BACKUP_FACTOR
    methode = "Backup-Schätzung (Faktor 1.142857)"

gesamtgewicht = real_antrieb + real_auflieger

# Ausgabe
st.header("📊 Ergebnis")
st.write(f"🔢 Methode: **{methode}**")
st.write(f"🚛 Zugmaschine (geschätzt): **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger (geschätzt): **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{gesamtgewicht:.2f} t**")
# Maximale Achslast laut EU-Richtlinie
MAX_ANTRIEBSACHSE = 11.5  # in Tonnen

# Berechnung der Überladung
ueberladung_kg = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) * 1000)
ueberladung_prozent = max(0, (real_antrieb - MAX_ANTRIEBSACHSE) / MAX_ANTRIEBSACHSE * 100)

st.header("⚖️ Achslast-Kontrolle")

if ueberladung_kg > 0:
    st.error(f"⚠️ Antriebsachse überladen: **{ueberladung_kg:.0f} kg** / **{ueberladung_prozent:.1f} %** über dem Limit!")
else:
    st.success("✅ Antriebsachse im grünen Bereich")
