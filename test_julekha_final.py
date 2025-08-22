#!/usr/bin/env python3
"""
Final test for Julekha query
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging

logging.basicConfig(level=logging.ERROR)

def test_julekha():
    """Test the improved Julekha query"""
    
    print('🧪 Testing Improved Julekha Query')
    print('='*50)
    
    rag = KPIGPTRagSystem()
    success = rag.setup_system()
    
    if not success:
        print('❌ Failed to setup system')
        return
    
    r = rag.query('Who is Julekha Akter Koli?')
    sources = r.get('sources', [])
    sections = sorted(set(s['section'] for s in sources))
    
    print(f'Sources: {len(sources)} from sections: {", ".join(sections)}')
    
    answer = r.get('answer', '')
    
    if 'julekha' in answer.lower() and 'chemistry' in answer.lower():
        print('✅ SUCCESS: Found Julekha Akter Koli!')
        print(f'Answer: {answer[:300]}...')
    elif 'julekha' in answer.lower():
        print('✅ PARTIAL: Found Julekha but missing details')
        print(f'Answer: {answer[:300]}...')
    else:
        print('❌ FAILED: Still not finding Julekha')
        print(f'Answer: {answer[:300]}...')

if __name__ == "__main__":
    test_julekha()
