import os
from typing import Dict

from llama_index.core.settings import Settings


def init_settings():
    model_provider = os.getenv("MODEL_PROVIDER")
    match model_provider:
        case "openai":
            init_openai()
        case "groq":
            init_groq()
        case "ollama":
            init_ollama()
        case "anthropic":
            init_anthropic()
        case "gemini":
            init_gemini()
        case "mistral":
            init_mistral()
        case "azure-openai":
            init_azure_openai()
        case "vllm":
            init_vllm()
        case "t-systems":
            from .llmhub import init_llmhub

            init_llmhub()
        case _:
            raise ValueError(f"Invalid model provider: {model_provider}")

    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))

def init_vllm():
    import os
    
    if os.getenv("EMBEDDING_PROVIDER") == "fastembed":
        init_fastembed()
    else:
        # switch to using ollama for embeddings
        from llama_index.embeddings.ollama import OllamaEmbedding
        
        base_url = os.getenv("EMBEDDING_URL") or "http://127.0.0.1:11434"
        Settings.embed_model = OllamaEmbedding(
            base_url=base_url,
            model_name=os.getenv("EMBEDDING_MODEL"),
        )
        
    from llama_index.llms.openai_like import OpenAILike
    
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "api_base": os.getenv("VLLM_URL"),
        "api_key": "fake",
        "temperature": float(os.getenv("LLM_TEMPERATURE", 0)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    
    Settings.llm = OpenAILike(**config)
    print("vllm setting initiated with model: " + os.getenv("MODEL") + " & embedding provider: "+ os.getenv("EMBEDDING_PROVIDER"))

def init_ollama():
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama.base import DEFAULT_REQUEST_TIMEOUT, Ollama

    base_url = os.getenv("EMBEDDING_URL") or "http://127.0.0.1:11434"
    request_timeout = float(
#        os.getenv("OLLAMA_REQUEST_TIMEOUT", DEFAULT_REQUEST_TIMEOUT)
        os.getenv("OLLAMA_REQUEST_TIMEOUT", 180)
    )
    Settings.embed_model = OllamaEmbedding(
        base_url=base_url,
        model_name=os.getenv("EMBEDDING_MODEL"),
    )
    Settings.llm = Ollama(
        base_url=base_url, model=os.getenv("MODEL"), request_timeout=request_timeout
    )


def init_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = OpenAI(**config)

    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = OpenAIEmbedding(**config)


def init_azure_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
    from llama_index.llms.azure_openai import AzureOpenAI

    llm_deployment = os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    llm_config = {
        "api_key": api_key,
        "deployment_name": llm_deployment,
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = AzureOpenAI(**llm_config)

    dimensions = os.getenv("EMBEDDING_DIM")
    embedding_config = {
        "api_key": api_key,
        "deployment_name": embedding_deployment,
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = AzureOpenAIEmbedding(**embedding_config)


def init_fastembed():
    """
    Use Qdrant Fastembed as the local embedding provider.
    """
    from llama_index.embeddings.fastembed import FastEmbedEmbedding

    embed_model_map: Dict[str, str] = {
        # Small and multilingual
        "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
        # Large and multilingual
        "paraphrase-multilingual-mpnet-base-v2": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",   # noqa: E501
        # bge series
        "bge-small-en-v1.5": "BAAI/bge-small-en-v1.5",
        "bge-small-zh-v1.5": "BAAI/bge-small-zh-v1.5",
        "bge-base-en-v1.5": "BAAI/bge-base-en-v1.5",
        "bge-large-en-v1.5": "BAAI/bge-large-en-v1.5",
    }

    # This will download the model automatically if it is not already downloaded
    Settings.embed_model = FastEmbedEmbedding(
        model_name=embed_model_map[os.getenv("EMBEDDING_MODEL")]
    )

def init_groq():
    from llama_index.llms.groq import Groq

    model_map: Dict[str, str] = {
        "llama3-8b": "llama3-8b-8192",
        "llama3-70b": "llama3-70b-8192",
        "mixtral-8x7b": "mixtral-8x7b-32768",
    }


    Settings.llm = Groq(model=model_map[os.getenv("MODEL")])
    # Groq does not provide embeddings, so we use FastEmbed instead
    init_fastembed()


def init_anthropic():
    from llama_index.llms.anthropic import Anthropic

    model_map: Dict[str, str] = {
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
        "claude-2.1": "claude-2.1",
        "claude-instant-1.2": "claude-instant-1.2",
    }

    Settings.llm = Anthropic(model=model_map[os.getenv("MODEL")])
    # Anthropic does not provide embeddings, so we use FastEmbed instead
    init_fastembed()


def init_gemini():
    from llama_index.embeddings.gemini import GeminiEmbedding
    from llama_index.llms.gemini import Gemini

    model_name = f"models/{os.getenv('MODEL')}"
    embed_model_name = f"models/{os.getenv('EMBEDDING_MODEL')}"

    Settings.llm = Gemini(model=model_name)
    Settings.embed_model = GeminiEmbedding(model_name=embed_model_name)


def init_mistral():
    from llama_index.embeddings.mistralai import MistralAIEmbedding
    from llama_index.llms.mistralai import MistralAI

    Settings.llm = MistralAI(model=os.getenv("MODEL"))
    Settings.embed_model = MistralAIEmbedding(model_name=os.getenv("EMBEDDING_MODEL"))
