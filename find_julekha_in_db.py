#!/usr/bin/env python3
"""
Find all documents in vector database that contain Julekha
"""

import chromadb
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def find_julekha_documents():
    print("🔍 Searching ALL documents in vector database for Julekha")
    print("=" * 60)
    
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./vector_db")
    collection = client.get_collection("kpi_documents")
    
    # Get ALL documents from the collection
    all_docs = collection.get(include=['documents', 'metadatas'])
    
    print(f"📊 Total documents in database: {len(all_docs['documents'])}")
    
    # Search for Julekha in all documents
    julekha_docs = []
    for i, (document, metadata) in enumerate(zip(all_docs['documents'], all_docs['metadatas'])):
        if 'julekha' in document.lower():
            julekha_docs.append({
                'id': f'doc_{i}',
                'content': document,
                'metadata': metadata,
                'index': i
            })
    
    print(f"🎯 Documents containing 'Julekha': {len(julekha_docs)}")
    
    if julekha_docs:
        for i, doc in enumerate(julekha_docs, 1):
            print(f"\n📄 DOCUMENT {i}:")
            print(f"   ID: {doc['id']}")
            print(f"   Section: {doc['metadata'].get('section', 'Unknown')}")
            print(f"   Index: {doc['index']}")
            print(f"   Content: {doc['content']}")
            print("-" * 50)
    else:
        print("\n❌ NO DOCUMENTS containing 'Julekha' found in the vector database!")
        print("   This means the data is not being processed correctly.")
        
        # Let's check a few random documents to see what's there
        print(f"\n📋 Sample of documents in database:")
        for i in range(min(5, len(all_docs['documents']))):
            doc = all_docs['documents'][i]
            section = all_docs['metadatas'][i].get('section', 'Unknown')
            print(f"   {i+1}. Section: {section}")
            print(f"      Content preview: {doc[:200]}...")
            print()

if __name__ == "__main__":
    find_julekha_documents()
