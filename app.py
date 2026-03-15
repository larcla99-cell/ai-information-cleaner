import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Study Assistant", page_icon="🧠", layout="wide")

# ---------- HEADER ----------

st.title("🧠 AI Study Assistant")

st.header("📚 Study smarter with AI")

st.write(
"""
Upload lecture notes or PDFs and instantly get:

• Summary  
• Flashcards  
• Quiz questions  
• Key concepts  
• Explanations at your level
"""
)

st.info("Paste text or upload a PDF to begin.")

st.divider()

# ---------- SESSION STATE ----------

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- SIDEBAR CONTROLS ----------

st.sidebar.header("⚙️ Settings")

mode = st.sidebar.selectbox(
    "Function",
    [
        "Oppsummer tekst",
        "Organiser notater",
        "Forklar tekst",
        "Chat med dokument",
        "Finn nøkkelinnsikt",
        "Lag flashcards",
        "Lag quiz"
    ]
)

level = st.sidebar.selectbox(
    "Explanation level",
    ["Veldig enkelt", "Normalt", "Ekspert"]
)

input_type = st.sidebar.radio(
    "Input type",
    ["Lim inn tekst", "Last opp PDF"]
)

# ---------- INPUT ----------

text = ""

if input_type == "Lim inn tekst":

    text = st.text_area(
        "Text input",
        height=250,
        placeholder="Paste lecture notes, articles or documents..."
    )

elif input_type == "Last opp PDF":

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:

        reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                pdf_text += page_text

        text = pdf_text

        st.success("PDF loaded")

        with st.expander("Preview document"):
            st.write(text[:1500] + "...")

# ---------- CHAT ----------

question = ""

if mode == "Chat med dokument":

    question = st.text_input("Ask a question about the document")

# ---------- ANALYSIS ----------

if st.button("Run AI analysis"):

    if text.strip() == "":
        st.warning("No text detected")
    else:

        if mode == "Oppsummer tekst":

            prompt = f"""
Create a clear summary.

Explanation level: {level}

Return:

SUMMARY
KEY POINTS

Text:
{text}
"""

        elif mode == "Organiser notater":

            prompt = f"""
Organize these notes.

Explanation level: {level}

Return:

SUMMARY
KEY POINTS
STRUCTURED NOTES

Text:
{text}
"""

        elif mode == "Forklar tekst":

            prompt = f"""
Explain the text.

Explanation level: {level}

Return:

MAIN IDEA
IMPORTANT CONCEPTS
EXAMPLE

Text:
{text}
"""

        elif mode == "Chat med dokument":

            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )

            conversation = "\n".join(
                [msg["content"] for msg in st.session_state.chat_history]
            )

            prompt = f"""
Use the document to answer the question.

Document:
{text}

Conversation:
{conversation}
"""

        elif mode == "Finn nøkkelinnsikt":

            prompt = f"""
Analyze the document and return:

MAIN IDEA
KEY CONCEPTS
IMPORTANT DATA
CONCLUSION

Text:
{text}
"""

        elif mode == "Lag flashcards":

            prompt = f"""
Create flashcards from the text.

Format:

Question:
Answer:

Text:
{text}
"""

        elif mode == "Lag quiz":

            prompt = f"""
Create a quiz from the text.

5 questions with answers.

Text:
{text}
"""

        with st.spinner("AI analyzing..."):

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

        result = response.output_text

        st.success("Analysis complete")

        # ---------- RESULT SECTIONS ----------

        st.subheader("Result")
        st.write(result)

        st.session_state.history.append(result)

        # ---------- DOWNLOAD ----------

        st.download_button(
            label="Download result",
            data=result,
            file_name="ai_result.txt",
            mime="text/plain"
        )

# ---------- HISTORY ----------

if len(st.session_state.history) > 0:

    st.divider()

    st.subheader("Previous analyses")

    for i, item in enumerate(st.session_state.history[::-1]):

        with st.expander(f"Analysis {i+1}"):

            st.write(item)
