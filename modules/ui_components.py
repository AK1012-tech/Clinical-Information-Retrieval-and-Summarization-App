import streamlit as st

def header():
    st.title("🩺 Clinical Information Retrieval & Summarization")
    st.caption("Find answers fast from trusted sources. Built with Streamlit + ChromaDB + Groq (LLaMA).")

def mode_selector():
    st.sidebar.header("Mode")
    return st.sidebar.radio("Choose function:", ["Guideline Search", "Research Summarizer"], index=0)
