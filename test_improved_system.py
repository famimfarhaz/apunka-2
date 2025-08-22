#!/usr/bin/env python3
"""
Test script for the improved RAG system with query expansion
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging

# Suppress INFO logs for cleaner output
logging.basicConfig(level=logging.ERROR)

def test_improved_system():
    """Test the improved system with problematic queries"""
    
    print("🧪 Testing Improved KPI RAG System")
    print("=" * 60)
    
    rag = KPIGPTRagSystem()
    success = rag.setup_system()
    
    if not success:
        print("❌ Failed to setup system")
        return
    
    # Test queries that were problematic before
    test_queries = [
        "Who is Julekha Akter Koli?",
        "Tell me about Julekha Akter Koli",
        "Who is Famim Farhaz?",
        "Who are the class captains?",
        "Tell me about Ripon Hossain",
        "Who is S.M. Kamruzzaman?",
        "List civil department teachers"
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} queries:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        response = rag.query(query)
        
        if 'error' in response:
            print(f"❌ Error: {response['error']}")
        else:
            # Check if the answer seems relevant
            answer = response['answer']
            query_words = query.lower().split()
            
            # Look for key names/terms in the answer
            relevant_terms = []
            for word in query_words:
                if len(word) > 3 and word.isalpha() and word.lower() in answer.lower():
                    relevant_terms.append(word)
            
            if relevant_terms:
                print(f"✅ SUCCESS - Found relevant information")
                print(f"   Relevant terms found: {', '.join(relevant_terms)}")
                print(f"   Answer preview: {answer[:150]}...")
            else:
                print(f"⚠️  PARTIAL - Response generated but relevance unclear")
                print(f"   Answer preview: {answer[:150]}...")
            
            print(f"   📊 Sources: {len(response.get('sources', []))} from sections: {', '.join(set(s['section'] for s in response.get('sources', [])))}")
    
    print(f"\n✅ Testing completed!")

if __name__ == "__main__":
    test_improved_system()
