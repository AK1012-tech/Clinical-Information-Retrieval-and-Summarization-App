import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from modules.ui_components import header, mode_selector
from modules.ingestion import process_inputs
from modules.vector_store import RAGStore
from modules.llm_utils import answer_with_context, summarize_text_bullets
from modules.pubmed_api import fetch_pubmed_papers
from modules.confidence_score import score_paper



st.set_page_config(page_title="Clinical Info Retrieval & Summarization", layout="wide")

header()

mode = mode_selector()

# Initialize Vector Store
chroma_dir = os.getenv("CHROMA_DIR", "data/embeddings")
rag = RAGStore(persist_dir=chroma_dir)

if mode == "Guideline Search":
    st.subheader("1) Upload guidelines (PDF/DOCX) or provide a URL")
    uploaded_files = st.file_uploader("Upload files", type=["pdf", "docx"], accept_multiple_files=True)
    url_input = st.text_input("Or paste a guideline URL (WHO/CDC/NICE)")
    with st.expander("Advanced"):
        chunk_size = st.slider("Chunk size (approx. words)", 200, 1200, 600, 50)
        top_k = st.slider("Top-K retrieved chunks", 2, 10, 5, 1)

    if st.button("Ingest / Update Index"):
        with st.spinner("Processing and indexing..."):
            n_docs, n_chunks = process_inputs(uploaded_files, url_input, chunk_size=chunk_size)
            st.success(f"Ingested {n_docs} document(s) into {n_chunks} chunks.")

    st.markdown("---")
    st.subheader("Ask a clinical question")
    query = st.text_input("E.g., What are the latest vaccination recommendations for pregnant women?")

    if st.button("Search & Summarize", disabled=(query.strip() == "")):
        with st.spinner("Retrieving and summarizing..."):
            results = rag.search(query, top_k=top_k)
            if not results:
                st.warning("No relevant sections found. Try ingesting content or refining your query.")
            else:
                context_blocks = []
                for i, r in enumerate(results, 1):
                    with st.container(border=True):
                        st.caption(f"Match {i} • Source: {r.get('source','unknown')} • Score: {r.get('score', 0):.3f}")
                        st.write(r.get("text",""))
                    context_blocks.append(r.get("text",""))

                answer = answer_with_context(query, context_blocks)
                st.markdown("### ✅ Answer")
                st.write(answer)

elif mode == "Research Summarizer":
    st.subheader("2) PubMed Research Summarizer")
    topic = st.text_input("Topic (e.g., 'gestational diabetes screening')")
    max_results = st.slider("How many papers?", 1, 20, 5, 1)

    if st.button("Fetch & Summarize", disabled=(topic.strip() == "")):
        with st.spinner("Calling PubMed and summarizing..."):
            papers = fetch_pubmed_papers(topic, retmax=max_results)
            if not papers:
                st.warning("No papers found.")
            else:
                for p in papers:
                    bullets = summarize_text_bullets(p.get("abstract","(No abstract)"))
                    conf = score_paper(p)
                    with st.container(border=True):
                        st.markdown(f"#### {p.get('title','Untitled')}")
                        st.caption(f"{p.get('journal','Unknown')} • {p.get('pubdate','')} • PMID: {p.get('pmid','')}")
                        st.markdown("**Summary**")
                        st.write(bullets)
                        st.markdown(f"**Confidence:** {conf['label']} ({conf['score']}/100)")
                        st.markdown(f"[View on PubMed](https://pubmed.ncbi.nlm.nih.gov/{p.get('pmid','')}/)")

else:
    st.info("Select a mode from the sidebar.")


# Run the app
# .venv/Scripts/Activate.ps1
# uv run streamlit run app.py