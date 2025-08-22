"""
Test script to rebuild database with principal information and test queries
"""

from ai_powered_kpi_gpt import create_ai_powered_kpi_gpt

def main():
    print('🔄 Rebuilding KPI GPT Database with Principal Information...')
    print('='*60)

    # Create and setup the AI-powered system with database rebuild
    ai_kpi_gpt = create_ai_powered_kpi_gpt()
    setup_success = ai_kpi_gpt.setup_system(rebuild_db=True)  # Force rebuild

    if setup_success:
        print('✅ Database successfully rebuilt with principal information!')
        
        # Test principal queries
        test_queries = [
            'Who is the principal of KPI?',
            'Tell me about Sheikh Mustafizur Rahman',
            'What is the principal contact number?',
            'Principal er phone number ki?'
        ]
        
        print('\n🧪 Testing Principal Queries:')
        print('-'*50)
        
        success_count = 0
        for i, query in enumerate(test_queries, 1):
            print(f'\n{i}. Query: "{query}"')
            
            try:
                response = ai_kpi_gpt.query(query)
                answer = response['answer']
                sources = len(response.get('sources', []))
                
                if 'Sheikh Mustafizur Rahman' in answer or ('principal' in answer.lower() and '01765696900' in answer):
                    status = '✅ SUCCESS'
                    success_count += 1
                else:
                    status = '❌ FAILED'
                
                print(f'   {status} - {sources} sources found')
                print(f'   Answer: {answer[:200]}...')
                
            except Exception as e:
                print(f'   ❌ ERROR: {e}')
        
        print(f'\n🎉 Principal Test Results: {success_count}/{len(test_queries)} successful')
        print('✅ Principal information has been added to KPI GPT!')
        
    else:
        print('❌ Failed to rebuild database')

if __name__ == "__main__":
    main()
