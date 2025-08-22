#!/usr/bin/env python3
"""
Test script for the improved KPI GPT RAG system
Specifically testing Julekha Akter Koli query
"""

import os
import sys
from kpi_gpt_rag import create_kpi_rag_system
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_julekha_query():
    """Test the improved system with Julekha Akter Koli query"""
    
    print("🚀 Testing Improved KPI GPT RAG System")
    print("=" * 50)
    
    # Create and setup RAG system
    print("📚 Creating RAG system...")
    rag_system = create_kpi_rag_system()
    
    print("🔧 Setting up system (this may rebuild the database)...")
    setup_success = rag_system.setup_system(rebuild_db=True)  # Force rebuild
    
    if not setup_success:
        print("❌ Failed to setup RAG system")
        return False
    
    print("✅ RAG system setup completed!")
    
    # Show system info
    system_info = rag_system.get_system_info()
    print(f"📊 System Info:")
    print(f"   - Database documents: {system_info.get('database', {}).get('document_count', 'N/A')}")
    print(f"   - Embedding model: {system_info.get('models', {}).get('embedding', 'N/A')}")
    print(f"   - Status: {system_info.get('status', 'N/A')}")
    
    # Test queries
    test_queries = [
        "can you tell me about Julekha Akter Koli ?",
        "Who is Julekha Akter Koli?",
        "Julekha Akter Koli contact information",
        "Tell me about Julekha",
        "What is the phone number of Julekha Akter Koli?",
        "chemistry teacher Julekha"
    ]
    
    print("\n" + "=" * 50)
    print("🧪 Running Test Queries")
    print("=" * 50)
    
    success_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: {query}")
        print("-" * 30)
        
        try:
            # Process query
            response = rag_system.query(query, max_tokens=512, temperature=0.5)
            
            if 'error' in response:
                print(f"❌ Error: {response['error']}")
                continue
            
            answer = response.get('answer', 'No answer provided')
            sources = response.get('sources', [])
            
            # Check if Julekha information is found
            answer_lower = answer.lower()
            has_julekha = 'julekha' in answer_lower
            has_contact = any(term in answer_lower for term in ['phone', 'contact', 'mobile', '1642-880100', '01642-880100'])
            has_chemistry = 'chemistry' in answer_lower
            has_instructor = any(term in answer_lower for term in ['instructor', 'teacher'])
            
            print(f"🤖 KPI GPT Answer:")
            print(f"   {answer}")
            print(f"\n📊 Analysis:")
            print(f"   ✓ Found Julekha: {'YES' if has_julekha else 'NO'}")
            print(f"   ✓ Has Contact Info: {'YES' if has_contact else 'NO'}")
            print(f"   ✓ Mentions Chemistry: {'YES' if has_chemistry else 'NO'}")
            print(f"   ✓ Mentions Instructor: {'YES' if has_instructor else 'NO'}")
            print(f"   📚 Sources Used: {len(sources)}")
            
            # Success criteria: Must find Julekha and provide some relevant info
            if has_julekha and (has_contact or has_chemistry or has_instructor):
                print(f"   🎉 TEST RESULT: SUCCESS")
                success_count += 1
            else:
                print(f"   ❌ TEST RESULT: FAILED")
                
            # Show top sources
            if sources:
                print(f"   📄 Top Sources:")
                for j, source in enumerate(sources[:2], 1):
                    score = source.get('similarity_score', 0)
                    section = source.get('section', 'Unknown')
                    preview = source.get('content_preview', '')[:100] + "..."
                    print(f"      {j}. Section: {section} | Score: {score:.3f}")
                    print(f"         Preview: {preview}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            continue
    
    print(f"\n" + "=" * 50)
    print(f"📈 FINAL RESULTS")
    print(f"   Total Tests: {len(test_queries)}")
    print(f"   Successful: {success_count}")
    print(f"   Success Rate: {success_count/len(test_queries)*100:.1f}%")
    
    if success_count >= len(test_queries) * 0.7:  # 70% success rate
        print(f"   🎉 OVERALL: SUCCESS - System is working well!")
        return True
    else:
        print(f"   ⚠️  OVERALL: NEEDS IMPROVEMENT")
        return False

def test_vector_search_directly():
    """Test vector search directly to debug issues"""
    
    print("\n" + "=" * 50)
    print("🔍 Direct Vector Search Test")
    print("=" * 50)
    
    try:
        # Create system
        rag_system = create_kpi_rag_system()
        rag_system.setup_system()
        
        # Test direct vector search
        search_terms = ["Julekha", "Julekha Akter Koli", "chemistry instructor", "non-tech chemistry"]
        
        for term in search_terms:
            print(f"\n🔍 Searching for: '{term}'")
            results = rag_system.vector_db.search_similar(term, n_results=3, where=None)
            
            print(f"   📊 Found: {len(results)} documents")
            for i, result in enumerate(results, 1):
                score = result.get('similarity_score', 0)
                content = result.get('content', '')[:200]
                section = result.get('metadata', {}).get('section', 'Unknown')
                print(f"   {i}. Score: {score:.3f} | Section: {section}")
                print(f"      Content: {content}...")
                print()
                
    except Exception as e:
        print(f"❌ Vector search test failed: {e}")

if __name__ == "__main__":
    print("Starting comprehensive test of improved KPI GPT system...")
    
    # Test the main functionality
    main_success = test_julekha_query()
    
    # Test vector search directly
    test_vector_search_directly()
    
    if main_success:
        print(f"\n🎉 SUCCESS! The improved system is working correctly.")
        print(f"   Julekha Akter Koli can now be found by the system.")
    else:
        print(f"\n⚠️  The system still needs improvements.")
    
    print(f"\nTest completed!")
