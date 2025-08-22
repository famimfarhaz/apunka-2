#!/usr/bin/env python3
"""
Script to find specific people in the vector database
"""

from vector_database import VectorDatabase
import logging

# Suppress INFO logs
logging.basicConfig(level=logging.ERROR)

def find_person(name):
    """Find a specific person in the database"""
    
    vdb = VectorDatabase()
    
    # Try different search queries
    search_queries = [
        name,
        f"{name} teacher",
        f"{name} instructor", 
        f"{name} chemistry",
        name.split()[0],  # First name only
        name.split()[-1] if len(name.split()) > 1 else name,  # Last name only
    ]
    
    print(f"Searching for: {name}")
    print("=" * 50)
    
    all_results = {}
    
    for query in search_queries:
        print(f"\nQuery: '{query}'")
        results = vdb.search_similar(query, n_results=10)
        
        found_matches = []
        for result in results:
            content_lower = result['content'].lower()
            name_parts = name.lower().split()
            
            # Check if all parts of the name are in the content
            if all(part in content_lower for part in name_parts):
                found_matches.append(result)
        
        if found_matches:
            print(f"  ✅ FOUND {len(found_matches)} matches!")
            for i, match in enumerate(found_matches, 1):
                print(f"\n  Match {i}:")
                print(f"    Section: {match['metadata']['section']}")
                print(f"    Similarity: {match['similarity_score']:.3f}")
                print(f"    Content: {match['content'][:200]}...")
                
                # Store the best match
                if query not in all_results or match['similarity_score'] > all_results[query]['similarity_score']:
                    all_results[query] = match
        else:
            print("  ❌ No direct matches found")
    
    # Show the best overall result
    if all_results:
        best_result = max(all_results.values(), key=lambda x: x['similarity_score'])
        print(f"\n🎯 BEST MATCH:")
        print(f"   Section: {best_result['metadata']['section']}")
        print(f"   Similarity: {best_result['similarity_score']:.3f}")
        print(f"   Full content: {best_result['content']}")
    else:
        print(f"\n❌ No matches found for {name} in the database")

def main():
    """Test with specific people"""
    
    people_to_find = [
        "Julekha Akter Koli",
        "Famim Farhaz",
        "S.M. Kamruzzaman"
    ]
    
    for person in people_to_find:
        find_person(person)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
