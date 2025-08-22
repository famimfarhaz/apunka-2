#!/usr/bin/env python3

from kpi_gpt_rag import create_kpi_rag_system

print("🧪 Testing name matching function...")

# Initialize RAG system
rag_system = create_kpi_rag_system()
rag_system.setup_system()

# Sample content from earlier check containing Julekha
test_content = "**Name:** Julekha Akter Koli **Designation:** Instructor (Non-Tech/Chemistry) **Faculty:** Non-Tech **Department:** RS (Non-Tech) **Email:** — **Batch (BCS):** 40 **Phone (Office):** +880 1642-880100"

# Test queries
test_queries = [
    "Who is Julekha Akter Koli?",
    "Who is Julekha Koli?",
    "Who is Koli?",
    "tell me about Julekha",
    "Julekha Akter Koli"
]

print("Testing _contains_person_name function:")
for query in test_queries:
    contains_name = rag_system._contains_person_name(test_content, query)
    print(f"Query: '{query}' -> {contains_name}")
    
    # Debug the matching logic
    query_cleaned = query.lower().replace('who is', '').replace('tell me about', '').replace('?', '').strip()
    query_words = query_cleaned.split()
    name_words = [word for word in query_words if len(word) > 2 and word.isalpha()]
    
    print(f"  - Cleaned query: '{query_cleaned}'")
    print(f"  - Name words: {name_words}")
    
    content_lower = test_content.lower()
    matches = [name_word for name_word in name_words if name_word in content_lower]
    print(f"  - Found matches: {matches} ({len(matches)}/{len(name_words)})")
    print()

# Test actual search with debug
print("\n" + "="*50)
print("Testing actual expanded search:")

query = "Who is Julekha Akter Koli?"
expanded_queries = rag_system._generate_person_queries(query)
print(f"Expanded queries: {expanded_queries}")

for i, expanded_query in enumerate(expanded_queries):
    print(f"\nTesting expanded query {i+1}: '{expanded_query}'")
    results = rag_system.vector_db.search_similar(expanded_query, n_results=3)
    
    for j, result in enumerate(results):
        contains_name = rag_system._contains_person_name(result['content'], query)
        indicator = "🎯" if contains_name else "  "
        print(f"  {indicator} Result {j+1}: Score {result['similarity_score']:.4f}")
        if 'julekha' in result['content'].lower() or 'koli' in result['content'].lower():
            print(f"      ✅ CONTAINS JULEKHA/KOLI!")
            print(f"      Content: {result['content'][:100]}...")
        else:
            print(f"      Content: {result['content'][:100]}...")
        print(f"      Name match: {contains_name}")
        print()
