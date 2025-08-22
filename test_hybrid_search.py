#!/usr/bin/env python3
"""
Test the new hybrid search system for finding Julekha Akter Koli
"""

from vector_database import VectorDatabase
import logging

logging.basicConfig(level=logging.INFO)

def test_hybrid_search():
    print("🔍 Testing Hybrid Search for Julekha Akter Koli")
    print("=" * 50)
    
    # Initialize vector database
    vdb = VectorDatabase('./vector_db')
    
    # Test queries for Julekha
    test_queries = [
        "Julekha Akter Koli",
        "Julekha",
        "Koli",
        "chemistry instructor Julekha",
        "Who is Julekha Akter Koli?",
        "+880 1642-880100",
        "non-tech chemistry teacher"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 30)
        
        results = vdb.search_similar(query, n_results=3, where=None)
        
        if results:
            for i, result in enumerate(results, 1):
                score = result.get('similarity_score', 0)
                content = result.get('content', '')[:300]
                section = result.get('metadata', {}).get('section', 'Unknown')
                method = result.get('search_method', 'unknown')
                
                # Check if content contains Julekha
                has_julekha = 'julekha' in content.lower()
                
                print(f"   {i}. Score: {score:.3f} | Method: {method} | Section: {section}")
                print(f"      Has Julekha: {'✅' if has_julekha else '❌'}")
                print(f"      Content: {content}...")
                print()
        else:
            print("   ❌ No results found!")

if __name__ == "__main__":
    test_hybrid_search()
