#!/usr/bin/env python3

from vector_database import VectorDatabase
import time

print("🧪 Testing vector database similarity search...")

# Initialize vector database
vdb = VectorDatabase()

# Test different query variations
queries = [
    "Julekha Akter Koli",
    "Julekha Koli", 
    "Koli Chemistry instructor",
    "Non-Tech Chemistry teacher",
    "Instructor Chemistry Non-Tech",
    "BCS 40 Chemistry",
    "+880 1642-880100",
    "RS Non-Tech Chemistry"
]

print(f"Testing {len(queries)} different query variations:")

for query in queries:
    print(f"\n🔍 Query: '{query}'")
    results = vdb.search_similar(query, n_results=5)
    
    for i, result in enumerate(results):
        score = result.get('similarity_score', 0)
        content = result.get('content', '')
        
        # Check if this result contains Julekha
        contains_julekha = 'julekha' in content.lower() or 'koli' in content.lower()
        indicator = "🎯" if contains_julekha else "  "
        
        print(f"  {indicator} {i+1}. Score: {score:.4f}")
        print(f"      Content: {content[:100]}...")
        
        if contains_julekha:
            print(f"      ✅ FOUND JULEKHA/KOLI!")

# Test direct embedding similarity
print(f"\n" + "="*60)
print("📊 Testing embedding similarity for Julekha chunks...")

# Get all documents and check which ones contain Julekha
collection = vdb.collection
all_results = collection.get()

julekha_docs = []
for i, doc in enumerate(all_results['documents']):
    if 'julekha' in doc.lower() or 'koli' in doc.lower():
        julekha_docs.append((i, doc))

print(f"Found {len(julekha_docs)} documents containing Julekha/Koli")

for i, (doc_idx, doc) in enumerate(julekha_docs):
    print(f"\n--- Julekha Document {i+1} ---")
    print(f"Document Index: {doc_idx}")
    print(f"Content: {doc[:200]}...")
    
    # Test similarity with this exact document
    results = vdb.search_similar(doc[:50], n_results=3)
    print(f"Self-similarity test (first 50 chars):")
    for j, result in enumerate(results):
        self_match = result['content'] == doc
        indicator = "🎯" if self_match else "  "
        print(f"  {indicator} {j+1}. Score: {result['similarity_score']:.4f} {'(EXACT MATCH)' if self_match else ''}")
