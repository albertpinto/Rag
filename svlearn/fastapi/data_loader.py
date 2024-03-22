import os
from llama_index.core import SimpleDirectoryReader

class DataLoader:
    def __init__(self, directory="/home/apinto/Documents/transcripts-2024/transcripts"):
        self.directory = directory

    def load_documents(self, directory=None):
        if directory:
            self.directory = directory
            
        if not os.path.exists(self.directory):
            raise Exception("Directory does not exist")
        documents = SimpleDirectoryReader(self.directory).load_data()
        return documents

        


