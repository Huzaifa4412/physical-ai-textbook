import os
import uuid
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import cohere

load_dotenv()

# ---------- Clients ----------
co = cohere.Client(os.getenv("COHERE_API_KEY"))

qdrant = QdrantClient(
    url=os.getenv("QDRANT_BASE_URL"),
    api_key=os.getenv("QDRANT_API"),
)

COLLECTION = "testing-rag-chatbot"
VECTOR_SIZE = 1024  # Cohere embed-english-v3.0

# ---------- Qdrant Setup ----------
def ensure_collection():
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION not in collections:
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

# ---------- Sitemap Handling ----------
def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    res = requests.get(sitemap_url, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "xml")

    # sitemap index
    if soup.find("sitemapindex"):
        urls = []
        for loc in soup.find_all("loc"):
            urls.extend(fetch_sitemap_urls(loc.text))
        return urls

    # normal sitemap
    return [loc.text for loc in soup.find_all("loc")]

# ---------- HTML Cleaning ----------
def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    return " ".join(soup.stripped_strings)

# ---------- Chunking (safe) ----------
def chunk_text(text: str, size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

# ---------- Embeddings ----------
def embed_chunks(chunks: list[str]):
    res = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document",
    )
    return res.embeddings

# ---------- Storage ----------
def store_chunks(chunks, embeddings, source_url):
    points = []

    for chunk, vector in zip(chunks, embeddings):
        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "text": chunk,
                "source": source_url,
            },
        })

    qdrant.upsert(collection_name=COLLECTION, points=points)

# ---------- Ingestion ----------
def ingest_website(sitemap_url: str):
    ensure_collection()

    urls = fetch_sitemap_urls(sitemap_url)
    print(f"Found {len(urls)} pages")

    for url in urls:
        try:
            html = requests.get(url, timeout=10).text
            text = html_to_text(html)

            if len(text) < 300:
                continue

            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            store_chunks(chunks, embeddings, url)

            print(f"Ingested: {url}")

        except Exception as e:
            print(f"Skipped {url}: {e}")

# ---------- Run ----------
if __name__ == "__main__":
    ingest_website("https://physical-ai-textbook-woad.vercel.app/sitemap.xml")
