# 🏥 Clinical Information Retrieval and Summarization App

A **Streamlit-based** application that helps healthcare professionals and researchers **retrieve, summarize, and analyze** clinical information from two main sources:

1. **Clinical Guidelines** (uploaded documents / pre-ingested guidelines)
2. **PubMed Articles** (fetched via PubMed API)

Built using **Groq LLaMA models** for fast summarization & QnA, and **ChromaDB** for semantic search.

---

## 📂 Project Structure

```
clinical_info_app/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── .env                    # API keys, configs
│
├── data/                   # Local storage for ingested docs
│   ├── guidelines/         # Parsed guideline files
│   └── embeddings/         # Saved vector DB
│
├── modules/                # Modular Python scripts
│   ├── ingestion.py        # File/URL ingestion and text extraction
│   ├── vector_store.py     # Create/search embeddings
│   ├── llm_utils.py        # Summarization & QnA functions (Groq LLaMA)
│   ├── pubmed_api.py       # Fetch and parse PubMed articles
│   ├── confidence_score.py # Assign confidence levels
│   └── ui_components.py    # Streamlit UI helper functions
│
└── README.md               # Project documentation
```

---

## ✨ Features

### 1. **Clinical Guideline Retrieval & Summarization**

* Upload PDF or text-based guidelines
* Extract and embed text into **ChromaDB** for semantic search
* Ask **natural language questions** to retrieve relevant passages
* Get concise, **Groq LLaMA-generated summaries** of search results

### 2. **PubMed Literature Search & Summarization**

* Search PubMed by **keywords or medical terms**
* Retrieve abstracts & metadata of top-matching articles
* Summarize multiple articles into a **clear, concise overview**
* Assign a **confidence score** to help gauge relevance

---

## ⚙️ Installation

```bash

# Create virtual environment
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

# Install dependencies
uv pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# Groq API key for LLaMA models
GROQ_API_KEY=your_groq_api_key_here

# ChromaDB storage directory
CHROMA_DIR=data/embeddings
```

---

## 🚀 Usage

Run the Streamlit app:

```bash
uv run streamlit run app.py
```

Then open your browser at:
`http://localhost:8501`

---

## 📸 Demo Screenshots

<img width="940" height="480" alt="image" src="https://github.com/user-attachments/assets/6910b19d-22cf-405d-a26d-5edc23e182d8" />

<img width="940" height="420" alt="image" src="https://github.com/user-attachments/assets/a3996638-1466-42f1-8baa-d05f2b88ec27" />


---

## 🛠️ Tech Stack

* **Frontend/UI**: [Streamlit](https://streamlit.io)
* **LLM**: [Groq LLaMA](https://groq.com)
* **Vector DB**: [ChromaDB](https://www.trychroma.com)
* **Data Source**: PubMed API
* **Language**: Python 3.11+

---

## 🛡️ Disclaimer

This application is for research and educational purposes only and not a substitute for professional medical advice.

---
