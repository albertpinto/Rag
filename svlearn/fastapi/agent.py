# agent.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
import index

app = FastAPI()
# Delete me later

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This is test
class Agent:
    def __init__(self, directory: str, storage_directory: str, agent_type: str):
        self.directory = directory
        self.storage_directory = storage_directory
        self.agent_type = agent_type
        self.index = index.Index(directory, storage_directory).load_index()
        if self.index is None:
            raise ValueError("Failed to load or create the index.")

    def query(self, query: str) -> str:
         
        # PromptTemplate ="""
        # # CONTEXT #
        #     You are a chatbot that provides answers only to question{query} from the context of the index.
        # # END CONTEXT #
        # # OBJECTIVE #
        #    You will answer the user's question based on the content of the index.
        # # END OBJECTIVE #
        # #STYLE#
        #     Like a question and answer session.
        # # END STYLE #
        # # TONE #
        #     Formal, Should be strictly based on the content.
        # # END TONE #
        # # AUDIENCE #
        #     The audience is a group of AI enthusiasts.
        # # END AUDIENCE #
        # #RESPONSE #
        #     Return the response to the user's question.
        #    Answer:
        # # END RESPONSE #    
        # """     
        # print (PromptTemplate)
        if self.index is None:
            raise HTTPException(status_code=500, detail="Index is not loaded.")
        if self.agent_type == "regular":
            #chat_engine = self.index.as_chat_engine()
            chat_engine = self.index.as_chat_engine(llm=Ollama(model="llama3", request_timeout=60.0))
        elif self.agent_type == "critique":
            query = "Check if this is correct: " + query
            chat_engine = self.index.as_chat_engine()
            #chat_engine = self.index.as_chat_engine(llm=Ollama(model="llama3", request_timeout=60.0))
        else:
            raise ValueError(f"Unknown agent type: {self.agent_type}")
        return chat_engine.query(query)



# test 
@app.get("/prompt/{prompt}")
async def main(prompt: str) -> str:
    try:
        directory = os.getenv("LECTURE_TRANSCRIPT_DIRECTORY")
        storage_directory = os.getenv("INDEX_STORAGE_DIRECTORY")
        
        # Configure and query the primary agent
        primary_agent = Agent(directory, storage_directory, "regular")
        response = primary_agent.query(prompt)
        
        print(f"Primary agent's response: {response.response}")
        
        primary_agent_response = response.response
        
        # Configure and query the critique agent
        critique_agent = Agent(directory, storage_directory, "critique")
        
        # Add the primary agent's response to the critique agent's query to get a critique
        critique = critique_agent.query(primary_agent_response)
        
        critique_response = critique.response
        print(f"Critique agent's response: {critique_response}")
        
        full_response = f"{primary_agent_response} Critique agent's response: {critique.response}"
        return full_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)
