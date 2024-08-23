import streamlit as st

def calculate_cykelforman(
    is_elcykel: bool,
    cykel_kostnad: float,
    antal_ar: int,
    service_kostnad: float,
    statslanerantan: float
):
    if is_elcykel:
        vardeminskning = cykel_kostnad * 0.20
    else:
        vardeminskning = cykel_kostnad / antal_ar

    ranta = (statslanerantan + 1.0) / 100
    kapitalkostnad = cykel_kostnad * ranta

    formansvarde = vardeminskning + service_kostnad + kapitalkostnad

    if formansvarde > 3000:
        beskattningsbart = formansvarde - 3000
    else:
        beskattningsbart = 0

    return {
        "Värdeminskning": round(vardeminskning, 2),
        "Service och reparationer": service_kostnad,
        "Kapitalkostnad": round(kapitalkostnad, 2),
        "Totalt förmånsvärde": round(formansvarde, 2),
        "Beskattningsbart belopp": round(beskattningsbart, 2)
    }

st.title("Cykelförmån Kalkylator")

st.write("""
Denna app hjälper dig att beräkna cykelförmån baserat på olika parametrar. 
Justera slidersen nedan och se resultatet i realtid!
""")

is_elcykel = st.checkbox("Är det en elcykel?")

col1, col2 = st.columns(2)

with col1:
    cykel_kostnad = st.slider("Cykelns kostnad (SEK)", min_value=1000, max_value=50000, value=5000, step=100)
    antal_ar = st.slider("Antal år cykeln förväntas hålla", min_value=1, max_value=10, value=6, step=1)

with col2:
    service_kostnad = st.slider("Årlig kostnad för service och reparationer (SEK)", min_value=0, max_value=2000, value=300, step=50)
    statslanerantan = st.slider("Statslåneräntan (%)", min_value=0.0, max_value=10.0, value=2.62, step=0.01)

resultat = calculate_cykelforman(is_elcykel, cykel_kostnad, antal_ar, service_kostnad, statslanerantan)

st.write("### Resultat")
for key, value in resultat.items():
    st.write(f"**{key}:** {value:.2f} SEK")

if resultat["Beskattningsbart belopp"] > 0:
    st.write("Du behöver beskattas för cykelförmånen.")
else:
    st.write("Du behöver inte beskattas för cykelförmånen.")

st.write("""
### Förklaring
- För vanliga cyklar beräknas värdeminskningen som cykelns kostnad delat med antalet år den förväntas hålla.
- För elcyklar beräknas värdeminskningen som 20% av cykelns kostnad per år.
- Kapitalkostnaden beräknas som cykelns kostnad multiplicerat med (statslåneräntan + 1%).
- Om det totala förmånsvärdet överstiger 3000 SEK, beskattas skillnaden.
""")
