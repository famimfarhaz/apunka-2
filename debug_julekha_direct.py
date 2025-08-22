#!/usr/bin/env python3
"""
Debug script to find Julekha Akter Koli in the database
"""

from vector_database import VectorDatabase
import logging

logging.basicConfig(level=logging.ERROR)

def find_julekha():
    """Find Julekha in the database using different approaches"""
    
    print("🔍 Searching for Julekha Akter Koli in database...")
    print("=" * 60)
    
    vdb = VectorDatabase()
    
    # Test different search queries
    search_queries = [
        "Julekha Akter Koli",
        "Julekha Akter Koli chemistry instructor",
        "chemistry instructor non-tech",
        "Julekha",
        "Koli",
        "instructor chemistry"
    ]
    
    found_results = []
    
    for query in search_queries:
        print(f"\n🔎 Query: '{query}'")
        results = vdb.search_similar(query, n_results=10)
        
        for i, result in enumerate(results, 1):
            content_lower = result['content'].lower()
            if 'julekha' in content_lower and 'koli' in content_lower:
                print(f"✅ FOUND in result {i}!")
                print(f"  Section: {result['metadata']['section']}")
                print(f"  Similarity: {result['similarity_score']:.3f}")
                print(f"  Content preview: {result['content'][:200]}...")
                found_results.append((query, result))
                break
        else:
            print("❌ Not found in this query")
    
    # If we found her, show the best result
    if found_results:
        print(f"\n🎯 BEST MATCH:")
        best_query, best_result = max(found_results, key=lambda x: x[1]['similarity_score'])
        print(f"Best query: '{best_query}'")
        print(f"Similarity: {best_result['similarity_score']:.3f}")
        print(f"Section: {best_result['metadata']['section']}")
        print(f"Full content:\n{best_result['content']}")
    else:
        print("\n❌ Julekha Akter Koli was not found in any search results")
        
        # Let's check if the teachers section has the data by filtering directly
        print("\n🔍 Checking teachers section directly...")
        teacher_results = vdb.search_similar("teacher instructor", n_results=20, where={"section": "teachers"})
        
        for result in teacher_results:
            if 'julekha' in result['content'].lower():
                print(f"✅ Found in teachers section!")
                print(f"Content: {result['content']}")
                break
        else:
            print("❌ Still not found in teachers section")

if __name__ == "__main__":
    find_julekha()
