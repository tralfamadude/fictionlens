import logging
import os
from llama_index.vector_stores import AstraDBVectorStore
# from astrapy.db import AstraDB

# from llamadb.indexing import LlamaIndex

query_index = None  

def save_query_index(index):
    global query_index 
    logger = logging.getLogger("uvicorn")
    logger.info(f"Saving query_index...")
    logger.info(f"query_index to save: {index}")
    query_index = index

def get_query_engine(query):
    return query_index
    # ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
    # ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")

    # client = AstraDBOps(
    #     token="ASTRA_DB_APPLICATION_TOKEN",
    #     endpoint="ASTRA_DB_API_ENDPOINT")

    # index = LlamaIndex(client)
    # collection_name = "test_fictionlens"

    # results = index.query(collection_name, query)

    # for document in results:
    #     print(document)

# def get_query_engine():
#     logger = logging.getLogger("uvicorn")

#     ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
#     ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")

#     # Initialize the AstraDB client and collection
#     db = AstraDB(token="ASTRA_DB_APPLICATION_TOKEN", api_endpoint="ASTRA_DB_API_ENDPOINT")
#     collection = db.collection(collection_name="test_fictionlens")

#     # Retrieve the first document with a product_price
#     results = collection.find({"product_price": {"$exists": True}})
#     for document in results["data"]["documents"]:
#         print(document)

#     # Retrieve the first document where the product_price is 12.99
#     results = collection.find({"product_price": 12.99})
#     for document in results["data"]["documents"]:
#         print(document)

#     # Retrieve the first document where product_price is 9.99
#     # and product_name is "HealthyFresh - Chicken raw dog food"
#     results = collection.find({
#         "product_name": "HealthyFresh - Chicken raw dog food",
#         "product_price": 9.99
#     })
#     for document in results["data"]["documents"]:
#      print(document)


#     # logger.info(f"AstraDBVectorStore: {astra_db_store}")

#     # logger.info(f"AstraDBVectorStore info: {astra_db_store}")

    
#     # logger.info(f"Extracting query_index...")
#     # logger.info(f"query_index: {query_index}")
#     return query_index
    
