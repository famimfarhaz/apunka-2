#!/usr/bin/env python3
"""
Debug script specifically for Julekha Akter Koli query
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

def debug_julekha_query():
    """Debug the Julekha Akter Koli query step by step"""
    
    print("🔍 Debugging Julekha Akter Koli Query")
    print("=" * 60)
    
    # Initialize RAG system
    rag = KPIGPTRagSystem()
    rag.setup_system()
    
    query = "Who is Julekha Akter Koli?"
    
    # Step 1: Test vector search directly
    print("\n1. Testing vector search...")
    retrieved_docs = rag.vector_db.search_similar(query, n_results=5)
    
    print(f"Retrieved {len(retrieved_docs)} documents:")
    for i, doc in enumerate(retrieved_docs, 1):
        content_lower = doc['content'].lower()
        has_julekha = 'julekha' in content_lower
        has_koli = 'koli' in content_lower
        
        print(f"\nDoc {i}:")
        print(f"  Section: {doc['metadata']['section']}")
        print(f"  Similarity: {doc['similarity_score']:.3f}")
        print(f"  Has 'julekha': {has_julekha}")
        print(f"  Has 'koli': {has_koli}")
        print(f"  Content preview: {doc['content'][:150]}...")
        
        if has_julekha or has_koli:
            print(f"  ⭐ MATCH FOUND!")
    
    # Step 2: Test RAG generation
    print(f"\n2. Testing RAG generation...")
    full_response = rag.query(query)
    
    print(f"Query: {full_response['query']}")
    print(f"Answer: {full_response['answer'][:300]}...")
    print(f"Sources in response: {len(full_response.get('sources', []))}")
    
    if 'sources' in full_response:
        print("\nSource details:")
        for i, source in enumerate(full_response['sources'], 1):
            print(f"  Source {i}: {source}")
    
    # Step 3: Try alternative queries
    print(f"\n3. Testing alternative queries...")
    alternative_queries = [
        "Julekha Akter Koli chemistry teacher",
        "instructor chemistry non-tech", 
        "chemistry department teachers",
        "Julekha instructor"
    ]
    
    for alt_query in alternative_queries:
        print(f"\nQuery: '{alt_query}'")
        alt_response = rag.query(alt_query)
        
        # Check if Julekha is mentioned in the answer
        if 'julekha' in alt_response['answer'].lower():
            print(f"  ✅ FOUND in answer: {alt_response['answer'][:200]}...")
        else:
            print(f"  ❌ Not found in answer")

if __name__ == "__main__":
    debug_julekha_query()
