#!/usr/bin/env python3
"""
Test script to verify teachers and class captains functionality
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging

# Suppress logs for cleaner output
logging.basicConfig(level=logging.ERROR)

def test_kpi_gpt():
    """Test KPI GPT for teachers and class captains"""
    
    print('🧪 Testing KPI GPT - Teachers and Class Captains')
    print('='*60)
    
    rag = KPIGPTRagSystem()
    success = rag.setup_system()
    
    if not success:
        print('❌ Failed to setup system')
        return
    
    # Test queries
    test_cases = [
        {
            'name': 'Class Captains',
            'query': 'Who are the class captains?',
            'expected_keywords': ['riazul', 'famim', 'abul', 'captain', 'semester']
        },
        {
            'name': 'Civil Teachers',
            'query': 'List civil department teachers',
            'expected_keywords': ['kamruzzaman', 'instructor', 'civil', 'teacher']
        },
        {
            'name': 'Specific Person',
            'query': 'Who is Julekha Akter Koli?',
            'expected_keywords': ['julekha', 'chemistry', 'instructor', 'non-tech']
        },
        {
            'name': 'Famim Farhaz',
            'query': 'Tell me about Famim Farhaz',
            'expected_keywords': ['famim', 'creator', 'civil', 'student']
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f'\n{i}. Testing {test["name"]}:')
        print('-' * 40)
        
        try:
            response = rag.query(test['query'])
            answer = response.get('answer', '')
            sources = response.get('sources', [])
            
            # Check sources
            sections = sorted(set(s['section'] for s in sources))
            print(f'Sources: {len(sources)} from sections: {", ".join(sections)}')
            
            # Check if expected keywords are found
            found_keywords = []
            for keyword in test['expected_keywords']:
                if keyword.lower() in answer.lower():
                    found_keywords.append(keyword)
            
            # Determine success
            success_rate = len(found_keywords) / len(test['expected_keywords'])
            
            if success_rate >= 0.3:  # At least 30% keywords found
                print(f'✅ SUCCESS: Found {len(found_keywords)}/{len(test["expected_keywords"])} keywords')
                print(f'Keywords found: {", ".join(found_keywords)}')
                status = 'PASS'
            else:
                print(f'❌ FAILED: Only {len(found_keywords)}/{len(test["expected_keywords"])} keywords found')
                status = 'FAIL'
            
            print(f'Answer preview: {answer[:150]}...')
            
            results.append({
                'test': test['name'],
                'status': status,
                'keywords_found': len(found_keywords),
                'total_keywords': len(test['expected_keywords']),
                'sections': sections
            })
            
        except Exception as e:
            print(f'❌ ERROR: {e}')
            results.append({
                'test': test['name'],
                'status': 'ERROR',
                'error': str(e)
            })
    
    # Summary
    print('\n' + '='*60)
    print('📊 FINAL RESULTS:')
    print('='*60)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)
    
    for result in results:
        status_icon = '✅' if result['status'] == 'PASS' else '❌'
        print(f"{status_icon} {result['test']}: {result['status']}")
        if 'keywords_found' in result:
            print(f"   Keywords: {result['keywords_found']}/{result['total_keywords']}")
            print(f"   Sections: {', '.join(result['sections'])}")
    
    print(f'\nOverall: {passed}/{total} tests passed ({passed/total*100:.0f}%)')
    
    if passed >= total * 0.75:
        print('🎉 EXCELLENT: Your KPI GPT is working well!')
    elif passed >= total * 0.5:
        print('👍 GOOD: Your KPI GPT is mostly working')
    else:
        print('⚠️  NEEDS WORK: Some issues remain')

if __name__ == "__main__":
    test_kpi_gpt()
