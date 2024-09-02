import os
import logging
from datetime import timedelta

from cachetools import cached, TTLCache
from llama_index.core.storage import StorageContext
from llama_index.core.indices import load_index_from_storage

logger = logging.getLogger("uvicorn")


@cached(
    TTLCache(maxsize=50, ttl=timedelta(minutes=5).total_seconds()),
    key=lambda *args, **kwargs: "global_storage_context",
)
def get_storage_context(persist_dir: str) -> StorageContext:
    return StorageContext.from_defaults(persist_dir=persist_dir)


def get_index():
    storage_dir = os.getenv("STORAGE_DIR", "storage")
    
    # check if storage already exists
    if not os.path.exists(storage_dir):
        return None

    # load the existing index
    logger.info(f"Loading index from {storage_dir}...")
    
    match storage_dir:
        case "storage":
            storage_context = get_storage_context(storage_dir)
            index = load_index_from_storage(storage_context)
        case "chromadb":
            import chromadb
            from chromadb.config import Settings
            from llama_index.core import VectorStoreIndex
            from llama_index.vector_stores.chroma import ChromaVectorStore
            from llama_index.core import StorageContext

            # initialize client
            db = chromadb.PersistentClient(path="./chromadb", settings=Settings(anonymized_telemetry=False))

            # get collection
            chroma_collection = db.get_or_create_collection("wsf")

            # assign chroma as the vector_store to the context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # load your index from stored vectors
            index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )      
        case _:
            raise ValueError(f"Invalid storage dir: {storage_dir}")    

    logger.info(f"Finished loading index from {storage_dir}")
    return index
