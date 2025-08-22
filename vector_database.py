"""
Vector Database Module for KPI GPT RAG System
Created by: Famim Farhaz

This module handles vector database operations using ChromaDB
for storing and retrieving document embeddings.
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDatabase:
    """Manages vector database operations for KPI GPT RAG system"""
    
    def __init__(self, db_path: str = "./vector_db", collection_name: str = "kpi_documents", 
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        
        # Initialize ChromaDB
        self._initialize_db()
        
        # Initialize embedding model with optimization
        logger.info(f"Loading embedding model: {embedding_model}")
        try:
            # Try to use cached model first
            self.embedding_model = SentenceTransformer(
                embedding_model,
                cache_folder=os.path.join(self.db_path, "model_cache"),
                device='cpu'  # Force CPU to avoid CUDA issues on some platforms
            )
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load model with cache, trying default: {e}")
            self.embedding_model = SentenceTransformer(embedding_model)
            logger.info("Embedding model loaded successfully (fallback)")
        
    def _initialize_db(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create directory if it doesn't exist
            Path(self.db_path).mkdir(parents=True, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(self.collection_name)
                logger.info(f"Using existing collection: {self.collection_name}")
            except (ValueError, Exception):
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "KPI GPT document embeddings"}
                )
                logger.info(f"Created new collection: {self.collection_name}")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = self.embedding_model.encode(
                texts, 
                convert_to_tensor=False,
                normalize_embeddings=True,
                show_progress_bar=True
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add document chunks to the vector database"""
        try:
            if not chunks:
                logger.warning("No chunks provided to add to database")
                return False
            
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                documents.append(chunk['content'])
                metadatas.append({
                    'section': chunk['section'],
                    'chunk_id': chunk['chunk_id'],
                    'length': chunk['metadata'].get('length', 0),
                    'chunk_num': chunk['metadata'].get('chunk_num', 0)
                })
                ids.append(chunk['chunk_id'])
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(documents)} documents...")
            embeddings = self.generate_embeddings(documents)
            
            # Add to collection
            logger.info("Adding documents to vector database...")
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(documents)} documents to the database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to database: {e}")
            return False
    
    def search_similar(self, query: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents based on query, with optional metadata filter"""
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances'],
                where=where if where else None
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity_score': 1.0 - results['distances'][0][i],  # Convert distance to similarity
                        'distance': results['distances'][0][i]
                    }
                    formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} similar documents for query")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching database: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the current collection"""
        try:
            count = self.collection.count()
            return {
                'name': self.collection_name,
                'document_count': count,
                'embedding_model': self.embedding_model_name,
                'database_path': self.db_path
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self) -> bool:
        """Delete the current collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False
    
    def reset_database(self) -> bool:
        """Reset the entire database"""
        try:
            self.client.reset()
            self._initialize_db()
            logger.info("Database reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            return False
    
    def export_database(self, export_path: str) -> bool:
        """Export database contents to JSON file"""
        try:
            # Get all documents from collection
            results = self.collection.get(
                include=['documents', 'metadatas', 'embeddings']
            )
            
            export_data = {
                'collection_name': self.collection_name,
                'document_count': len(results['documents']),
                'embedding_model': self.embedding_model_name,
                'documents': results['documents'],
                'metadatas': results['metadatas'],
                'ids': results['ids']
                # Note: embeddings are excluded from export to reduce file size
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Database exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting database: {e}")
            return False

def create_and_populate_database(data_file: str, db_path: str = "./vector_db") -> VectorDatabase:
    """Create and populate vector database with KPI data"""
    from data_preprocessor import KPIDataProcessor
    
    # Initialize components
    processor = KPIDataProcessor()
    vector_db = VectorDatabase(db_path=db_path)
    
    # Process data and create chunks
    logger.info("Processing KPI data...")
    chunks = processor.process_file(data_file)
    
    # Add to vector database
    logger.info("Adding chunks to vector database...")
    success = vector_db.add_documents(chunks)
    
    if success:
        info = vector_db.get_collection_info()
        logger.info(f"Database created successfully: {info}")
        return vector_db
    else:
        logger.error("Failed to create database")
        return None

if __name__ == "__main__":
    # Test the vector database
    vector_db = create_and_populate_database("kpi_data.txt")
    
    if vector_db:
        # Test search
        query = "Who is the principal of KPI?"
        results = vector_db.search_similar(query, n_results=3)
        
        print(f"\nSearch results for: '{query}'")
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Similarity: {result['similarity_score']:.3f}")
            print(f"Section: {result['metadata']['section']}")
            print(f"Content: {result['content'][:200]}...")
        
        # Show database info
        info = vector_db.get_collection_info()
        print(f"\nDatabase Info: {info}")
