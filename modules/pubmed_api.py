import requests
from datetime import datetime

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def _esearch(term: str, retmax: int = 5):
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "sort": "pubdate",
        "retmax": retmax
    }
    r = requests.get(BASE + "esearch.fcgi", params=params, timeout=20)
    r.raise_for_status()
    js = r.json()
    return js.get("esearchresult", {}).get("idlist", [])

def _esummary(id_list):
    ids = ",".join(id_list)
    params = {"db":"pubmed", "id": ids, "retmode":"json"}
    r = requests.get(BASE + "esummary.fcgi", params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("result", {})

def _efetch_abstract(pmid: str):
    params = {"db":"pubmed", "id": pmid, "retmode":"text", "rettype":"abstract"}
    r = requests.get(BASE + "efetch.fcgi", params=params, timeout=20)
    r.raise_for_status()
    return r.text

def fetch_pubmed_papers(topic: str, retmax: int = 5):
    ids = _esearch(topic, retmax=retmax)
    if not ids:
        return []
    meta = _esummary(ids)
    papers = []
    for pmid in ids:
        rec = meta.get(pmid, {})
        title = rec.get("title","")
        journal = rec.get("fulljournalname", rec.get("source",""))
        pubdate = rec.get("pubdate","")
        try:
            abstract = _efetch_abstract(pmid)
        except Exception:
            abstract = ""
        papers.append({
            "pmid": pmid,
            "title": title,
            "journal": journal,
            "pubdate": pubdate,
            "abstract": abstract
        })
    return papers
