This is a [LlamaIndex](https://www.llamaindex.ai/) project using [Next.js](https://nextjs.org/).

## Getting Started

Prepare: 
1. Please change ip address in .env file
2. Make sure you have [NodeJS](https://nodejs.org/en/download/package-manager) and npx installed on your machine

First, install the dependencies:

```
npm install
```

Second, run the development server for development (only accessible on localhost):

```
npm run dev
```

Once everything is done, run build and serv for production:
```
npm run build
npx serve@latest out
```

Open [http://ip:3000](http://ip:3000) with your browser to see the result.


## Using Docker

1. Build an image for the Next.js app:

```
docker build -t <your_app_image_name> .
```

2. Start the app:

```
docker run \
  --rm \
  -v $(pwd)/.env:/app/.env \ # Use ENV variables and configuration from your file-system
  -v $(pwd)/config:/app/config \
  -v $(pwd)/cache:/app/cache \ # Use your file system to store gea vector database
  -p 3000:3000 \
  <your_app_image_name>
```

## Learn More

To learn more about LlamaIndex, take a look at the following resources:

- [LlamaIndex Documentation](https://docs.llamaindex.ai) - learn about LlamaIndex (Python features).
- [LlamaIndexTS Documentation](https://ts.llamaindex.ai) - learn about LlamaIndex (Typescript features).
