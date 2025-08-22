#!/usr/bin/env python3
"""
Debug script to test teacher and class captain queries
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging

# Suppress INFO logs to focus on results
logging.basicConfig(level=logging.ERROR)

def test_specific_queries():
    """Test specific queries that are reported as not working"""
    
    rag = KPIGPTRagSystem()
    rag.setup_system()

    queries = [
        "Who is Julekha Akter Koli?",
        "Tell me about Julekha Akter Koli",
        "Who is Famim Farhaz?", 
        "Tell me about Famim Farhaz",
        "List all teachers in Civil department",
        "Who are the class captains?",
        "Give me information about class captains",
        "Tell me about Civil department teachers",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*50}")
        print(f"Query {i}: {query}")
        print(f"{'='*50}")
        
        response = rag.query(query)
        
        print(f"Answer: {response['answer'][:300]}...")
        print(f"Sources found: {len(response.get('sources', []))}")
        
        if response.get('sources'):
            print("Source sections:")
            for source in response['sources'][:3]:  # Show first 3 sources
                print(f"  - {source.get('metadata', {}).get('section', 'Unknown')}")

if __name__ == "__main__":
    test_specific_queries()
