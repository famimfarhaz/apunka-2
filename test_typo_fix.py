#!/usr/bin/env python3
"""
Test the typo handling fix for principal queries
"""

from kpi_gpt_rag import create_kpi_rag_system

def test_typo_fix():
    """Test principal query with typo handling"""
    
    print("🔧 Testing Typo Fix for Principal Queries")
    print("=" * 50)
    
    # Create and setup system
    print("Creating KPI RAG system...")
    rag_system = create_kpi_rag_system()
    success = rag_system.setup_system()
    
    if not success:
        print("❌ System setup failed!")
        return
    
    print("✅ System setup successful!")
    
    # Test the problematic query with typo
    problematic_queries = [
        "did you have any information about the principle of kpi ?",
        "Who is the principle of KPI?", 
        "Tell me about the principle",
        "principle information"
    ]
    
    for i, query in enumerate(problematic_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        response = rag_system.query(query)
        
        print(f"Answer: {response['answer'][:200]}...")
        print(f"Sources: {len(response.get('sources', []))}")
        
        if response.get('sources'):
            for j, source in enumerate(response['sources'][:2]):
                print(f"  Source {j+1}: {source['section']} (Score: {source['similarity_score']:.3f})")

if __name__ == "__main__":
    test_typo_fix()
