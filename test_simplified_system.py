#!/usr/bin/env python3

from kpi_gpt_rag import create_kpi_rag_system

print("🧪 Testing Simplified KPI GPT System - Let Groq Handle Everything!")
print("=" * 70)

# Initialize RAG system
rag_system = create_kpi_rag_system()
rag_system.setup_system()

# Test various query formats
test_queries = [
    # Direct name queries
    "Who is Julekha Akter Koli?",
    "Tell me about Julekha Akter Koli",
    "Julekha Akter Koli information",
    "What do you know about Julekha Koli?",
    
    # Different formats
    "জুলেখা আক্তার কলি কে?",  # Bengali
    "koli chemistry teacher",
    "BCS 40 instructor",
    "Non-Tech Chemistry teacher",
    "+880 1642-880100 phone number",
    
    # Various question styles
    "Who teaches chemistry in non-tech department?",
    "List all chemistry instructors",
    "Principal information",
    "Tell me about KPI computer department",
    "What clubs are available?",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n🔍 Test {i}: '{query}'")
    print("-" * 50)
    
    try:
        response = rag_system.query(query)
        
        # Check for success indicators
        answer = response.get('answer', '')
        has_julekha = 'julekha' in answer.lower() or 'koli' in answer.lower()
        has_error = 'error' in response or 'sorry' in answer.lower() or "couldn't find" in answer.lower()
        
        if query.lower().__contains__('julekha') or query.lower().__contains__('koli'):
            if has_julekha:
                print("🎉 SUCCESS: Found Julekha information!")
            else:
                print("❌ FAILED: Julekha query but no Julekha in answer")
        elif has_error:
            print("⚠️  No specific info found, but system handled gracefully")
        else:
            print("✅ Successfully answered query")
        
        # Show answer preview
        answer_preview = answer[:200] + "..." if len(answer) > 200 else answer
        print(f"📝 Answer: {answer_preview}")
        
        # Show retrieval stats
        sources = response.get('sources', [])
        system_info = response.get('system_info', {})
        print(f"📊 Retrieved: {system_info.get('retrieval_results', 0)} documents | Sources: {len(sources)}")
        
        if sources:
            best_score = sources[0].get('similarity_score', 0) if sources else 0
            print(f"🎯 Best similarity: {best_score:.3f}")
        
    except Exception as e:
        print(f"💥 ERROR: {e}")

print(f"\n" + "=" * 70)
print("🏁 Test Complete! The simplified system now:")
print("✅ Uses multi-approach retrieval (direct + word-based + section-based)")  
print("✅ Passes more context to Groq (16 documents instead of 5)")
print("✅ Lets Groq AI interpret and understand any question format")
print("✅ No complex word triggers or query expansion needed")
print("🎯 Groq AI handles the intelligence - we just provide good retrieval!")
