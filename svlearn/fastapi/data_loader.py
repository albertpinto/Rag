import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from fastapi.middleware.cors import CORSMiddleware
# from qdrant_client import QdrantClient
# from llama_index.vector_stores.qdrant import QdrantVectorStore

# pip install -U qdrant-client
# pip install llama-index-vector-stores-qdrant
from fastapi import FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class DocumentReader:
    def __init__(self):
        self.directory = (
            "/Users/albertpinto/documents/transcripts"  # Change the directory as needed
        )
        self.openapikey = os.environ.get("OPENAI_API_KEY")
        self.storage_directory = (
            "/Users/albertpinto/documents/storage"  # Change the directory as needed
        )
        self.index = None
        self.storage_context = None
        self.client = None

    def load_documents(self):
        # Create an instance of SimpleDirectoryReader
        if not os.path.exists(self.directory):
            raise Exception("Directory does not exist")
        documents = SimpleDirectoryReader(self.directory).load_data()
        return documents

    def create_index(self, documents):
        # Create an instance of VectorStoreIndex
        self.index = VectorStoreIndex.from_documents(documents)
        return self.index

    def perist_index(self, index, client=None):
        # Persist the index
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

            index.storage_context.persist(persist_dir=self.storage_directory)

        else:
            # load the existing index
            self.storage_context = StorageContext.from_defaults(
                persist_dir=self.storage_directory
            )
            self.index = load_index_from_storage(self.storage_context)

    def query_index(self, query):
        # Query the index
        query_engine = self.index.as_query_engine()
        return query_engine.query(query)

    def print_class(self):
        print(self.directory)
        print(self.openapikey)
        print(self.storage_directory)
        # print(self.index)
        print(self.storage_context)

@app.get("/prompt/{prompt}")
async def main(prompt: str = None):
    # Create an instance of DocumentReader
    reader = DocumentReader()
   
    if not os.path.exists(reader.storage_directory):
        documents = reader.load_documents()
        # Call the create_index method
        index = reader.create_index(documents)
        # Call the perist_index method
        reader.perist_index(index)    
    else:
        reader.storage_context = StorageContext.from_defaults(
            persist_dir=reader.storage_directory
        )
        reader.index = load_index_from_storage(reader.storage_context)
    # Call the query_index method
    reponse = reader.query_index(prompt)
    return(reponse)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9002)


""" if __name__ == "__main__":
    main() """
