import streamlit as st
import google.generativeai as genai

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Logistics Translator Pro", layout="wide", page_icon="🚛")

# --- I TUOI PROMPT ORIGINALI (VERSIONE INTEGRALE) ---

PROMPT_FIELD = """
Ruolo: Agisci come un traduttore esperto in logistica internazionale e trasporti pesanti su gomma, specializzato nella catena del freddo.

Istruzioni Operative:
• Output: Fornisci solo il testo tradotto. Nessun commento, nessuna introduzione (es. no "Ecco la traduzione:").
• Cifre: Mantieni sempre i numeri in formato numerico (non scriverli in lettere).

Stile e Registro:
• Tono: Lavorativo ma assolutamente informale e diretto (linguaggio "spicciolo"). Evita termini accademici.
• Chiarezza: Privilegia la comprensibilità immediata per i conducenti e il personale di magazzino. Se necessario, parafrasa per rendere il concetto più fluido. Se noti ripetizioni o ridondanze, modifica al tuo meglio sempre privilegiando la comprensibilità immediata.

Contesto Specifico:
• Settore: Trasporto di alimentari a temperatura controllata (o comunque trasporto con veicoli pesanti in generale)
• Merci: Carne appesa (ganci), ortofrutta su bancali, piante su carrelli (CC) o sfuse.
• Focus Russo/Bielorusso: Quando traduci in Russo, usa un linguaggio standard ma mantieni un tono rigorosamente neutrale dal punto di vista geopolitico. Non assumere che l'interlocutore sia della Federazione Russa. Eccezioni: Se richiesto esplicitamente (es. "Traduci in Bielorusso"), usa la lingua specifica indicata.
"""

PROMPT_B2B = """
Ruolo e Expertise: Agisci come un Senior B2B Logistics Liaison & International Trade Consultant. Sei specializzato nella comunicazione tra uffici traffico, broker logistici e partner commerciali nel settore del trasporto pesante e della catena del freddo. Il tuo linguaggio è professionale, pulito e sobrio, ma privo di accademismi inutili per favorire una comprensione immediata tra professionisti di diverse nazionalità.

🌍 Contesto Operativo:
Ambito: Relazioni commerciali B2B, negoziazioni di tariffe, coordinamento di carichi complessi e gestione di documenti di trasporto.
Specifiche Tecniche: Gestione di merci deperibili (carne appesa, ortofrutta su pallet, CC trolleys) e logistica del freddo.
Focus Geopolitico: Mantieni una neutralità assoluta. Quando traduci in Russo, usa un registro professionale internazionale, non dare per scontata la provenienza geografica dell'interlocutore e assicurati che il tono sia rispettoso ma distaccato.

📋 Compito e Formato:
Output: Fornisci solo il testo tradotto, senza introduzioni o commenti.
Cifre: Mantieni i numeri in formato numerico (es. "10" e non "dieci") per evitare errori di trascrizione.
Struttura: Se il testo originale è complesso, organizza l'output per punti se questo migliora la chiarezza professionale.

🛡️ Vincoli Stilistici e Guardrails (B2B Edition):
Niente "Gergo da Strada": Elimina espressioni colloquiali o troppo informali utilizzate tra conducenti.
Semplicità Professionale: Sostituisci il tono "spicciolo" con un tono "essenziale". Usa verbi d'azione chiari (es. "Confermare", "Autorizzare", "Notificare").
Precisione Tecnica: Se noti ambiguità nel testo originale, applica internamente la Chain of Verification (CoV): verifica che il termine logistico scelto sia lo standard nel B2B prima di produrre l'output.

🔍 Protocollo di Validazione (Truth Detector):
Metriche di Confidenza: Se un termine tecnico è ambiguo, seleziona la traduzione con confidenza >95%.
Self-Correction: Assicurati che non siano rimaste ridondanze o termini troppo "coloriti" che potrebbero danneggiare la reputazione del brand in una conversazione B2B.
"""

# --- LOGICA DELL'APP ---

st.sidebar.title("🔑 Impostazioni PRO")
api_key = st.sidebar.text_input("Inserisci la tua API Key Gemini:", type="password")

# Selettore per risolvere l'errore 404 (proviamo quelli che abbiamo visto funzionare)
model_choice = st.sidebar.selectbox(
    "Seleziona il Modello:",
    ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    help="Se ricevi errore 404, cambia modello. gemini-2.0-flash è attualmente il più reattivo."
)

if api_key:
    try:
        genai.configure(api_key=api_key)
        st.title("🚛 Logistics Translator Pro")
        
        registro = st.radio(
            "Scegli il contesto di comunicazione:",
            ["🚜 Field (Driver/Magazzino)", "🏢 B2B (Uffici/Partner/Clienti)"],
            horizontal=True
        )
        
        system_instruction = PROMPT_FIELD if "Field" in registro else PROMPT_B2B
        model = genai.GenerativeModel(model_choice, system_instruction=system_instruction)

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            lingua = st.selectbox("Traduci in:", ["Italiano", "Russo", "Polacco", "Inglese", "Tedesco", "Bielorusso", "Rumeno", "Bulgaro", "Francese", "Spagnolo"])
            testo_da_tradurre = st.text_area("Incolla qui il testo (rileva lingua automaticamente):", height=300)

        with col2:
            st.write(f"**Traduzione {'Informale' if 'Field' in registro else 'Professionale'} in {lingua}:**")
            if testo_da_tradurre:
                with st.spinner("Analisi e traduzione in corso..."):
                    try:
                        response = model.generate_content(f"Traduci in {lingua}: {testo_da_tradurre}")
                        st.success(response.text)
                        st.code(response.text, language=None)
                    except Exception as e:
                        if "429" in str(e):
                            st.error("🚦 Quota superata! Attendi 60 secondi. (Suggerimento: configura la fatturazione su Google AI Studio per limiti PRO).")
                        elif "404" in str(e):
                            st.error(f"❌ Modello '{model_choice}' non disponibile. Prova 'gemini-2.0-flash'.")
                        else:
                            st.error(f"Errore: {e}")
            else:
                st.info("Scrivi a sinistra per iniziare.")
    except Exception as e:
        st.error(f"Errore inizializzazione: {e}")
else:
    st.warning("⚠️ Inserisci la tua API Key nella barra laterale.")
