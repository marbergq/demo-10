import streamlit as st

def berakna_kapitalkostnad(inköpspris, statslåneränta):
    return inköpspris * (statslåneränta / 100 + 1) / 100

def berakna_cykelforman(cykeltyp, inköpspris, år_att_hålla, service_kostnad, statslåneränta):
    if cykeltyp == "Vanlig cykel":
        värdeminskning = inköpspris / år_att_hålla
    elif cykeltyp == "Elcykel":
        värdeminskning = inköpspris * 0.20  # 20% årlig värdeminskning för elcyklar
    else:
        raise ValueError("Ogiltig cykeltyp. Använd 'Vanlig cykel' eller 'Elcykel'.")

    kapitalkostnad = berakna_kapitalkostnad(inköpspris, statslåneränta)
    
    förmånsvärde = värdeminskning + service_kostnad + kapitalkostnad
    
    if förmånsvärde <= 3000:
        skattepliktig_förmån = 0
    else:
        skattepliktig_förmån = förmånsvärde - 3000
    
    return {
        "Värdeminskning": round(värdeminskning, 2),
        "Service och reparationer": service_kostnad,
        "Kapitalkostnad": round(kapitalkostnad, 2),
        "Totalt förmånsvärde": round(förmånsvärde, 2),
        "Skattepliktig förmån": round(skattepliktig_förmån, 2)
    }

st.title("Cykelförmån Kalkylator")

st.write("""
Denna app beräknar cykelförmån baserat på de regler som gäller för beskattning av cykelförmån.
Justera parametrarna nedan med slidersen för att beräkna förmånsvärdet och den skattepliktiga förmånen.
""")

cykeltyp = st.selectbox("Välj cykeltyp", ["Vanlig cykel", "Elcykel"])

col1, col2 = st.columns(2)

with col1:
    inköpspris = st.slider("Inköpspris (kr)", min_value=1000, max_value=50000, value=5000, step=100)
    år_att_hålla = st.slider("Antal år cykeln förväntas hålla", min_value=1, max_value=10, value=6)

with col2:
    service_kostnad = st.slider("Årlig kostnad för service och reparationer (kr)", min_value=0, max_value=2000, value=300, step=50)
    statslåneränta = st.slider("Statslåneränta (%)", min_value=0.0, max_value=10.0, value=2.62, step=0.01)

if st.button("Beräkna förmån"):
    try:
        resultat = berakna_cykelforman(cykeltyp, inköpspris, år_att_hålla, service_kostnad, statslåneränta)
        
        st.subheader("Resultat:")
        for key, value in resultat.items():
            st.write(f"{key}: {value:.2f} kr")
        
        if resultat["Skattepliktig förmån"] > 0:
            st.warning(f"Du behöver betala skatt på {resultat['Skattepliktig förmån']:.2f} kr av förmånsvärdet.")
        else:
            st.success("Du behöver inte betala någon skatt på denna förmån.")
    except ValueError as e:
        st.error(str(e))

st.info("""
OBS: Denna kalkylator är baserad på förenklade regler och bör endast användas som en uppskattning. 
För exakta beräkningar och aktuella regler, vänligen kontakta Skatteverket eller en skatteexpert.
""")
