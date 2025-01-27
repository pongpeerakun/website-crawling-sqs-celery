from assistric_kownledge_base.crawler import crawl_target_website
from assistric_kownledge_base.scraper import scrape_target_website
import asyncio
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from chromadb.config import Settings
import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai import CrawlerRunConfig
import chromadb
import json
from pymongo import MongoClient


load_dotenv()

async def main():
    CHROMADB_URL = os.getenv("CHROMA_DB_URL")
    CHROMADB_USERNAME = os.getenv("CHROMA_DB_USERNAME")
    CHROMADB_PASSWORD = os.getenv("CHROMA_DB_PASSWORD")
    settings = Settings(
        chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
        chroma_client_auth_credentials=f"{CHROMADB_USERNAME}:{CHROMADB_PASSWORD}",
    )
    host = CHROMADB_URL.split("//")[1].split(":")[0]
    port = int(CHROMADB_URL.split(":")[2])
    client = chromadb.HttpClient(
        host=host,
        port=port,
        settings=settings
    )

    client.heartbeat()

if __name__ == "__main__":
    asyncio.run(main())
