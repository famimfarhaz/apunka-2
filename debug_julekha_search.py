#!/usr/bin/env python3

from vector_database import VectorDatabase
from kpi_gpt_rag import create_kpi_rag_system

print("🔍 Debugging Julekha Akter Koli search...")

# Test 1: Direct vector database search
print("\n1. Testing direct vector database search:")
try:
    vdb = VectorDatabase()
    results = vdb.search('Julekha Akter Koli', top_k=10)
    print(f"Found {len(results)} results:")
    for i, r in enumerate(results):
        print(f"  {i+1}. Score: {r['score']:.3f}")
        print(f"      Content: {r['content'][:150]}...")
        print()
except Exception as e:
    print(f"Error: {e}")

# Test 2: RAG system search
print("\n2. Testing RAG system search:")
try:
    rag_system = create_kpi_rag_system()
    rag_system.setup_system()
    
    response = rag_system.query("Who is Julekha Akter Koli?")
    print(f"RAG Response: {response}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Check if the data exists in vector database
print("\n3. Searching for individual words:")
try:
    vdb = VectorDatabase()
    
    # Search for individual components
    for term in ['Julekha', 'Akter', 'Koli', 'Chemistry', 'Non-Tech']:
        results = vdb.search(term, top_k=3)
        print(f"\nSearching '{term}':")
        for r in results[:2]:
            if term.lower() in r['content'].lower():
                print(f"  ✅ Found: Score {r['score']:.3f}")
                print(f"      Content: {r['content'][:100]}...")
            else:
                print(f"  ❌ No match: Score {r['score']:.3f}")
                
except Exception as e:
    print(f"Error: {e}")

# Test 4: Check collection contents
print("\n4. Checking collection info:")
try:
    vdb = VectorDatabase()
    info = vdb.get_collection_info()
    print(f"Total documents in collection: {info}")
except Exception as e:
    print(f"Error: {e}")
