import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Agent:
    def __init__(self):
        self.directory = "/home/apinto/Documents"
        self.openapikey = os.getenv("OPENAI_API_KEY")
        print(self.openapikey)
        self.storage_directory = "/home/apinto/Documents/storage"
        self.llm = "none"
        self.index = None
        self.storage_context = None

    def load_documents(self):
        if not os.path.exists(self.directory):
            raise Exception("Directory does not exist")
        documents = SimpleDirectoryReader(self.directory).load_data()
        return documents
    
    def create_index(self, documents):
        self.index = VectorStoreIndex.from_documents(documents)
        return self.index
    
    def persist_index(self, index):
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)
        # Always persist the new index
        index.storage_context = StorageContext.from_defaults(persist_dir=self.storage_directory)
        index.storage_context.persist()

    def load_or_create_index(self):
        if os.path.exists(self.storage_directory):
            self.storage_context = StorageContext.from_defaults(persist_dir=self.storage_directory)
            self.index = load_index_from_storage(self.storage_context)
        else:
            documents = self.load_documents()
            self.create_index(documents)
            self.persist_index(self.index)

    def query_index(self, query):
        query_engine = self.index.as_query_engine()
        return query_engine.query(query)
    
    def critique_query(self, query):
        query_engine = self.index.as_query_engine(llm=Ollama(model="mistral", request_timeout=60.0))
        critique_query = "Check if this is correct give me a yes or no answer " + query
        return query_engine.query(critique_query)
    
@app.get("/prompt/{prompt}")
async def main(prompt: str):
    agent = Agent()
    agent.load_or_create_index()
    response = agent.query_index(prompt)

    print(response)
    critique = agent.critique_query(str(response))
    print(critique)
    full_response = str(response)+ " Critique of agent's response: " + str(critique)
    return full_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)
