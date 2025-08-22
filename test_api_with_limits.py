#!/usr/bin/env python3
"""
Enhanced API Test Script with Rate Limit Handling
Test the KPI GPT system with the new Groq API key, including proper rate limit handling.
"""

import time
import sys
from kpi_gpt_rag import KPIGPTRagSystem

def test_api_with_rate_limits():
    """Test the KPI GPT system with proper rate limit handling."""
    
    print("🔧 Testing KPI GPT with Rate Limit Handling")
    print("=" * 50)
    
    # Initialize the system
    print("📚 Initializing system...")
    try:
        rag_system = KPIGPTRagSystem()
        print("✅ System initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return False
    
    # Setup the system
    print("🔧 Setting up system components...")
    try:
        rag_system.setup_system()
        print("✅ System setup completed successfully!")
    except Exception as e:
        print(f"❌ Failed to setup system: {e}")
        return False
    
    # Test queries with rate limit handling
    test_queries = [
        "Who is the principal of KPI?",
        "Tell me about Julekha Akter Koli",
        "What departments are available at KPI?",
        "Who created KPI GPT?",
        "What is the principal's phone number?"
    ]
    
    successful_queries = 0
    
    print(f"\n🧪 Testing {len(test_queries)} queries with rate limit handling...")
    print("⏱️  Adding delays between requests to avoid rate limits...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Add delay between requests to avoid rate limits
            if i > 1:
                print("⏳ Waiting 10 seconds to avoid rate limits...")
                time.sleep(10)
            
            response = rag_system.query(query, max_tokens=200, temperature=0.5)
            
            if response and response.get('answer') and len(response['answer'].strip()) > 10:
                print(f"✅ Success: {response['answer'][:100]}...")
                successful_queries += 1
            else:
                print("❌ Empty or very short response received")
                print(f"Response: {response}")
                
        except Exception as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                print(f"⚠️  Rate limit hit: {e}")
                print("⏳ Waiting 60 seconds before continuing...")
                time.sleep(60)
                # Try once more after waiting
                try:
                    response = rag_system.query(query, max_tokens=200, temperature=0.5)
                    if response and response.get('answer') and len(response['answer'].strip()) > 10:
                        print(f"✅ Success after retry: {response['answer'][:100]}...")
                        successful_queries += 1
                    else:
                        print("❌ Empty response after retry")
                        print(f"Response: {response}")
                except Exception as retry_e:
                    print(f"❌ Failed even after retry: {retry_e}")
            else:
                print(f"❌ Query failed: {e}")
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"✅ Successful queries: {successful_queries}/{len(test_queries)}")
    print(f"📈 Success rate: {(successful_queries/len(test_queries)*100):.1f}%")
    
    if successful_queries >= 3:
        print("\n🎉 API key is working well! System is functional.")
        print("💡 Rate limits are expected with free/basic Groq plans.")
        return True
    else:
        print("\n⚠️  System may have issues or severe rate limiting.")
        return False

def quick_single_test():
    """Run a single quick test to verify the API key works."""
    print("⚡ Quick Single Query Test")
    print("=" * 30)
    
    try:
        rag_system = KPIGPTRagSystem()
        rag_system.setup_system()
        
        response = rag_system.query("Who is the principal?", max_tokens=100, temperature=0.3)
        
        if response and response.get('answer') and len(response['answer'].strip()) > 10:
            print(f"✅ Quick test successful!")
            print(f"📝 Response: {response['answer'][:150]}...")
            return True
        else:
            print("❌ Quick test failed - empty response")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 KPI GPT API Testing Suite")
    print("=" * 40)
    
    # First run a quick test
    if quick_single_test():
        print("\n" + "=" * 40)
        # If quick test passes, run full test suite
        test_api_with_rate_limits()
    else:
        print("\n❌ Quick test failed. Check your API configuration.")
        sys.exit(1)
