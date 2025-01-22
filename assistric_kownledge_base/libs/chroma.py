from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_core.documents.base import Document
import os
import chromadb


load_dotenv()

class ChromaClient:
    chromaDb: Chroma

    def __init__(self):
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
        CHROMADB_URL = os.getenv("CHROMA_DB_URL")
        CHROMADB_USERNAME = os.getenv("CHROMA_DB_USERNAME")
        CHROMADB_PASSWORD = os.getenv("CHROMA_DB_PASSWORD")

        settings = Settings(
            chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
            chroma_client_auth_credentials=f"{CHROMADB_USERNAME}:{CHROMADB_PASSWORD}",
        )

        # get host from CHROMADB_URL
        host = CHROMADB_URL.split("//")[1].split(":")[0]
        port = int(CHROMADB_URL.split(":")[2])
        client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=settings
        )

        self.chromaDb = Chroma(
            collection_name="knowledge_base",
            client=client,
            embedding_function=embeddings,
        )
    
    def add_documents(self, documents: list[Document]) -> None:
        self.chromaDb.add_documents(documents)