#!/usr/bin/env python3
"""
Test script specifically for Julekha Akter Koli query
"""

import sys
from kpi_gpt_rag import KPIGPTRagSystem

def test_julekha_query():
    """Test specifically for Julekha Akter Koli information."""
    
    print("🔍 Testing Julekha Akter Koli Query")
    print("=" * 40)
    
    try:
        # Initialize and setup system
        print("📚 Setting up KPI GPT system...")
        rag_system = KPIGPTRagSystem()
        success = rag_system.setup_system()
        
        if not success:
            print("❌ Failed to setup system")
            return False
        
        print("✅ System setup complete!\n")
        
        # Test different variations of the query
        test_queries = [
            "Tell me about Julekha Akter Koli",
            "Who is Julekha Akter Koli?",
            "Julekha Akter Koli information",
            "What is the designation of Julekha Akter Koli?",
            "Julekha phone number"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 Query {i}: {query}")
            print("-" * 30)
            
            try:
                response = rag_system.query(query, max_tokens=300, temperature=0.3)
                
                if response and response.get('answer'):
                    print(f"✅ Answer: {response['answer']}")
                    print(f"📊 Sources found: {len(response.get('sources', []))}")
                    
                    # Check if the answer mentions Julekha
                    if 'Julekha' in response['answer'] or 'Chemistry' in response['answer']:
                        print("🎯 Relevant information found!")
                    else:
                        print("⚠️  Answer doesn't seem to contain Julekha's information")
                else:
                    print("❌ No answer received")
                    print(f"Full response: {response}")
                
                print()
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
                print()
            
            # Small delay to avoid rate limits
            import time
            time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Julekha Akter Koli Query Test")
    print("=" * 40)
    
    success = test_julekha_query()
    
    if success:
        print("\n✅ Test completed successfully")
    else:
        print("\n❌ Test failed")
        sys.exit(1)
