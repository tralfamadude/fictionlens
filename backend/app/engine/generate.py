import logging 
import os

from llama_index.vector_stores import AstraDBVectorStore
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

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()



def test_astradb():
    dataset = download_llama_dataset(
    "PaulGrahamEssayDataset", "./data"
    )

    documents = SimpleDirectoryReader("./data").load_data()
    print(f"Total documents: {len(documents)}")
    print(f"First document, id: {documents[0].doc_id}")
    print(f"First document, hash: {documents[0].hash}")
    print(
        "First document, text"
        f" ({len(documents[0].text)} characters):\n"
        f"{'=' * 20}\n"
        f"{documents[0].text[:360]} ..."
    )

    astra_db_store = AstraDBVectorStore(
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        collection_name="test_fictionlens",
        embedding_dimension=1536,
    )

    storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    query_engine = index.as_query_engine()
    query_string_1 = "Why did the author choose to work on AI?"
    response = query_engine.query(query_string_1)
    print(f"querystring.....")
    print(query_string_1)
    print(response.response)


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
    # generate_datasource(service_context)
    test_astradb()

