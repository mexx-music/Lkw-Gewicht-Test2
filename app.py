import json
import os
import streamlit as st

# ---------------------------
# Hilfsfunktionen
# ---------------------------

DATA_FILE = "kalibrierung.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def korrigiere_werte(zug, trailer, option, beladungsgrad):
    # Palettenkorb-Korrektur (in kg)
    KORREKTUR = 800
    if option == "ohne":
        return zug, trailer
    elif option == "nur_leer":
        trailer += KORREKTUR * (1 - beladungsgrad)
    elif option == "voll_und_leer":
        trailer += KORREKTUR
    return zug, trailer

def berechne_gewicht(volvo_zug, volvo_trailer, leer, voll):
    def faktor(basis_volvo, basis_real):
        return (basis_real[1] - basis_real[0]) / (basis_volvo[1] - basis_volvo[0]) if basis_volvo[1] != basis_volvo[0] else 1.0

    zug_factor = faktor([leer["zug"], voll["zug"]], [leer["real_zug"], voll["real_zug"]])
    trailer_factor = faktor([leer["trailer"], voll["trailer"]], [leer["real_trailer"], voll["real_trailer"]])

    zug_real = leer["real_zug"] + (volvo_zug - leer["zug"]) * zug_factor
    trailer_real = leer["real_trailer"] + (volvo_trailer - leer["trailer"]) * trailer_factor

    return zug_real, trailer_real

# ---------------------------
# Streamlit App
# ---------------------------

st.set_page_config(page_title="🚛 LKW-Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht mit Palettenkorb-Korrektur")

kalibrier_data = load_data()

kennzeichen = st.text_input("Kennzeichen / Profil", value="Volvo-Test")

volvo_zug = st.number_input("Volvo-Anzeige Zugmaschine (t)", 0.0, 30.0, 4.7, 0.1)
volvo_trailer = st.number_input("Volvo-Anzeige Auflieger (t)", 0.0, 40.0, 6.6, 0.1)

beladungsgrad = st.slider("Beladungsgrad (%)", 0, 100, 0) / 100.0

palettenkorb_option = st.radio(
    "Palettenkorb",
    options=["ohne", "nur_leer", "voll_und_leer"],
    index=0
)

zug_korr, trailer_korr = korrigiere_werte(volvo_zug, volvo_trailer, palettenkorb_option, beladungsgrad)

st.markdown(f"**Korrigierte Werte:** Zug = {zug_korr:.2f} t, Trailer = {trailer_korr:.2f} t, Gesamt = {zug_korr + trailer_korr:.2f} t")

if kennzeichen not in kalibrier_data:
    kalibrier_data[kennzeichen] = {
        "leer": None,
        "voll": None,
        "aktiv": True
    }

st.subheader("Kalibrierung")
if st.button("Aktuellen Wert als Leer speichern"):
    kalibrier_data[kennzeichen]["leer"] = {"zug": zug_korr, "trailer": trailer_korr, "real_zug": zug_korr, "real_trailer": trailer_korr}
    save_data(kalibrier_data)
    st.success("Leer-Kalibrierung gespeichert!")

if st.button("Aktuellen Wert als Voll speichern"):
    kalibrier_data[kennzeichen]["voll"] = {"zug": zug_korr, "trailer": trailer_korr, "real_zug": zug_korr, "real_trailer": trailer_korr}
    save_data(kalibrier_data)
    st.success("Voll-Kalibrierung gespeichert!")

aktiv_status = st.checkbox("Kalibrierpunkt aktiv?", value=kalibrier_data[kennzeichen]["aktiv"])
kalibrier_data[kennzeichen]["aktiv"] = aktiv_status
save_data(kalibrier_data)

if st.button("Reales Gewicht berechnen"):
    leer = kalibrier_data[kennzeichen]["leer"]
    voll = kalibrier_data[kennzeichen]["voll"]

    if leer and voll:
        zug_real, trailer_real = berechne_gewicht(volvo_zug, volvo_trailer, leer, voll)
        st.success(f"Reales Gewicht: Zug = {zug_real:.2f} t, Trailer = {trailer_real:.2f} t, Gesamt = {zug_real + trailer_real:.2f} t")
    else:
        st.warning("Bitte erst Leer- und Voll-Kalibrierung speichern.")

st.subheader("Gespeicherte Kalibrierpunkte")
st.json(kalibrier_data)
