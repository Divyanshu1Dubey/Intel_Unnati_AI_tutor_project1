import streamlit as st
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
from tempfile import NamedTemporaryFile

# ----------- UI Setup -----------
st.set_page_config(page_title="PDF Query AI", page_icon="📚", layout="wide")
st.title("📚 Ask Your PDF")
st.markdown("Upload a PDF, ask questions, and get intelligent answers using state-of-the-art NLP models.")

# ----------- Load Model Resources -----------
@st.cache_resource
def load_models():
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return encoder, reranker, qa

@st.cache_resource
def load_index():
    with open("pdf_index.pkl", "rb") as f:
        index, embeddings, chunks = pickle.load(f)
    return index, embeddings, chunks

# ----------- Query Function -----------
def retrieve(query, index, chunks, encoder, reranker, k=10):
    query_emb = encoder.encode([query])
    _, I = index.search(query_emb, k)
    retrieved = [chunks[i] for i in I[0]]
    pairs = [[query, passage] for passage in retrieved]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(retrieved, scores), key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked[:5]]

def generate_answer(query, retrieved_text, qa_pipeline):
    best_answer = None
    best_score = 0
    for context in retrieved_text:
        try:
            result = qa_pipeline(question=query, context=context)
            if result['score'] > best_score:
                best_score = result['score']
                best_answer = result['answer']
        except:
            continue
    return best_answer if best_answer else "❌ No relevant answer found."

# ----------- Upload & Process PDF -----------
uploaded_file = st.file_uploader("📄 Upload your PDF file", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully.")
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    st.info("⚙️ Indexing the PDF... please wait.")
    os.system(f"python index_pdf.py {temp_pdf_path}")

    if os.path.exists("pdf_index.pkl"):
        index, embeddings, chunks = load_index()
        encoder, reranker, qa_pipeline = load_models()

        # ----------- Ask Query -----------
        st.subheader("🔍 Ask something about your PDF")
        query = st.text_input("Enter your question:")
        if st.button("Search") and query:
            with st.spinner("🔎 Searching for the best answer..."):
                retrieved_text = retrieve(query, index, chunks, encoder, reranker)
                answer = generate_answer(query, retrieved_text, qa_pipeline)
                st.success("✅ Answer found!")
                st.markdown(f"### 💡 **Answer:** {answer}")

                with st.expander("📄 View Retrieved Contexts"):
                    for i, passage in enumerate(retrieved_text, 1):
                        st.markdown(f"**Context {i}:** {passage}")
        elif query == "":
            st.warning("Please enter a query.")

    else:
        st.error("Failed to index the PDF. Please check your PDF or try again.")
