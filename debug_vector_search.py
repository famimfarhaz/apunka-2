#!/usr/bin/env python3
"""
Debug vector search to find why Julekha is not being retrieved properly
"""

from vector_database import VectorDatabase
import logging

logging.basicConfig(level=logging.INFO)

def debug_search():
    print("🔍 Debugging Vector Search for Julekha Akter Koli")
    print("=" * 50)
    
    # Initialize vector database
    vdb = VectorDatabase('./vector_db')
    
    # Get collection info
    info = vdb.get_collection_info()
    print(f"📊 Database Info: {info['document_count']} documents")
    
    # Different search strategies
    search_terms = [
        "Julekha Akter Koli",
        "Julekha",
        "Koli", 
        "chemistry instructor",
        "non-tech chemistry",
        "1642-880100",
        "+880 1642-880100",
        "Instructor Non-Tech Chemistry",
        "Name: Julekha Akter Koli"
    ]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: '{term}'")
        print("-" * 30)
        
        results = vdb.search_similar(term, n_results=3, where=None)
        
        if results:
            for i, result in enumerate(results, 1):
                score = result.get('similarity_score', 0)
                content = result.get('content', '')[:300]
                section = result.get('metadata', {}).get('section', 'Unknown')
                
                # Check if content contains Julekha
                has_julekha = 'julekha' in content.lower()
                
                print(f"   {i}. Score: {score:.3f} | Section: {section} | Has Julekha: {has_julekha}")
                print(f"      Content: {content}...")
                print()
        else:
            print("   No results found!")

if __name__ == "__main__":
    debug_search()
