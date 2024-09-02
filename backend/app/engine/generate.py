from dotenv import load_dotenv

load_dotenv()

import os
import logging
from llama_index.core.indices import (
    VectorStoreIndex,
)
from app.engine.loaders import get_documents
from app.settings import init_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from llama_index.core.node_parser import SentenceSplitter

def generate_datasource():
    init_settings()
    logger.info("Creating new index")
    storage_dir = os.environ.get("STORAGE_DIR", "storage")
        
    match storage_dir:
        case "storage":
            init_local_storage()
        case "chromadb":
            init_chromadb()
        case _:
            raise ValueError(f"Invalid storage dir: {storage_dir}")    

def init_local_storage():    
    # load the documents and create the index
    documents = get_documents()
    # Set private=false to mark the document as public (required for filtering)
    for doc in documents:
        doc.metadata["private"] = "false"
    index = VectorStoreIndex.from_documents(
        documents, 
    )
    # store it for later
    index.storage_context.persist("storage")
    logger.info(f"Finished creating new index. Stored in local folder 'storage'")


def init_chromadb():    
    # load the documents and create the index
    documents = get_documents()
    # Set private=false to mark the document as public (required for filtering)
    for doc in documents:
        doc.metadata["private"] = "false"

    import chromadb
    from chromadb.config import Settings
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from llama_index.core import StorageContext

    # initialize client, setting path to save data
    db = chromadb.PersistentClient(path="./chromadb", settings=Settings(anonymized_telemetry=False))

    # create collection
    chroma_collection = db.get_or_create_collection("wsf")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    logger.info(f"Finished creating new index. Stored in chromadb")
    
    
if __name__ == "__main__":
    generate_datasource()
