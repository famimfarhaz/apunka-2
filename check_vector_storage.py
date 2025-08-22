#!/usr/bin/env python3
"""
Check how data is stored in the vector database
"""

from vector_database import VectorDatabase
from data_preprocessor import KPIDataProcessor

def check_vector_storage():
    """Check how data is stored in the vector database"""
    
    # Initialize components
    processor = KPIDataProcessor()
    vector_db = VectorDatabase()
    
    # Test a specific query
    query = "Julekha Akter Koli"
    print(f"Searching for: '{query}'")
    
    results = vector_db.search_similar(query, n_results=5)
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Content (first 200 chars): {result['content'][:200]}...")
        print(f"  Metadata: {result['metadata']}")
        print(f"  Similarity: {result['similarity_score']:.3f}")
        
    # Also check some data from the collection directly
    print("\n" + "="*60)
    print("Checking raw collection data...")
    
    collection_info = vector_db.get_collection_info()
    print(f"Collection info: {collection_info}")
    
    # Get a few random documents
    try:
        raw_results = vector_db.collection.get(limit=3, include=['documents', 'metadatas'])
        if raw_results['documents']:
            print(f"\nFirst few documents in collection:")
            for i in range(min(3, len(raw_results['documents']))):
                print(f"\nDocument {i+1}:")
                print(f"  Content (first 100 chars): {raw_results['documents'][i][:100]}...")
                print(f"  Metadata: {raw_results['metadatas'][i]}")
    except Exception as e:
        print(f"Error getting raw data: {e}")

if __name__ == "__main__":
    check_vector_storage()
