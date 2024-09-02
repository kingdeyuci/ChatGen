This is a [LlamaIndex](https://www.llamaindex.ai/) project using [FastAPI](https://fastapi.tiangolo.com/).

## Getting Started

First, setup the environment with python3.11 and poetry. After that, 

```
poetry install
```

Then create the parameters in `.env` as pre-configured settings in this directory. (You can take .env-template as reference).
```
cp .env-template .env
```

If you are using any tools or data sources, you can update their config files in the `config` folder.

Second, generate the embeddings of the documents in the `./data` directory (Currently, most of WSF *.md files are in this folder. You can remove most of them and just keep a small set for better experiment experience):

```
poetry run generate
```
Note: Check your no_proxy setting in case any connection error happens.

Third, run the development server:

```
python main.py
```

The example provides two different API endpoints:

1. `/api/chat` - a streaming chat endpoint
2. `/api/chat/request` - a non-streaming chat endpoint

You can test the streaming endpoint with the following curl request:

```
curl --location 'localhost:8000/api/chat' \
--header 'Content-Type: application/json' \
--data '{ "messages": [{ "role": "user", "content": "Hello" }] }'
```

And for the non-streaming endpoint run:

```
curl --location 'localhost:8000/api/chat/request' \
--header 'Content-Type: application/json' \
--data '{ "messages": [{ "role": "user", "content": "Hello" }] }'
```

You can start editing the API endpoints by modifying `app/api/routers/chat.py`. The endpoints auto-update as you save the file. You can delete the endpoint you're not using.

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the Swagger UI of the API.

The API allows CORS for all origins to simplify development. You can change this behavior by setting the `ENVIRONMENT` environment variable to `prod`:

```
ENVIRONMENT=prod python main.py
```

## Using Docker

1. Build an image for the FastAPI app:

```
docker build -t <your_backend_image_name> .
```

2. Generate embeddings:

Parse the data and generate the vector embeddings if the `./data` folder exists - otherwise, skip this step:

```
docker run \
  --rm \
  -v $(pwd)/.env:/app/.env \ # Use ENV variables and configuration from your file-system
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \ # Use your local folder to read the data
  -v $(pwd)/storage:/app/storage \ # Use your file system to store the vector database
  <your_backend_image_name> \
  poetry run generate
```

3. Start the API:

```
docker run \
  -v $(pwd)/.env:/app/.env \ # Use ENV variables and configuration from your file-system
  -v $(pwd)/config:/app/config \
  -v $(pwd)/storage:/app/storage \ # Use your file system to store gea vector database
  -p 8000:8000 \
  <your_backend_image_name>
```


