#!/usr/bin/env python3
"""
Quick test to verify the new Groq API key is working
"""

from kpi_gpt_rag import create_kpi_rag_system
import logging

logging.basicConfig(level=logging.INFO)

def test_new_api_key():
    print("🔧 Testing KPI GPT with New Groq API Key")
    print("=" * 50)
    
    try:
        # Create and setup RAG system
        print("📚 Initializing system with new API key...")
        rag_system = create_kpi_rag_system()
        
        # Setup system
        print("🔧 Setting up system components...")
        setup_success = rag_system.setup_system()
        
        if not setup_success:
            print("❌ Failed to setup system")
            return False
        
        print("✅ System setup completed successfully!")
        
        # Test queries
        test_queries = [
            "Who is the principal of KPI?",
            "Tell me about Julekha Akter Koli",
            "What departments are available at KPI?",
            "Who created KPI GPT?",
            "What is the phone number of the principal?"
        ]
        
        print(f"\n🧪 Testing {len(test_queries)} queries with new API...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 40)
            
            try:
                response = rag_system.query(query, max_tokens=300, temperature=0.5)
                
                if 'error' not in response:
                    answer = response.get('answer', 'No answer')
                    print(f"✅ Success: {answer[:150]}{'...' if len(answer) > 150 else ''}")
                else:
                    print(f"❌ Error: {response.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"⚠️ Exception: {str(e)}")
        
        print(f"\n🎉 API key test completed successfully!")
        print("Your new Groq API key is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to test new API key: {str(e)}")
        return False

if __name__ == "__main__":
    test_new_api_key()
