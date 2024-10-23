import logging 
import os

from weaviate import Client as WeaviateClient
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.llama_dataset import download_llama_dataset
from dotenv import load_dotenv

from app.engine.constants import DATA_DIR, STORAGE_DIR
from app.engine.context import create_service_context
from app.engine.loader import get_documents
from app.engine.query_engine import save_query_index

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()



def test_astradb(query_string_1):
    dataset = download_llama_dataset(
    "PaulGrahamEssayDataset", "./data"
    )

    documents = SimpleDirectoryReader("./data3").load_data()
    print(f"Total documents: {len(documents)}")
    print(f"First document, id: {documents[0].doc_id}")
    print(f"First document, hash: {documents[0].hash}")
    print(
        "First document, text"
        f" ({len(documents[0].text)} characters):\n"
        f"{'=' * 20}\n"
        f"{documents[0].text[:360]} ..."
    )


    #  # only top 20 list
    # astra_db_store = AstraDBVectorStore(
    #     token=ASTRA_DB_APPLICATION_TOKEN,
    #     api_endpoint=ASTRA_DB_API_ENDPOINT,
    #     collection_name="fictionlens_prod_3",
    #     embedding_dimension=1536,
    # )

    client = WeaviateClient("http://localhost:8080")
    # Example logic for Weaviate
    # Add your data generation logic here using the Weaviate client


def generate_datasource(service_context):
    logger.info("Creating new index")
    # load the documents and create the index
    documents = get_documents()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    # store it for later
    index.storage_context.persist(STORAGE_DIR)
    logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")


if __name__ == "__main__":
    service_context = create_service_context()
    generate_datasource(service_context)
    test_astradb("Why did the author choose to work on AI?")

