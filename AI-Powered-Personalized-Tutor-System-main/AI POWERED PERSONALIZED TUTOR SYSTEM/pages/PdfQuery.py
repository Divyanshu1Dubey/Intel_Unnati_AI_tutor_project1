import streamlit as st
import os
import pickle
from tempfile import NamedTemporaryFile
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
import faiss
import glob
from PyPDF2 import PdfReader
import hashlib

# ----------- CONFIG -----------
st.set_page_config(page_title="Smart PDF QA", page_icon="🧠", layout="wide")
st.title("🧠 Intelligent PDF Assistant")
st.markdown("Upload one or more PDFs and ask deep questions. Powered by cutting-edge NLP.")


# ----------- MODEL LOADING -----------
@st.cache_resource
def load_models():
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return encoder, reranker, qa


encoder, reranker, qa_pipeline = load_models()


# ----------- HELPERS -----------
def clean_filename(name):
    return hashlib.md5(name.encode()).hexdigest()[:12]


def save_index(filename, index, embeddings, chunks):
    with open(f"indices/{filename}.pkl", "wb") as f:
        pickle.dump((index, embeddings, chunks), f)


def load_index(filename):
    with open(f"indices/{filename}.pkl", "rb") as f:
        return pickle.load(f)


def index_pdf(file_path):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or '' for page in reader.pages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = encoder.encode(chunks, show_progress_bar=True)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings, chunks


def retrieve(query, index, chunks, encoder, reranker, k=10):
    query_emb = encoder.encode([query])
    _, I = index.search(query_emb, k)
    retrieved = [chunks[i] for i in I[0]]
    pairs = [[query, passage] for passage in retrieved]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(retrieved, scores), key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked[:5]]


def generate_answer(query, contexts):
    best_answer = None
    best_score = 0
    best_context = None
    for context in contexts:
        try:
            result = qa_pipeline(question=query, context=context)
            if result['score'] > best_score:
                best_score = result['score']
                best_answer = result['answer']
                best_context = context
        except:
            continue
    return best_answer, best_context


# ----------- UI SECTION: PDF Upload and Selection -----------
os.makedirs("indices", exist_ok=True)
uploaded_files = st.file_uploader("📄 Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

pdf_map = {}
for uploaded_file in uploaded_files:
    st.toast(f"📥 Processing {uploaded_file.name}")
    filename = clean_filename(uploaded_file.name)
    file_path = f"temp_{filename}.pdf"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if not os.path.exists(f"indices/{filename}.pkl"):
        st.info(f"🔎 Indexing {uploaded_file.name}...")
        index, embeddings, chunks = index_pdf(file_path)
        save_index(filename, index, embeddings, chunks)
    pdf_map[uploaded_file.name] = filename

if pdf_map:
    st.success("✅ All PDFs indexed.")
    selected_pdf = st.selectbox("📑 Choose a PDF to query:", list(pdf_map.keys()))
    if selected_pdf:
        index, embeddings, chunks = load_index(pdf_map[selected_pdf])

        # ----------- UI SECTION: Ask Queries -----------
        st.subheader("💬 Ask a question about the PDF")
        query = st.text_input("Type your question here:")
        if st.button("🔍 Get Answer") and query:
            with st.spinner("Thinking..."):
                retrieved = retrieve(query, index, chunks, encoder, reranker)
                answer, context = generate_answer(query, retrieved)
                if answer:
                    st.markdown(f"### ✅ **Answer:** `{answer}`")
                    st.markdown("#### 📖 Context Highlighted:")
                    highlighted = context.replace(answer, f"**:blue[{answer}]**")
                    st.markdown(highlighted)
                else:
                    st.warning("❌ Sorry, I couldn't find an exact answer. Try rephrasing!")

                with st.expander("📄 Show All Retrieved Contexts"):
                    for i, passage in enumerate(retrieved, 1):
                        st.markdown(f"**Context {i}:** {passage}")

# ----------- OPTIONAL FEATURE: Summarizer -----------
st.divider()
st.subheader("📝 Want a quick summary?")
if st.button("📃 Generate PDF Summary") and uploaded_files:
    for file in uploaded_files:
        reader = PdfReader(file)
        full_text = "\n".join([page.extract_text() or '' for page in reader.pages])
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(full_text[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        st.markdown(f"### Summary of **{file.name}**")
        st.info(summary)

st.sidebar.title("⚙️ Models Used")
st.sidebar.markdown("- SentenceTransformer: `all-MiniLM-L6-v2`")
st.sidebar.markdown("- Reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2`")
st.sidebar.markdown("- QA: `deepset/roberta-base-squad2`")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ for the **AI-Powered Personalized Tutor System**.")
