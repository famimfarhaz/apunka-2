"""
AI-Powered KPI GPT System
Natural language understanding without pattern matching
Uses Groq API for intent recognition and semantic retrieval
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import components
from kpi_gpt_rag import KPIGPTRagSystem
from ai_intent_recognizer import AIIntentRecognizer
from semantic_retrieval import SemanticRetrieval
from groq_client import GroqClient

logger = logging.getLogger(__name__)

class AIPoweredKPIGPT(KPIGPTRagSystem):
    """KPI GPT system powered by KPI understanding instead of pattern matching"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # AI components (will be initialized in setup)
        self.intent_recognizer = None
        self.semantic_retrieval = None
        
        logger.info("AI-Powered KPI GPT System initialized")
    
    def setup_system(self, rebuild_db: bool = False) -> bool:
        """Set up the AI-powered RAG system"""
        try:
            # Setup base system first
            if not super().setup_system(rebuild_db):
                return False
            
            # Initialize AI components
            logger.info("Initializing AI-powered components...")
            
            # Create Groq client for intent recognition
            groq_client = GroqClient(model=self.groq_model)
            
            # Initialize intent recognizer
            self.intent_recognizer = AIIntentRecognizer(groq_client)
            
            # Initialize semantic retrieval
            self.semantic_retrieval = SemanticRetrieval(self.vector_db)
            
            logger.info("AI-powered KPI GPT setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up AI-powered system: {e}")
            return False
    
    def query(self, user_query: str, max_tokens: int = 1024, 
              temperature: float = 0.7) -> Dict[str, Any]:
        """Process query using AI-powered natural language understanding"""
        try:
            if not self._is_system_ready() or not self.intent_recognizer:
                raise RuntimeError("AI-powered RAG system is not properly initialized")
            
            logger.info(f"Processing AI-powered query: {user_query}")
            
            # Step 1: AI-powered intent recognition
            logger.info("Analyzing user intent with AI...")
            intent_data = self.intent_recognizer.analyze_intent(user_query)
            
            intent = intent_data.get('intent', '')
            confidence = intent_data.get('confidence', 0)
            entities = intent_data.get('entities', {})
            
            logger.info(f"AI detected intent: {intent} (confidence: {confidence:.2f})")
            logger.info(f"Extracted entities: {entities}")
            
            # Step 2: Handle special intents
            if intent == 'GREETING':
                return self._create_response(
                    answer=self._generate_greeting_response(user_query),
                    sources=[],
                    query=user_query,
                    intent_data=intent_data
                )
            
            elif intent == 'THANKS':
                return self._create_response(
                    answer=self._generate_thanks_response(user_query),
                    sources=[],
                    query=user_query,
                    intent_data=intent_data
                )
            
            # Step 3: AI-powered semantic retrieval
            logger.info("Performing semantic document retrieval...")
            retrieved_docs = self.semantic_retrieval.retrieve_documents(
                intent_data, max_results=self.max_retrieval_results
            )
            
            if not retrieved_docs:
                logger.warning("No relevant documents found through semantic retrieval")
                return self._create_response(
                    answer=self._generate_no_info_response(intent_data),
                    sources=[],
                    query=user_query,
                    intent_data=intent_data,
                    error="No relevant documents found"
                )
            
            # Log retrieval info
            retrieval_info = self.semantic_retrieval.get_retrieval_info(retrieved_docs)
            logger.info(f"Retrieved {retrieval_info['total_results']} documents using methods: {retrieval_info['methods_used']}")
            
            # Step 4: Generate AI response
            logger.info("Generating AI response...")
            answer = self.rag_generator.generate_answer(
                query=user_query,
                retrieved_docs=retrieved_docs,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Step 5: Post-process response
            processed_answer = self._post_process_response(answer['answer'], intent_data)
            
            # Step 6: Create enhanced response
            return self._create_response(
                answer=processed_answer,
                sources=answer.get('sources', []),
                query=user_query,
                intent_data=intent_data,
                retrieval_info=retrieval_info
            )
            
        except Exception as e:
            logger.error(f"Error processing AI-powered query: {e}")
            return self._create_response(
                answer=f"আমি আপনার প্রশ্ন বুঝতে সমস্যা হচ্ছে। দয়া করে আবার চেষ্টা করুন। Error: {str(e)}",
                sources=[],
                query=user_query,
                error=str(e)
            )
    
    def _generate_greeting_response(self, query: str) -> str:
        """Generate natural greeting response"""
        greetings = [
            "আসসালামু আলাইকুম! আমি KPI GPT, খুলনা পলিটেকনিক ইনস্টিটিউটের AI সহায়ক। আপনাকে কীভাবে সাহায্য করতে পারি?",
            "হ্যালো! আমি KPI GPT। খুলনা পলিটেকনিক সম্পর্কে যেকোনো প্রশ্ন আমাকে করতে পারেন।",
            "নমস্কার! আমি KPI এর তথ্য সহায়ক। শিক্ষক, বিভাগ, বা অন্য যেকোনো বিষয়ে জানতে চাইলে বলুন।"
        ]
        return greetings[hash(query) % len(greetings)]
    
    def _generate_thanks_response(self, query: str) -> str:
        """Generate natural thanks response"""
        responses = [
            "আপনাকে ধন্যবাদ! KPI সম্পর্কে আরো কিছু জানতে চাইলে বলুন।",
            "স্বাগতম! আরো কোনো প্রশ্ন থাকলে জিজ্ঞেস করুন।",
            "খুশি হলাম সাহায্য করতে পেরে! আরো কিছু জানতে চান?"
        ]
        return responses[hash(query) % len(responses)]
    
    def _generate_no_info_response(self, intent_data: Dict[str, Any]) -> str:
        """Generate appropriate response when no information is found"""
        intent = intent_data.get('intent', '')
        entities = intent_data.get('entities', {})
        person_name = entities.get('person_name')
        
        if intent == 'PERSON_INFO' and person_name:
            return f"দুঃখিত, আমার কাছে '{person_name}' সম্পর্কে কোনো তথ্য নেই। অন্য কোনো শিক্ষক বা কর্মকর্তার নাম দিয়ে চেষ্টা করুন।"
        
        elif intent == 'DEPARTMENT_INFO':
            return "আমি সেই বিভাগের তথ্য খুঁজে পাইনি। দয়া করে সিভিল, ইলেকট্রিক্যাল, মেকানিক্যাল - এভাবে বিভাগের নাম দিয়ে চেষ্টা করুন।"
        
        return "দুঃখিত, আমি আপনার প্রশ্নের উত্তর খুঁজে পাইনি। অন্যভাবে প্রশ্ন করে চেষ্টা করুন।"
    
    def _post_process_response(self, answer: str, intent_data: Dict[str, Any]) -> str:
        """Post-process the AI response to make it more natural"""
        # Remove overly formal AI phrases
        processed = answer
        
        # Make it more conversational based on intent
        intent = intent_data.get('intent', '')
        
        if intent == 'PERSON_INFO':
            # Add natural intro for person info
            if not processed.startswith(('তিনি', 'এই ব্যক্তি', 'উনি')):
                entities = intent_data.get('entities', {})
                person_name = entities.get('person_name', '')
                if person_name and person_name.lower() not in processed.lower()[:50]:
                    processed = f"{person_name} সম্পর্কে বলতে পারি - {processed}"
        
        return processed
    
    def _create_response(self, answer: str, sources: List[Dict], query: str, 
                        intent_data: Dict = None, retrieval_info: Dict = None, 
                        error: str = None) -> Dict[str, Any]:
        """Create structured response"""
        response = {
            'query': query,
            'answer': answer,
            'sources': sources,
            'timestamp': datetime.now().isoformat()
        }
        
        if intent_data:
            response['ai_analysis'] = {
                'intent': intent_data.get('intent'),
                'confidence': intent_data.get('confidence'),
                'entities': intent_data.get('entities'),
                'query_type': intent_data.get('query_type')
            }
        
        if retrieval_info:
            response['retrieval_info'] = retrieval_info
        
        if error:
            response['error'] = error
        
        # Add system info
        response['system_info'] = {
            'powered_by': 'AI Understanding',
            'method': 'Semantic Retrieval',
            'database_docs': self.vector_db.get_collection_info().get('document_count', 0),
            'embedding_model': self.embedding_model,
            'generation_model': self.groq_model
        }
        
        return response
    
    def chat(self, user_query: str) -> str:
        """Simple chat interface returning just the answer"""
        response = self.query(user_query)
        return response['answer']
    
    def get_ai_analysis(self, user_query: str) -> Dict[str, Any]:
        """Get AI analysis of a query without full processing"""
        if not self.intent_recognizer:
            return {'error': 'AI intent recognizer not initialized'}
        
        return self.intent_recognizer.analyze_intent(user_query)


def create_ai_powered_kpi_gpt(**kwargs) -> AIPoweredKPIGPT:
    """Factory function to create AI-powered KPI GPT system"""
    
    # Get configuration from environment variables
    config = {
        'data_file': kwargs.get('data_file', os.getenv('DATA_FILE', 'kpi_data.txt')),
        'db_path': kwargs.get('db_path', os.getenv('VECTOR_DB_PATH', './vector_db')),
        'embedding_model': kwargs.get('embedding_model', os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')),
        'groq_model': kwargs.get('groq_model', os.getenv('GROQ_MODEL', 'llama3-8b-8192')),
        'chunk_size': kwargs.get('chunk_size', int(os.getenv('CHUNK_SIZE', '1000'))),
        'chunk_overlap': kwargs.get('chunk_overlap', int(os.getenv('CHUNK_OVERLAP', '200'))),
        'max_retrieval_results': kwargs.get('max_retrieval_results', int(os.getenv('MAX_RETRIEVAL_RESULTS', '5')))
    }
    
    return AIPoweredKPIGPT(**config)


def main():
    """Main function for testing the AI-powered KPI GPT system"""
    print("🤖 Initializing AI-Powered KPI GPT System...")
    print("=" * 60)
    
    # Create and setup AI-powered RAG system
    rag_system = create_ai_powered_kpi_gpt()
    
    print("📚 Setting up AI-powered system components...")
    setup_success = rag_system.setup_system()
    
    if not setup_success:
        print("❌ Failed to setup AI-powered RAG system")
        return
    
    print("✅ AI-Powered KPI GPT setup completed!")
    print("🧠 AI Understanding: Enabled")
    print("🔍 Semantic Retrieval: Enabled")
    print("❌ Pattern Matching: Disabled")
    
    # Show system info
    system_info = rag_system.get_system_info()
    print(f"📊 System Info:")
    print(f"   - Database documents: {system_info['database']['document_count']}")
    print(f"   - AI Model: {system_info['models']['generation']}")
    
    print("\n" + "=" * 60)
    print("💬 AI-Powered KPI GPT is ready! Try natural queries:")
    print("   - 'Md. Al-Emran er information deo'")
    print("   - 'civil department e kara kara teacher ache?'")
    print("   - 'oi teacher er phone number ki?'")
    print("   - 'KPI te computer department ache?'")
    print("   Type 'quit' to exit")
    print("=" * 60 + "\n")
    
    # Interactive query loop
    while True:
        try:
            user_input = input("🤔 আপনার প্রশ্ন: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'বের হও', 'বাই']:
                print("👋 ধন্যবাদ! আবার আসবেন।")
                break
            elif not user_input:
                continue
            
            print("🤖 KPI GPT:", end=" ", flush=True)
            
            # Process query with AI
            response = rag_system.query(user_input)
            
            # Display the answer
            print(response['answer'])
            
            # Show AI analysis info
            if 'ai_analysis' in response:
                ai_info = response['ai_analysis']
                print(f"🧠 AI Analysis: {ai_info['intent']} (confidence: {ai_info['confidence']:.2f})")
            
            # Show sources if available
            if response.get('sources'):
                print(f"📚 Sources: {len(response['sources'])} documents found")
            
            print("\n" + "-" * 40 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 বিদায়!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
