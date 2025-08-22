"""
Streamlit-compatible Vector Database
A simplified vector database that works well with Streamlit Cloud
"""

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

class StreamlitVectorDB:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2", persist_directory="./vector_db"):
        self.embedding_model_name = embedding_model_name
        self.persist_directory = persist_directory
        self.model = None
        self.documents = []
        self.embeddings = []
        self.metadata = []
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
    def _load_model(self):
        """Load the embedding model"""
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.embedding_model_name)
            except Exception as e:
                st.error(f"Error loading embedding model: {e}")
                raise e
    
    def add_documents(self, texts, metadatas=None):
        """Add documents to the vector database"""
        self._load_model()
        
        if metadatas is None:
            metadatas = [{"id": i} for i in range(len(texts))]
        
        # Generate embeddings
        with st.spinner("Generating embeddings..."):
            new_embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add to storage
        self.documents.extend(texts)
        self.embeddings.extend(new_embeddings.tolist())
        self.metadata.extend(metadatas)
        
        # Persist to disk
        self._persist()
        
        return True
    
    def similarity_search(self, query, k=5):
        """Search for similar documents"""
        if not self.documents:
            self._load_from_disk()
        
        if not self.documents:
            return []
        
        self._load_model()
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        if self.embeddings:
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get top k results
            top_indices = np.argsort(similarities)[::-1][:k]
            
            results = []
            for idx in top_indices:
                results.append({
                    'content': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'similarity_score': float(similarities[idx])
                })
            
            return results
        
        return []
    
    def _persist(self):
        """Save the database to disk"""
        try:
            data = {
                'documents': self.documents,
                'embeddings': self.embeddings,
                'metadata': self.metadata,
                'embedding_model': self.embedding_model_name
            }
            
            with open(os.path.join(self.persist_directory, 'vectordb.pkl'), 'wb') as f:
                pickle.dump(data, f)
                
        except Exception as e:
            st.warning(f"Could not persist database: {e}")
    
    def _load_from_disk(self):
        """Load the database from disk"""
        try:
            db_file = os.path.join(self.persist_directory, 'vectordb.pkl')
            if os.path.exists(db_file):
                with open(db_file, 'rb') as f:
                    data = pickle.load(f)
                
                self.documents = data.get('documents', [])
                self.embeddings = data.get('embeddings', [])
                self.metadata = data.get('metadata', [])
                
                return True
        except Exception as e:
            st.warning(f"Could not load database: {e}")
            
        return False
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.documents = []
        self.embeddings = []
        self.metadata = []
        
        # Remove persistence file
        try:
            db_file = os.path.join(self.persist_directory, 'vectordb.pkl')
            if os.path.exists(db_file):
                os.remove(db_file)
        except Exception as e:
            st.warning(f"Could not delete database file: {e}")
        
        return True
    
    def get_document_count(self):
        """Get the number of documents in the database"""
        if not self.documents:
            self._load_from_disk()
        return len(self.documents)
