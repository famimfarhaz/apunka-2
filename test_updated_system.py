#!/usr/bin/env python3
"""
Test script for the updated KPI GPT RAG System
Created by: Famim Farhaz
"""

from kpi_gpt_rag import KPIGPTRagSystem

def test_updated_system():
    """Test the updated RAG system with new data"""
    print("🧪 Testing Updated KPI GPT RAG System")
    print("=" * 50)
    
    # Initialize the system
    rag_system = KPIGPTRagSystem()
    
    # Setup the system (will use existing database if available)
    print("📚 Setting up system...")
    success = rag_system.setup_system()
    
    if not success:
        print("❌ Failed to setup system")
        return
    
    # Get system info
    print("\n📊 System Information:")
    info = rag_system.vector_db.get_collection_info()
    print(f"   - Documents in database: {info.get('document_count', 0)}")
    print(f"   - Embedding model: {info.get('embedding_model', 'Unknown')}")
    print(f"   - Database path: {info.get('database_path', 'Unknown')}")
    
    # Test queries
    test_queries = [
        "Who is the principal of KPI?",
        "Tell me about Civil Technology department",
        "What is BNCC?",
        "Give me the contact of Computer department head",
        "Tell me about your creator"
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} sample queries:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 30)
        
        response = rag_system.query(query)
        
        if 'error' in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"✅ Answer: {response['answer'][:200]}...")
            print(f"📁 Sources found: {len(response.get('sources', []))}")
    
    print("\n✅ Testing completed!")
    print("🎉 Your KPI RAG system is updated and working with the new data!")

if __name__ == "__main__":
    test_updated_system()
