"""
Test script for AI-powered KPI GPT natural language understanding
"""

import logging
logging.basicConfig(level=logging.ERROR)

from ai_powered_kpi_gpt import create_ai_powered_kpi_gpt

def main():
    print('🧪 Testing AI-Powered KPI GPT (No Pattern Matching)')
    print('='*60)

    # Create and setup the system
    ai_kpi_gpt = create_ai_powered_kpi_gpt()
    setup_success = ai_kpi_gpt.setup_system()

    if not setup_success:
        print('❌ Failed to setup AI system')
        return

    print('✅ AI System setup complete!')
    print('🧠 AI Understanding: Enabled')
    print('❌ Pattern Matching: Disabled')
    print()

    # Test natural language queries (the ones that failed before)
    test_queries = [
        # The original failing queries
        'did you have any information about Md. Al-Emran?',
        'Md. Al-Emran er information deo',
        'tell me something about this teacher',
        'KPI te kon kon teacher ache?',
        'civil department er teachers der nam bolo'
    ]

    print('🎯 Testing Natural Language Understanding:')
    print('-'*50)

    success_count = 0
    for i, query in enumerate(test_queries, 1):
        print(f'\n{i}. Query: "{query}"')
        
        try:
            # Get AI analysis first
            ai_analysis = ai_kpi_gpt.get_ai_analysis(query)
            intent = ai_analysis.get('intent', 'UNKNOWN')
            confidence = ai_analysis.get('confidence', 0)
            entities = ai_analysis.get('entities', {})
            
            print(f'   🧠 AI Analysis: {intent} (confidence: {confidence:.2f})')
            print(f'   📋 Entities: {entities}')
            
            # Process the full query
            response = ai_kpi_gpt.query(query)
            answer = response['answer']
            sources = response.get('sources', [])
            
            # Check success
            if 'error' in response or 'কোনো তথ্য নেই' in answer or 'no information' in answer.lower():
                status = '❌ NO INFO'
            elif len(answer) > 50 and len(sources) > 0:
                status = '✅ SUCCESS'
                success_count += 1
            else:
                status = '⚠️  PARTIAL'
            
            print(f'   {status} - {len(sources)} sources found')
            print(f'   💬 Answer: {answer[:150]}...')
            
        except Exception as e:
            print(f'   ❌ ERROR: {e}')

    print(f'\n🎉 AI-Powered KPI GPT Results: {success_count}/{len(test_queries)} successful')
    
    # Test specific case that was failing
    print('\n🔍 Testing the original failing case:')
    print('-'*40)
    
    failing_query = "did you have any information about Md. Al-Emran"
    print(f'Query: "{failing_query}"')
    
    try:
        response = ai_kpi_gpt.query(failing_query)
        print(f'Answer: {response["answer"]}')
        
        if 'ai_analysis' in response:
            ai_info = response['ai_analysis']
            print(f'AI Intent: {ai_info["intent"]} (confidence: {ai_info["confidence"]:.2f})')
            print(f'Entities: {ai_info["entities"]}')
        
        if response.get('sources'):
            print(f'Sources found: {len(response["sources"])}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
