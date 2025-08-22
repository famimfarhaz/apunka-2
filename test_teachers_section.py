#!/usr/bin/env python3

from kpi_gpt_rag import create_kpi_rag_system

print("🧪 Testing teachers section search...")

# Initialize RAG system
rag_system = create_kpi_rag_system()
rag_system.setup_system()

print("1. Testing direct search with teachers section filter:")
results = rag_system.vector_db.search_similar('Julekha Akter Koli', n_results=10, where={'section': 'teachers'})

for i, result in enumerate(results):
    contains_julekha = 'julekha' in result['content'].lower() or 'koli' in result['content'].lower()
    indicator = "🎯" if contains_julekha else "  "
    print(f"  {indicator} {i+1}. Score: {result['similarity_score']:.4f}")
    if contains_julekha:
        print(f"      ✅ FOUND JULEKHA/KOLI!")
    print(f"      Content: {result['content'][:100]}...")
    print()

print("2. Testing simple search queries in teachers section:")
simple_queries = ['Julekha', 'Koli', 'Chemistry instructor', 'BCS 40']

for query in simple_queries:
    print(f"\n--- Query: '{query}' ---")
    results = rag_system.vector_db.search_similar(query, n_results=5, where={'section': 'teachers'})
    
    for i, result in enumerate(results):
        contains_julekha = 'julekha' in result['content'].lower() or 'koli' in result['content'].lower()
        indicator = "🎯" if contains_julekha else "  "
        print(f"  {indicator} {i+1}. Score: {result['similarity_score']:.4f}")
        if contains_julekha:
            print(f"      ✅ FOUND JULEKHA/KOLI!")
            print(f"      Full content: {result['content']}")
        else:
            print(f"      Content: {result['content'][:100]}...")

print("\n3. Testing without section filter:")
results = rag_system.vector_db.search_similar('Julekha', n_results=10)
for i, result in enumerate(results):
    contains_julekha = 'julekha' in result['content'].lower() or 'koli' in result['content'].lower()
    if contains_julekha:
        print(f"🎯 Found Julekha at position {i+1}: Score {result['similarity_score']:.4f}")
        print(f"   Content: {result['content'][:150]}...")
        print(f"   Section: {result['metadata'].get('section', 'unknown')}")
        break
else:
    print("❌ No Julekha found in top 10 results without section filter")
    
# Final test - let's see what the system actually returns for a Julekha query
print("\n" + "="*50)
print("4. Full RAG system test:")
response = rag_system.query("Tell me about Julekha Akter Koli instructor")
print(f"Answer: {response['answer'][:200]}...")
if 'julekha' in response['answer'].lower():
    print("🎉 SUCCESS - Answer mentions Julekha!")
else:
    print("❌ Answer does not mention Julekha")
