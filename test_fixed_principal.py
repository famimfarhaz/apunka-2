#!/usr/bin/env python3
"""
Test the fixed principal query system
"""

from kpi_gpt_rag import create_kpi_rag_system

def test_principal_query():
    """Test principal query after fixes"""
    
    print("🔧 Testing Fixed Principal Query System")
    print("=" * 50)
    
    # Create and setup system
    print("Creating KPI RAG system...")
    rag_system = create_kpi_rag_system()
    success = rag_system.setup_system()
    
    if not success:
        print("❌ System setup failed!")
        return
    
    print("✅ System setup successful!")
    
    # Test principal queries
    principal_queries = [
        "Who is the principal of KPI?",
        "Tell me about the principal",
        "Principal information",
        "Sheikh Mustafizur Rahman"
    ]
    
    for i, query in enumerate(principal_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        response = rag_system.query(query)
        
        print(f"Answer: {response['answer'][:200]}...")
        print(f"Sources: {len(response.get('sources', []))}")
        
        if response.get('sources'):
            for j, source in enumerate(response['sources'][:2]):
                print(f"  Source {j+1}: {source['section']} (Score: {source['similarity_score']:.3f})")

if __name__ == "__main__":
    test_principal_query()
