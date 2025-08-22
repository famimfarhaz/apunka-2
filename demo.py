"""
Demo Script for KPI GPT RAG System
Created by: Famim Farhaz

This script demonstrates the capabilities of the KPI GPT RAG system
with various sample queries.
"""

from kpi_gpt_rag import create_kpi_rag_system
import time

def run_demo():
    """Run demonstration of KPI GPT RAG system"""
    
    print("=" * 60)
    print("🎯 KPI GPT RAG System Demo")
    print("Created by: Famim Farhaz")
    print("=" * 60)
    
    # Initialize the RAG system
    print("\n🚀 Initializing KPI GPT RAG System...")
    try:
        rag_system = create_kpi_rag_system()
        
        print("📚 Setting up system components...")
        setup_success = rag_system.setup_system()
        
        if not setup_success:
            print("❌ Failed to setup RAG system")
            return
        
        print("✅ System ready!\n")
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return
    
    # Sample queries to demonstrate system capabilities
    sample_queries = [
        "Who is the principal of KPI?",
        "Tell me about the Computer Science department",
        "What is CODE KPI?",
        "Who is Famim Farhaz?",
        "List the departments in KPI",
        "Give me contact information for the Civil department head",
        "What clubs are available at KPI?",
        "Who is Susmita Kundu?",
        "Tell me about Khulna Polytechnic Institute"
    ]
    
    print("🔍 Running demo queries...")
    print("=" * 60)
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n📋 Query {i}: {query}")
        print("-" * 50)
        
        try:
            # Process the query
            response = rag_system.query(query)
            
            if 'error' not in response:
                print(f"🤖 Answer: {response['answer']}")
                
                # Show top sources
                if response.get('sources'):
                    print(f"\n📚 Top sources ({len(response['sources'][:2])}/):")
                    for j, source in enumerate(response['sources'][:2], 1):
                        print(f"   {j}. {source['section']} (Similarity: {source['similarity_score']:.2f})")
            else:
                print(f"❌ Error: {response['error']}")
            
            print(f"\n📊 Model: {response.get('model_used', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        # Small delay between queries
        time.sleep(1)
        
        if i < len(sample_queries):
            print("\n" + "=" * 60)
    
    # Show system information
    print(f"\n\n🔧 System Information:")
    print("-" * 30)
    system_info = rag_system.get_system_info()
    
    if system_info.get('status') == 'ready':
        print(f"📊 Database documents: {system_info['database']['document_count']}")
        print(f"🤖 Embedding model: {system_info['models']['embedding']}")
        print(f"🧠 Generation model: {system_info['models']['generation']}")
        print(f"⚙️  Chunk size: {system_info['config']['chunk_size']}")
        print(f"🔗 Max retrieval: {system_info['config']['max_retrieval_results']}")
    else:
        print(f"Status: {system_info.get('status', 'unknown')}")
    
    print(f"\n{'=' * 60}")
    print("✨ Demo completed! The KPI GPT RAG system is working perfectly.")
    print("💡 You can now use the system interactively by running: python kpi_gpt_rag.py")
    print("📝 Created by: Famim Farhaz for Khulna Polytechnic Institute")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
