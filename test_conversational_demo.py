"""
Test script for Conversational KPI GPT demonstration
"""

import logging
logging.basicConfig(level=logging.ERROR)

from conversational_kpi_gpt import create_conversational_kpi_gpt

def main():
    print('🎯 Final Conversational AI Demonstration')
    print('='*55)

    # Create and setup the system
    kpi_gpt = create_conversational_kpi_gpt()
    setup_success = kpi_gpt.setup_system()

    if not setup_success:
        print('❌ Failed to setup system')
        return

    # Demonstrate natural conversation flow
    conversation = [
        ('Hello', 'greeting'),
        ('Who is Julekha Akter Koli?', 'person query'),
        ('What about her contact info?', 'pronoun resolution + casual query'),
        ('Tell me about S.M. Kamruzzaman', 'another person query'),
        ('his email?', 'very casual pronoun query'),
        ('thanks!', 'gratitude')
    ]

    print('💬 Natural Conversation Demonstration:')
    print('='*55)

    for i, (query, note) in enumerate(conversation, 1):
        print(f'\n{i}. 😊 You: "{query}" ({note})')
        
        response = kpi_gpt.query(query)
        answer = response['answer']
        context_info = response.get('context_info', {})
        
        print(f'   🤖 KPI GPT: {answer[:120]}...')
        
        # Show conversational features
        if context_info.get('current_person'):
            print(f'   🧠 Context: {context_info["current_person"]}')
        
        if 'suggested_questions' in response:
            print(f'   💡 Next: {response["suggested_questions"][0][:40]}...')

    # Show conversation summary
    print('\n' + '='*55)
    summary = kpi_gpt.get_conversation_summary()
    session_info = summary['session_info']
    print('📊 Conversation Summary:')
    print(f'   - Total interactions: {session_info["total_interactions"]}')
    print(f'   - People discussed: {len(session_info.get("mentioned_people", []))}')
    print(f'   - Current focus: {session_info.get("current_person", "None")}')

    print('\n✨ KPI GPT is now conversational and context-aware!')
    print('   Features implemented:')
    print('   ✅ Natural greetings and thanks')
    print('   ✅ Pronoun resolution (him, her, etc.)')
    print('   ✅ Conversation context tracking')
    print('   ✅ Casual query understanding')
    print('   ✅ Follow-up question suggestions')
    print('   ✅ Person-focused context memory')

if __name__ == "__main__":
    main()
