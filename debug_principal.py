#!/usr/bin/env python3
"""
Debug script to check principal query retrieval
"""

from kpi_gpt_rag import create_kpi_rag_system

# Create system
print("Creating KPI RAG system...")
rag_system = create_kpi_rag_system()
success = rag_system.setup_system()

if not success:
    print("System setup failed!")
    exit(1)

print("System setup successful!")

# Test principal query with detailed debugging
print("\nTesting principal query...")
response = rag_system.query("Who is the principal of KPI?")

print(f"Query: {response['query']}")
print(f"Answer: {response['answer']}")
print(f"Sources found: {len(response.get('sources', []))}")

print("\nRetrieved Sources:")
for i, source in enumerate(response.get('sources', [])):
    print(f"\nSource {i+1}:")
    print(f"Section: {source['section']}")
    print(f"Score: {source['similarity_score']:.3f}")
    print(f"Content: {source['content_preview']}")

# Also test direct vector search for "principal"
print("\n" + "="*50)
print("DIRECT VECTOR SEARCH TEST")
print("="*50)

search_results = rag_system.vector_db.search_similar("principal Sheikh Mustafizur Rahman", n_results=10)

print(f"\nDirect search found {len(search_results)} results:")
for i, result in enumerate(search_results):
    print(f"\nResult {i+1}:")
    print(f"Section: {result['metadata']['section']}")
    print(f"Score: {result['similarity_score']:.3f}")
    print(f"Content preview: {result['content'][:300]}...")

# Test if principal info exists in the chunks
print("\n" + "="*50)  
print("CHECKING RAW DATA PROCESSING")
print("="*50)

from data_preprocessor import KPIDataProcessor

processor = KPIDataProcessor()
chunks = processor.process_file("kpi_data.txt")

principal_chunks = []
for chunk in chunks:
    if "principal" in chunk['content'].lower() or "sheikh mustafizur rahman" in chunk['content'].lower():
        principal_chunks.append(chunk)

print(f"\nFound {len(principal_chunks)} chunks containing principal info:")
for i, chunk in enumerate(principal_chunks):
    print(f"\nChunk {i+1}:")
    print(f"Section: {chunk['section']}")  
    print(f"Content: {chunk['content'][:500]}...")
