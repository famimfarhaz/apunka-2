#!/usr/bin/env python3

from kpi_gpt_rag import create_kpi_rag_system

print("🧪 Testing RAG system with phone number query...")

# Initialize RAG system
rag_system = create_kpi_rag_system()
rag_system.setup_system()

# Test queries that should work based on vector search results
test_queries = [
    "+880 1642-880100",  # This found Julekha in 3rd position
    "phone number 1642-880100",
    "BCS 40 instructor",  # BCS 40 is Julekha's batch
    "Chemistry instructor BCS 40",
    "Non-Tech Chemistry instructor",
    "Instructor Non-Tech Chemistry"
]

for query in test_queries:
    print(f"\n🔍 Testing query: '{query}'")
    print("-" * 50)
    
    response = rag_system.query(query)
    
    print(f"Answer: {response['answer'][:300]}...")
    print(f"Sources: {len(response.get('sources', []))}")
    
    # Check if Julekha is mentioned in answer or sources
    answer_has_julekha = 'julekha' in response['answer'].lower() or 'koli' in response['answer'].lower()
    
    for i, source in enumerate(response.get('sources', [])[:3]):
        source_has_julekha = 'julekha' in source['content_preview'].lower() or 'koli' in source['content_preview'].lower()
        indicator = "🎯" if source_has_julekha else "  "
        print(f"  {indicator} Source {i+1}: Score {source['similarity_score']:.4f}")
        if source_has_julekha:
            print(f"      ✅ CONTAINS JULEKHA/KOLI!")
    
    if answer_has_julekha:
        print(f"🎉 SUCCESS: Answer contains Julekha/Koli!")
    else:
        print(f"❌ Answer does not contain Julekha/Koli")

print(f"\n" + "="*60)
print("🎯 Now testing exact name query with improved understanding...")

response = rag_system.query("Who is Julekha Akter Koli? Tell me about her role at KPI.")
print(f"Final test answer: {response['answer']}")
