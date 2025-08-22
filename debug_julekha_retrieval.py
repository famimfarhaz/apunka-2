#!/usr/bin/env python3
"""
Debug script to see exactly what documents are being retrieved for Julekha queries
and check if her information is actually present in the context sent to Groq.
"""

import logging
from kpi_gpt_rag import KPIGPTRagSystem

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(name)s:%(levelname)s: %(message)s')

def debug_retrieval():
    """Debug what documents are retrieved for Julekha queries"""
    
    print("🔬 Debugging Julekha Retrieval")
    print("=" * 50)
    
    # Initialize system
    kpi_system = KPIGPTRagSystem()
    kpi_system.setup_system()
    
    # Test queries about Julekha
    test_queries = [
        "Who is Julekha Akter Koli?",
        "Julekha Akter Koli information",
        "koli chemistry teacher",
        "Non-Tech Chemistry teacher"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 40)
        
        # Get documents (without generating answer)
        retrieved_docs = kpi_system._retrieve_with_expansion(query)
        
        print(f"📊 Retrieved {len(retrieved_docs)} documents")
        
        # Check each document for Julekha's name
        julekha_found = False
        for i, doc in enumerate(retrieved_docs):
            content = doc.get('content', '').lower()
            score = doc.get('similarity_score', 'N/A')
            
            if 'julekha' in content or 'koli' in content:
                julekha_found = True
                print(f"✅ Document {i+1} (score: {score:.3f}) contains Julekha/Koli:")
                # Show a snippet around the name
                lines = content.split('\n')
                for j, line in enumerate(lines):
                    if 'julekha' in line.lower() or 'koli' in line.lower():
                        start_line = max(0, j-2)
                        end_line = min(len(lines), j+3)
                        print("    Context:")
                        for k in range(start_line, end_line):
                            marker = ">>> " if k == j else "    "
                            print(f"    {marker}{lines[k].strip()}")
                        print()
                        break
            else:
                print(f"❌ Document {i+1} (score: {score:.3f}) - No Julekha/Koli mention")
        
        if not julekha_found:
            print("⚠️  NO documents contain 'Julekha' or 'Koli' in retrieved set!")
            print("\n🔍 Let's see what WAS retrieved:")
            for i, doc in enumerate(retrieved_docs[:3]):  # Show first 3
                content = doc.get('content', '')[:200] + "..."
                score = doc.get('similarity_score', 'N/A')
                print(f"    Doc {i+1} (score: {score:.3f}): {content}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    debug_retrieval()
