# agent.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.ollama import Ollama
import index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Agent:
    def __init__(self, directory: str, storage_directory: str, agent_type: str):
        self.directory = directory
        self.storage_directory = storage_directory
        self.agent_type = agent_type
        self.index = index.Index(directory, storage_directory).load_index()
        if self.index is None:
            raise ValueError("Failed to load or create the index.")

    def query(self, query: str) -> str:
        if self.index is None:
            raise HTTPException(status_code=500, detail="Index is not loaded.")
        if self.agent_type == "regular":
            query_engine = self.index.as_query_engine()
            #query_engine = self.index.as_query_engine(llm=Ollama(model="llama2", request_timeout=60.0))
        elif self.agent_type == "critique":
            query = "Check if this is correct: " + query
            query_engine = self.index.as_query_engine(llm=Ollama(model="mistral", request_timeout=60.0))
        else:
            raise ValueError(f"Unknown agent type: {self.agent_type}")
        return query_engine.query(query)

@app.get("/prompt/{prompt}")
async def main(prompt: str) -> str:
    try:
        directory = os.getenv("DIRECTORY", "/home/apinto/Documents/transcripts-2024/transcripts")
        storage_directory = os.getenv("STORAGE_DIRECTORY", "/home/apinto/Documents/storage")
        
        # Configure and query the primary agent
        primary_agent = Agent(directory, storage_directory, "regular")
        response = primary_agent.query(prompt)
        
        # Configure and query the critique agent
        critique_agent = Agent(directory, storage_directory, "critique")
        critique = critique_agent.query(prompt)
        
        full_response = f"{response} Critique agent's response: {critique}"
        return full_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)
