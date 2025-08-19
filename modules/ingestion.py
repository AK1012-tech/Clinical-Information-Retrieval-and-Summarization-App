import os
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
import io
import time
import requests
import pdfplumber
from bs4 import BeautifulSoup
from docx import Document
import streamlit as st

from .vector_store import RAGStore
from .llm_utils import simple_text_clean

def _read_pdf(file_bytes: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text.append(t)
    return "\n".join(text)

def _read_docx(file_bytes: bytes) -> str:
    f = io.BytesIO(file_bytes)
    doc = Document(f)
    return "\n".join([p.text for p in doc.paragraphs])

def _read_url(url: str) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Remove script/style
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text("\n")
    return text

from langchain_text_splitters import RecursiveCharacterTextSplitter

def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 80):
    """
    Use RecursiveCharacterTextSplitter to create chunks.
    Splits on paragraphs -> sentences -> words for cleaner context.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(text)
    return chunks

def process_inputs(uploaded_files, url_input: str, chunk_size: int = 600):
    rag = RAGStore()
    n_docs = 0
    n_chunks_total = 0

    if uploaded_files:
        for f in uploaded_files:
            name = f.name
            bytes_data = f.read()
            if name.lower().endswith(".pdf"):
                raw = _read_pdf(bytes_data)
            elif name.lower().endswith(".docx"):
                raw = _read_docx(bytes_data)
            else:
                continue
            raw = simple_text_clean(raw)
            chunks = _chunk_text(raw, chunk_size=chunk_size)
            rag.add_documents(chunks, metadoc={"source": name})
            n_docs += 1
            n_chunks_total += len(chunks)

    if url_input and url_input.strip():
        try:
            raw = _read_url(url_input.strip())
            raw = simple_text_clean(raw)
            chunks = _chunk_text(raw, chunk_size=chunk_size)
            rag.add_documents(chunks, metadoc={"source": url_input.strip()})
            n_docs += 1
            n_chunks_total += len(chunks)
        except Exception as e:
            st.error(f"Failed to fetch URL: {e}")

    return n_docs, n_chunks_total
