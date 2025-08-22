"""
Conversational KPI GPT RAG System
Enhanced version with natural language processing and context awareness
Created by: Famim Farhaz
"""

import os
import sys
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Import the original system
from kpi_gpt_rag import KPIGPTRagSystem
from conversation_context import ConversationContext
from natural_language_processor import NaturalLanguageProcessor

logger = logging.getLogger(__name__)

class ConversationalKPIGPT(KPIGPTRagSystem):
    """Enhanced KPI GPT RAG System with conversational AI capabilities"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add conversational components
        self.conversation_context = ConversationContext()
        self.nlp_processor = NaturalLanguageProcessor()
        
        logger.info("Conversational KPI GPT System initialized")
    
    def query(self, user_query: str, max_tokens: int = 1024, 
              temperature: float = 0.7) -> Dict[str, Any]:
        """Enhanced query processing with conversational AI"""
        try:
            if not self._is_system_ready():
                raise RuntimeError("RAG system is not properly initialized")
            
            original_query = user_query
            logger.info(f"Processing conversational query: {user_query}")
            
            # Step 1: Detect query type
            query_type = self.nlp_processor.detect_query_type(user_query)
            logger.info(f"Detected query type: {query_type}")
            
            # Step 2: Handle special query types
            if query_type == 'greeting':
                response = self._handle_greeting()
                return self._format_conversational_response(response, [], original_query)
            elif query_type == 'thanks':
                response = self._handle_thanks()
                return self._format_conversational_response(response, [], original_query)
            
            # Step 3: Enhance query with conversation context
            enhanced_query = self.conversation_context.enhance_query_with_context(user_query)
            if enhanced_query != user_query:
                logger.info(f"Enhanced query with context: '{user_query}' -> '{enhanced_query}'")
                user_query = enhanced_query
            
            # Step 4: Transform casual queries to more structured format
            if self.nlp_processor.is_conversational_query(user_query):
                transformed_query = self.nlp_processor.transform_casual_query(user_query)
                if transformed_query != user_query:
                    logger.info(f"Transformed casual query: '{user_query}' -> '{transformed_query}'")
                    user_query = transformed_query
            
            # Step 5: Process query using parent class method
            response = super().query(user_query, max_tokens, temperature)
            
            # Step 6: Enhance response with conversational features
            enhanced_answer = self.nlp_processor.make_response_conversational(
                response['answer'], original_query
            )
            
            # Step 7: Add interaction to conversation history
            sources = response.get('sources', [])
            self.conversation_context.add_interaction(original_query, enhanced_answer, sources)
            
            # Step 8: Format final response with conversational features
            return self._format_conversational_response(enhanced_answer, sources, original_query, response)
            
        except Exception as e:
            logger.error(f"Error processing conversational query: {e}")
            error_response = f"Sorry, I encountered an error while processing your query: {str(e)}"
            return self._format_conversational_response(error_response, [], original_query)
    
    def _handle_greeting(self) -> str:
        """Handle greeting queries"""
        greetings = [
            "Hello! I'm KPI GPT, your AI assistant for Khulna Polytechnic Institute.",
            "Hi there! I'm here to help you with any questions about KPI.",
            "Hey! I'm KPI GPT. What would you like to know about Khulna Polytechnic Institute?"
        ]
        
        # Vary response based on conversation history
        interaction_count = len(self.conversation_context.conversation_history)
        if interaction_count == 0:
            return f"{greetings[0]} How can I help you today?"
        else:
            return f"{greetings[1]} What else can I help you with?"
    
    def _handle_thanks(self) -> str:
        """Handle thank you queries"""
        responses = [
            "You're welcome! Feel free to ask me anything else about KPI.",
            "Happy to help! Is there anything else you'd like to know?",
            "Glad I could help! Any other questions about teachers, departments, or KPI?"
        ]
        
        # Choose response based on context
        if self.conversation_context.current_person_context:
            return f"{responses[0]} Want to know more about {self.conversation_context.current_person_context} or someone else?"
        else:
            return responses[1]
    
    def _format_conversational_response(self, answer: str, sources: List[Dict], 
                                      original_query: str, base_response: Dict = None) -> Dict[str, Any]:
        """Format response with conversational features"""
        response = {
            'query': original_query,
            'answer': answer,
            'sources': sources,
            'timestamp': datetime.now().isoformat(),
            'conversation_id': id(self.conversation_context)
        }
        
        # Add base response metadata if available
        if base_response:
            response.update({k: v for k, v in base_response.items() 
                           if k not in ['query', 'answer', 'sources', 'timestamp']})
        
        # Add conversational features
        if len(sources) > 0 and 'no information' not in answer.lower():
            suggestions = self.nlp_processor.suggest_followup_questions(original_query, answer)
            if suggestions:
                response['suggested_questions'] = suggestions
        
        # Add context information
        response['context_info'] = {
            'current_person': self.conversation_context.current_person_context,
            'conversation_turns': len(self.conversation_context.conversation_history),
            'mentioned_people': len(self.conversation_context.mentioned_people)
        }
        
        return response
    
    def chat(self, user_query: str) -> str:
        """Simple chat interface that returns just the answer"""
        response = self.query(user_query)
        return response['answer']
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation"""
        return {
            'session_info': self.conversation_context.get_context_summary(),
            'system_info': self.get_system_info(),
            'last_interaction': (
                self.conversation_context.conversation_history[-1] 
                if self.conversation_context.conversation_history else None
            )
        }
    
    def clear_conversation(self):
        """Clear conversation history and start fresh"""
        self.conversation_context.clear_context()
        logger.info("Conversation context cleared")
    
    def set_context_person(self, person_name: str):
        """Manually set the current person context"""
        self.conversation_context.current_person_context = person_name
        logger.info(f"Manually set context person to: {person_name}")


def create_conversational_kpi_gpt(**kwargs) -> ConversationalKPIGPT:
    """Factory function to create Conversational KPI GPT system"""
    
    # Get configuration from environment variables (same as base system)
    config = {
        'data_file': kwargs.get('data_file', os.getenv('DATA_FILE', 'kpi_data.txt')),
        'db_path': kwargs.get('db_path', os.getenv('VECTOR_DB_PATH', './vector_db')),
        'embedding_model': kwargs.get('embedding_model', os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')),
        'groq_model': kwargs.get('groq_model', os.getenv('GROQ_MODEL', 'llama3-8b-8192')),
        'chunk_size': kwargs.get('chunk_size', int(os.getenv('CHUNK_SIZE', '1000'))),
        'chunk_overlap': kwargs.get('chunk_overlap', int(os.getenv('CHUNK_OVERLAP', '200'))),
        'max_retrieval_results': kwargs.get('max_retrieval_results', int(os.getenv('MAX_RETRIEVAL_RESULTS', '5')))
    }
    
    return ConversationalKPIGPT(**config)


def main():
    """Main function for testing the Conversational KPI GPT system"""
    print("🚀 Initializing Conversational KPI GPT System...")
    print("==" * 30)
    
    # Create and setup conversational RAG system
    rag_system = create_conversational_kpi_gpt()
    
    print("📚 Setting up system components...")
    setup_success = rag_system.setup_system()
    
    if not setup_success:
        print("❌ Failed to setup conversational RAG system")
        return
    
    print("✅ Conversational KPI GPT setup completed!")
    
    # Show system info
    system_info = rag_system.get_system_info()
    print(f"📊 System Info:")
    print(f"   - Database documents: {system_info['database']['document_count']}")
    print(f"   - Embedding model: {system_info['models']['embedding']}")
    print(f"   - Generation model: {system_info['models']['generation']}")
    print(f"   - Conversational AI: ✅ Enabled")
    
    print("\n" + "==" * 30)
    print("💬 Conversational KPI GPT is ready!")
    print("   Try natural queries like:")
    print("   - 'Hi' or 'Hello'")
    print("   - 'Who is Julekha Akter Koli?'")
    print("   - 'Tell me about him' (after asking about someone)")
    print("   - 'What's her contact info?' (follow-up question)")
    print("   Type 'quit' to exit, 'clear' to clear conversation, 'summary' for conversation summary")
    print("==" * 30 + "\n")
    
    # Interactive conversational loop
    while True:
        try:
            user_input = input("😊 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thanks for using KPI GPT!")
                break
            elif user_input.lower() == 'clear':
                rag_system.clear_conversation()
                print("🔄 Conversation cleared. Starting fresh!")
                continue
            elif user_input.lower() == 'summary':
                summary = rag_system.get_conversation_summary()
                session_info = summary['session_info']
                print(f"📊 Conversation Summary:")
                print(f"   - Turns: {session_info['total_interactions']}")
                print(f"   - Current person: {session_info.get('current_person', 'None')}")
                print(f"   - People mentioned: {len(session_info.get('mentioned_people', []))}")
                continue
            elif not user_input:
                continue
            
            print("🤖 KPI GPT:", end=" ", flush=True)
            
            # Process query and get response
            response = rag_system.query(user_input)
            
            # Display the answer
            print(response['answer'])
            
            # Show suggested questions if available
            if 'suggested_questions' in response:
                print(f"\n💡 You might also ask:")
                for i, suggestion in enumerate(response['suggested_questions'], 1):
                    print(f"   {i}. {suggestion}")
            
            # Show context info if debugging
            context_info = response.get('context_info', {})
            if context_info.get('current_person'):
                print(f"🎯 Currently discussing: {context_info['current_person']}")
            
            print("\n" + "--" * 20 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
