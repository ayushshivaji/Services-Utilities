from dotenv import load_dotenv
from agno.agent import Agent
from agno.agent import AgentKnowledge
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.website import WebsiteTools
from agno.knowledge.json import JSONKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.vectordb.mongodb import MongoDb
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.csv import CSVKnowledgeBase
from agno.embedder.ollama import OllamaEmbedder
from pathlib import Path

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

password = "b6SEBY9cxKq5qhh"
mdb_connection_string = "mongodb+srv://mongodb:b6SEBY9cxKq5qhh@cluster0.hcrgp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


load_dotenv()

knowledge_base = TextKnowledgeBase(
    path=Path("./data"),
    vector_db = PgVector(
        table_name="text_documents",
        db_url=db_url,
        embedder=OllamaEmbedder(id="openhermes"),
    ),
)

knowledge_base.load(recreate=False, upsert=True)

embeddings = OllamaEmbedder(id="openhermes").get_embedding("user name is ayush")

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:5]}")
print(f"Dimensions: {len(embeddings)}")
