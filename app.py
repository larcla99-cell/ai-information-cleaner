import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# API-nøkkel
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Information Cleaner", page_icon="🧠")

st.title("🧠 AI Information Cleaner")
st.write("Rydd opp i rotete tekst eller analyser PDF-dokumenter.")

# Velg modus
mode = st.selectbox(
    "Hva vil du gjøre?",
    [
        "Oppsummer tekst",
        "Organiser notater",
        "Forklar vanskelig tekst"
    ]
)

# Velg input-type
input_type = st.radio(
    "Velg input-type",
    ["Lim inn tekst", "Last opp PDF"]
)

text = ""

# Tekstinput
if input_type == "Lim inn tekst":
    text = st.text_area(
        "Lim inn tekst",
        height=200,
        placeholder="Lim inn notater, dokumenter eller rotete tekst..."
    )

# PDF-opplasting
elif input_type == "Last opp PDF":

    uploaded_file = st.file_uploader("Last opp PDF", type="pdf")

    if uploaded_file is not None:

        reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text

        text = pdf_text

        st.success("PDF lastet inn!")

        # Vis litt av teksten
        st.subheader("Forhåndsvisning av PDF-tekst")
        st.write(text[:1500] + "...")

# Analyse
if st.button("Analyser"):

    if text.strip() == "":
        st.warning("Ingen tekst funnet.")
    else:

        if mode == "Oppsummer tekst":
            prompt = f"""
Lag en kort og klar oppsummering av teksten under.

Tekst:
{text}
"""

        elif mode == "Organiser notater":
            prompt = f"""
Du er en ekspert på å rydde opp i rotete informasjon.

1. Lag en kort oppsummering
2. Lag hovedpunkter
3. Lag strukturert versjon

Tekst:
{text}
"""

        elif mode == "Forklar vanskelig tekst":
            prompt = f"""
Forklar teksten under på en enkel måte.

1. Forklar hovedideen
2. Gi et eksempel
3. Forklar viktige begreper

Tekst:
{text}
"""

        with st.spinner("AI analyserer..."):

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

        result = response.output_text

        st.success("Ferdig!")
        st.write(result)

        # Nedlastbar fil
        st.download_button(
            label="Last ned resultat",
            data=result,
            file_name="ai_analyse.txt",
            mime="text/plain"
        )