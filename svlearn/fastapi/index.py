# index.py
import os
from typing import List, Optional
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import data_loader

class Index:
    def __init__(self, directory: str = os.getenv("LECTURE_TRANSCRIPT_DIRECTORY")
                 ,storage_directory: str = os.getenv("INDEX_STORAGE_DIRECTORY")) -> None:
        self.directory = directory
        self.storage_directory = storage_directory
        self.index = None

    def create_index(self, documents: List[str]) -> VectorStoreIndex:
        """Creates an index from the provided documents."""
        index = VectorStoreIndex.from_documents(documents)
        return index
    
    def persist_index(self, index: VectorStoreIndex) -> None:
        """Persists the provided index to the storage directory."""
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)
        index.storage_context.persist(persist_dir=self.storage_directory)

    def load_index(self) -> Optional[VectorStoreIndex]:
        """Loads the index from storage, or creates a new one if necessary."""
        try:
            if os.path.exists(self.storage_directory):
                storage_context = StorageContext.from_defaults(persist_dir=self.storage_directory)
                self.index = load_index_from_storage(storage_context)
            else:
                documents = data_loader.DataLoader().load_documents(self.directory)
                self.index = self.create_index(documents)
                self.persist_index(self.index)
            return self.index
        except Exception as e:
            print(f"Error loading or creating the index: {e}")
            return None
