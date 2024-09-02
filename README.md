This is a POC of ChatWSF powered by LlamaIndex with WSF md files

## Preparation

First, please installed related LlamaIndex libraries:
```
pip install llama-index llama-index-llms-ollama llama-index-embeddings-ollama llama-index-llms-openai-like llama-index-embeddings-fastembed chromadb llama-index-vector-stores-chroma
```

Then install Ollama & download llama3 (**Note**: It is not necessary any more if you are using vLLM together with fastembed in backend config)
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

## Getting Started

First, startup the backend as described in the [backend README](./backend/README.md).

Second, run the development server of the frontend as described in the [frontend README](./frontend/README.md).

Open [http://ip:3000](http://ip:3000) with your browser to see the result.

## Learn More

To learn more about LlamaIndex, take a look at the following resources:

- [LlamaIndex Documentation](https://docs.llamaindex.ai) - learn about LlamaIndex (Python features).
- [LlamaIndexTS Documentation](https://ts.llamaindex.ai) - learn about LlamaIndex (Typescript features).

