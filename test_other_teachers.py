#!/usr/bin/env python3
"""
Test script to check multiple teacher queries
"""

from kpi_gpt_rag import KPIGPTRagSystem
import logging

logging.basicConfig(level=logging.ERROR)

def test_multiple_teachers():
    """Test queries for different teachers"""
    
    print('🧪 Testing Multiple Teacher Queries')
    print('='*60)
    
    rag = KPIGPTRagSystem()
    success = rag.setup_system()
    
    if not success:
        print('❌ Failed to setup system')
        return
    
    # Test different teacher names from the database
    teacher_queries = [
        "Who is S.M. Kamruzzaman?",
        "Who is Susmita Kundu?",
        "Who is Alok Sarkar?", 
        "Who is Subrata Saha?",
        "Who is Mina Md. Bulbul Jahan?",
        "Who is Md. Yasir Arafat?",
        "Who is Shariful Islam?",
        "Who is Dipak Kumar Mondal?",
        "Who is Liakat Hossain?",
        "Who is Md. Nazmul Hossain?"
    ]
    
    results = []
    
    for i, query in enumerate(teacher_queries, 1):
        print(f'\n{i}. Testing: {query}')
        print('-' * 40)
        
        try:
            response = rag.query(query)
            answer = response.get('answer', '')
            sources = response.get('sources', [])
            sections = sorted(set(s['section'] for s in sources))
            
            print(f'Sources: {len(sources)} from sections: {", ".join(sections)}')
            
            # Extract the name from query to check if found
            name_parts = query.replace('Who is', '').replace('?', '').strip().split()
            
            # Check if teacher was found
            found_name_parts = []
            for part in name_parts:
                if part.lower() in answer.lower():
                    found_name_parts.append(part)
            
            if len(found_name_parts) >= 2:  # Found at least 2 name parts
                status = '✅ SUCCESS'
                print(f'{status}: Found teacher information')
                results.append('SUCCESS')
            elif len(found_name_parts) >= 1:
                status = '⚠️  PARTIAL'
                print(f'{status}: Found some information')
                results.append('PARTIAL')
            else:
                status = '❌ FAILED'
                print(f'{status}: Teacher not found')
                results.append('FAILED')
            
            print(f'Answer preview: {answer[:150]}...')
            
        except Exception as e:
            print(f'❌ ERROR: {e}')
            results.append('ERROR')
    
    # Summary
    print('\n' + '='*60)
    print('📊 RESULTS SUMMARY:')
    print('='*60)
    
    success_count = results.count('SUCCESS')
    partial_count = results.count('PARTIAL')
    failed_count = results.count('FAILED')
    error_count = results.count('ERROR')
    total = len(results)
    
    print(f'✅ SUCCESS: {success_count}/{total} ({success_count/total*100:.0f}%)')
    print(f'⚠️  PARTIAL: {partial_count}/{total} ({partial_count/total*100:.0f}%)')
    print(f'❌ FAILED:  {failed_count}/{total} ({failed_count/total*100:.0f}%)')
    print(f'🔥 ERROR:   {error_count}/{total} ({error_count/total*100:.0f}%)')
    
    if success_count + partial_count >= total * 0.7:
        print('\n🎉 GOOD: Most teacher queries are working!')
    elif success_count + partial_count >= total * 0.5:
        print('\n👍 OK: Some teacher queries need improvement')
    else:
        print('\n⚠️  NEEDS WORK: Many teacher queries are failing')

if __name__ == "__main__":
    test_multiple_teachers()
