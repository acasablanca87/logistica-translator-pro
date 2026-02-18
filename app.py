import streamlit as st
import google.generativeai as genai

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Logistics Translator Pro", layout="wide", page_icon="🚛")

# --- I TUOI PROMPT ORIGINALI ---
PROMPT_FIELD = """
Ruolo: Agisci come un traduttore esperto in logistica internazionale e trasporti pesanti su gomma, specializzato nella catena del freddo.
Output: Fornisci solo il testo tradotto. Nessun commento, nessuna introduzione.
Cifre: Mantieni sempre i numeri in formato numerico.
Stile: Tono lavorativo ma assolutamente informale e diretto (linguaggio "spicciolo").
Contesto: Trasporto alimentari, carne appesa, ortofrutta, piante CC.
Focus Russo/Bielorusso: Tono neutrale geopoliticamente.
"""

PROMPT_B2B = """
Ruolo: Senior B2B Logistics Liaison & International Trade Consultant.
Ambito: Relazioni commerciali, negoziazioni, uffici traffico.
Stile: Professionale, pulito e sobrio. Tono "essenziale" e verbi d'azione (Confermare, Autorizzare).
Output: Solo testo tradotto. Se complesso, usa i punti elenco.
Focus Geopolitico: Neutralità assoluta e registro professionale internazionale.
"""

# --- INTERFACCIA APP ---
st.sidebar.title("🔑 Accesso")
api_key = st.sidebar.text_input("Inserisci la tua API Key Gemini:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    st.title("🚛 Logistics Translator Pro")
    
    registro = st.radio(
        "Scegli il contesto di comunicazione:",
        ["🚜 Field (Driver/Magazzino)", "🏢 B2B (Uffici/Partner/Clienti)"],
        horizontal=True
    )
    
    system_instruction = PROMPT_FIELD if "Field" in registro else PROMPT_B2B
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        lingua = st.selectbox("Traduci in:", ["Russo", "Polacco", "Inglese", "Tedesco", "Bielorusso", "Rumeno", "Bulgaro", "Francese", "Spagnolo"])
        testo_da_tradurre = st.text_area("Inserisci il testo in Italiano:", height=250, placeholder="Es: Il carico deve viaggiare a 2 gradi...")

    with col2:
        st.write(f"**Traduzione {'Informale' if 'Field' in registro else 'Professionale'} in {lingua}:**")
        if testo_da_tradurre:
            try:
                response = model.generate_content(f"Traduci in {lingua}: {testo_da_tradurre}")
                st.success(response.text)
                st.code(response.text, language=None) 
            except Exception as e:
                st.error(f"Errore: {e}")
        else:
            st.info("In attesa di testo...")
else:
    st.warning("⚠️ Inserisci la tua API Key nella barra laterale per iniziare.")
