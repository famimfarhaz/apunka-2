"""
KPI GPT RAG (Retrieval-Augmented Generation) System
Created by: Famim Farhaz

Main application that combines all components to create a complete RAG system
for Khulna Polytechnic Institute information retrieval and generation.
"""

import os
import sys
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv

# Import custom modules
from data_preprocessor import KPIDataProcessor
from vector_database import VectorDatabase
from groq_client import GroqClient, RAGGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kpi_gpt_rag.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class KPIGPTRagSystem:
    """Complete KPI GPT RAG System"""
    
    def __init__(self, 
                 data_file: str = "kpi_data.txt",
                 db_path: str = "./vector_db",
                 embedding_model: str = "all-MiniLM-L6-v2",
                 groq_model: str = "llama3-8b-8192",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 max_retrieval_results: int = 8):  # Increased for better coverage
        
        self.data_file = data_file
        self.db_path = db_path
        self.embedding_model = embedding_model
        self.groq_model = groq_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_retrieval_results = max_retrieval_results
        
        # Initialize components
        self.processor = None
        self.vector_db = None
        self.rag_generator = None
        
        logger.info("KPI GPT RAG System initialized")
    
    def setup_system(self, rebuild_db: bool = False) -> bool:
        """Set up the complete RAG system"""
        try:
            logger.info("Setting up KPI GPT RAG System...")
            
            # Initialize data processor
            logger.info("Initializing data processor...")
            self.processor = KPIDataProcessor(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            
            # Initialize vector database
            logger.info("Initializing vector database...")
            self.vector_db = VectorDatabase(
                db_path=self.db_path,
                embedding_model=self.embedding_model
            )
            
            # Check if database needs to be populated
            db_info = self.vector_db.get_collection_info()
            if db_info.get('document_count', 0) == 0 or rebuild_db:
                logger.info("Populating vector database with KPI data...")
                success = self._populate_database()
                if not success:
                    logger.error("Failed to populate database")
                    return False
            else:
                logger.info(f"Using existing database with {db_info['document_count']} documents")
            
            # Initialize RAG generator
            logger.info("Initializing RAG generator...")
            groq_client = GroqClient(model=self.groq_model)
            self.rag_generator = RAGGenerator(groq_client)
            
            logger.info("KPI GPT RAG System setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up RAG system: {e}")
            return False
    
    def _populate_database(self) -> bool:
        """Populate vector database with processed KPI data"""
        try:
            # Check if data file exists
            if not os.path.exists(self.data_file):
                logger.error(f"Data file not found: {self.data_file}")
                return False
            
            # Process KPI data
            chunks = self.processor.process_file(self.data_file)
            
            if not chunks:
                logger.error("No chunks created from data file")
                return False
            
            # Add to vector database
            success = self.vector_db.add_documents(chunks)
            return success
            
        except Exception as e:
            logger.error(f"Error populating database: {e}")
            return False
    
    def query(self, user_query: str, max_tokens: int = 1024, 
              temperature: float = 0.7) -> Dict[str, Any]:
        """Process user query and generate response"""
        try:
            if not self._is_system_ready():
                raise RuntimeError("RAG system is not properly initialized")
            
            logger.info(f"Processing query: {user_query}")
            
            # Retrieve relevant documents with query expansion
            logger.info("Retrieving relevant documents...")
            retrieved_docs = self._retrieve_with_expansion(user_query)
            
            if not retrieved_docs:
                logger.warning("No relevant documents found")
                return {
                    'query': user_query,
                    'answer': "I couldn't find relevant information to answer your query about KPI. Please try rephrasing your question.",
                    'sources': [],
                    'error': 'No relevant documents found'
                }
            
            # Generate answer using RAG
            logger.info("Generating answer...")
            response = self.rag_generator.generate_answer(
                query=user_query,
                retrieved_docs=retrieved_docs,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Add system metadata
            response['system_info'] = {
                'database_docs': self.vector_db.get_collection_info().get('document_count', 0),
                'retrieval_results': len(retrieved_docs),
                'embedding_model': self.embedding_model,
                'generation_model': self.groq_model
            }
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'query': user_query,
                'answer': f"Sorry, I encountered an error while processing your query: {str(e)}",
                'sources': [],
                'error': str(e)
            }
    
    def stream_query(self, user_query: str, max_tokens: int = 1024, 
                     temperature: float = 0.7):
        """Process user query and generate streaming response"""
        try:
            if not self._is_system_ready():
                raise RuntimeError("RAG system is not properly initialized")
            
            logger.info(f"Processing streaming query: {user_query}")
            
            # Retrieve relevant documents
            retrieved_docs = self.vector_db.search_similar(
                query=user_query,
                n_results=self.max_retrieval_results,
                where=self._section_filter_for_query(user_query)
            )
            
            if not retrieved_docs:
                yield "I couldn't find relevant information to answer your query about KPI. Please try rephrasing your question."
                return
            
            # Generate streaming answer
            for chunk in self.rag_generator.generate_stream_answer(
                query=user_query,
                retrieved_docs=retrieved_docs,
                max_tokens=max_tokens,
                temperature=temperature
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error processing streaming query: {e}")
            yield f"Sorry, I encountered an error: {str(e)}"
    
    def _section_filter_for_query(self, query: str) -> Optional[Dict[str, Any]]:
        """NO FILTERING - Let Groq handle all queries without restrictions"""
        # Removed all keyword-based filtering to let Groq handle everything
        return None

    def _retrieve_with_expansion(self, user_query: str) -> List[Dict[str, Any]]:
        """Smart universal retrieval - works for any query without restrictions"""
        try:
            logger.info(f"Retrieving documents for: '{user_query}'")
            
            all_results = []
            seen_content = set()
            
            # Primary search - Direct semantic search
            logger.info("Performing primary semantic search...")
            primary_results = self.vector_db.search_similar(
                query=user_query,
                n_results=self.max_retrieval_results * 2,  # Get more initially
                where=None  # No filtering!
            )
            
            # Add primary results
            for result in primary_results:
                content_hash = hash(result['content'])
                if content_hash not in seen_content:
                    result['search_method'] = 'primary_semantic'
                    all_results.append(result)
                    seen_content.add(content_hash)
            
            # Secondary searches - Individual query words
            query_words = [word.strip() for word in user_query.replace('?', '').split() 
                          if len(word.strip()) > 2 and word.strip().lower() not in 
                          ['who', 'what', 'when', 'where', 'how', 'tell', 'about', 'the', 'and', 'or']]
            
            logger.info(f"Trying individual word searches for: {query_words[:4]}")
            for word in query_words[:4]:  # Try first 4 meaningful words
                try:
                    word_results = self.vector_db.search_similar(
                        query=word,
                        n_results=4,
                        where=None
                    )
                    
                    for result in word_results:
                        content_hash = hash(result['content'])
                        if content_hash not in seen_content:
                            result['search_method'] = f'word_search_{word}'
                            all_results.append(result)
                            seen_content.add(content_hash)
                            
                except Exception as e:
                    logger.debug(f"Word search failed for '{word}': {e}")
                    continue
            
            # If we still don't have enough results, try broader searches
            if len(all_results) < 5:
                logger.info("Expanding search with broader terms...")
                broad_searches = [
                    "instructor teacher",
                    "staff member", 
                    "department faculty",
                    "contact information",
                    "chemistry physics",
                    "non-tech"
                ]
                
                for broad_term in broad_searches:
                    try:
                        broad_results = self.vector_db.search_similar(
                            query=broad_term,
                            n_results=2,
                            where=None
                        )
                        
                        for result in broad_results:
                            content_hash = hash(result['content'])
                            if content_hash not in seen_content:
                                result['search_method'] = f'broad_search_{broad_term.replace(" ", "_")}'
                                all_results.append(result)
                                seen_content.add(content_hash)
                                
                    except Exception as e:
                        logger.debug(f"Broad search failed for '{broad_term}': {e}")
                        continue
            
            # Sort by similarity score (higher is better)
            all_results.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            
            # Return top results - give Groq plenty of context
            final_results = all_results[:self.max_retrieval_results * 3]  # More context for Groq
            
            if final_results:
                scores_str = ', '.join([f"{r.get('similarity_score', 0):.3f}" for r in final_results[:5]])
                logger.info(f"Retrieved {len(final_results)} documents with similarity scores: [{scores_str}]")
            else:
                logger.warning("No documents retrieved!")
            
            return final_results
            
        except Exception as e:
            logger.error(f"Error in retrieval: {e}")
            # Fallback to simple search
            try:
                return self.vector_db.search_similar(
                    query=user_query,
                    n_results=self.max_retrieval_results,
                    where=None
                )
            except Exception as fallback_error:
                logger.error(f"Fallback search also failed: {fallback_error}")
                return []
    
    def _is_person_query(self, query: str) -> bool:
        """Check if query looks like it's asking about a person"""
        query_lower = query.lower()
        person_indicators = [
            'who is', 'tell me about', 'information about',
            'contact', 'details about', 'about'
        ]
        
        # Check if query has person indicators
        has_indicator = any(indicator in query_lower for indicator in person_indicators)
        
        # Check if query has name-like patterns (multiple words with capitals)
        words = query.split()
        has_name_pattern = len(words) >= 2 and any(word[0].isupper() for word in words if word)
        
        return has_indicator or has_name_pattern
    
    def _generate_person_queries(self, original_query: str) -> List[str]:
        """Generate expanded queries for person searches"""
        # Extract potential name from query
        query_lower = original_query.lower()
        
        # Remove common question words and clean up
        clean_query = original_query
        for phrase in ['who is', 'tell me about', 'information about', 'about', 'details about', '?']:
            clean_query = clean_query.replace(phrase, '').strip()
        
        # Generate expanded queries (simple concatenation)
        expanded_queries = [
            f"{clean_query} teacher",
            f"{clean_query} instructor", 
            f"{clean_query} staff",
            f"{clean_query} official",
            f"{clean_query} department",
            f"{clean_query} contact",
            # Also try with partial name components
            clean_query.split()[0] + " instructor" if clean_query.split() else "instructor",
            clean_query.split()[-1] + " teacher" if clean_query.split() else "teacher"
        ]
        
        # Remove duplicates and empty queries
        expanded_queries = [q.strip() for q in expanded_queries if q.strip()]
        expanded_queries = list(set(expanded_queries))  # Remove duplicates
        
        return expanded_queries
    
    def _contains_person_name(self, content: str, query: str) -> bool:
        """Check if content contains the person name from the query"""
        # Extract name parts from query
        query_cleaned = query.lower().replace('who is', '').replace('tell me about', '').replace('?', '').strip()
        query_words = query_cleaned.split()
        name_words = [word for word in query_words if len(word) > 2 and word.isalpha()]
        
        if not name_words:
            return False
        
        content_lower = content.lower()
        
        # More lenient matching - if we find at least 2 name parts, consider it a match
        # This helps with cases like "Julekha Akter Koli" where middle names might be missing
        matches = sum(1 for name_word in name_words if name_word in content_lower)
        return matches >= min(2, len(name_words))  # At least 2 matches, or all if less than 2 words
    
    def _inject_section_docs(self, section_name: str) -> List[Dict[str, Any]]:
        """Create synthetic retrieved docs from a structured section to bypass weak embedding recall"""
        try:
            # Load and extract structured data
            raw_text = self.processor.load_data(self.data_file)
            cleaned = self.processor.clean_text(raw_text)
            structured = self.processor.extract_structured_data(cleaned)
            section_text = structured.get(section_name, '')
            if not section_text:
                return []
            # Respect chunking for large sections
            section_chunks = self.processor._create_section_chunks(section_text, section_name)
            # Convert to retrieved_docs format expected by generator
            retrieved_docs = []
            for ch in section_chunks[: self.max_retrieval_results]:
                retrieved_docs.append({
                    'content': ch['content'],
                    'metadata': {'section': section_name, 'injected': True},
                    'similarity_score': 0.99
                })
            return retrieved_docs
        except Exception as e:
            logger.warning(f"Failed to inject section docs for {section_name}: {e}")
            return []
    
    def _is_system_ready(self) -> bool:
        """Check if all system components are initialized"""
        return (self.processor is not None and 
                self.vector_db is not None and 
                self.rag_generator is not None)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the RAG system"""
        try:
            if not self._is_system_ready():
                return {'status': 'not_initialized'}
            
            db_info = self.vector_db.get_collection_info()
            
            return {
                'status': 'ready',
                'database': db_info,
                'models': {
                    'embedding': self.embedding_model,
                    'generation': 'KPI-GPT V1.0'
                },
                'config': {
                    'chunk_size': self.chunk_size,
                    'chunk_overlap': self.chunk_overlap,
                    'max_retrieval_results': self.max_retrieval_results
                },
                'data_file': self.data_file
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def reset_database(self) -> bool:
        """Reset and rebuild the vector database"""
        try:
            logger.info("Resetting vector database...")
            success = self.vector_db.reset_database()
            if success:
                success = self._populate_database()
            return success
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            return False

def create_kpi_rag_system() -> KPIGPTRagSystem:
    """Factory function to create KPI RAG system with environment variables"""
    
    # Get configuration from environment variables
    config = {
        'data_file': os.getenv('DATA_FILE', 'kpi_data.txt'),
        'db_path': os.getenv('VECTOR_DB_PATH', './vector_db'),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
        'groq_model': os.getenv('GROQ_MODEL', 'llama3-8b-8192'),
        'chunk_size': int(os.getenv('CHUNK_SIZE', '1000')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '200')),
        'max_retrieval_results': int(os.getenv('MAX_RETRIEVAL_RESULTS', '5'))
    }
    
    return KPIGPTRagSystem(**config)

def main():
    """Main function for testing the RAG system"""
    print("🚀 Initializing KPI GPT RAG System...")
    print("=" * 50)
    
    # Create and setup RAG system
    rag_system = create_kpi_rag_system()
    
    print("📚 Setting up system components...")
    setup_success = rag_system.setup_system()
    
    if not setup_success:
        print("❌ Failed to setup RAG system")
        return
    
    print("✅ RAG system setup completed!")
    
    # Show system info
    system_info = rag_system.get_system_info()
    print(f"📊 System Info:")
    print(f"   - Database documents: {system_info['database']['document_count']}")
    print(f"   - Embedding model: {system_info['models']['embedding']}")
    print(f"   - Generation model: {system_info['models']['generation']}")
    
    print("\n" + "=" * 50)
    print("💬 KPI GPT is ready! You can now ask questions about Khulna Polytechnic Institute.")
    print("   Type 'quit' to exit, 'info' for system information")
    print("=" * 50 + "\n")
    
    # Interactive query loop
    while True:
        try:
            user_input = input("🤔 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'info':
                info = rag_system.get_system_info()
                print(f"📊 System Status: {info.get('status', 'unknown')}")
                continue
            elif not user_input:
                continue
            
            print("🤖 KPI GPT:", end=" ", flush=True)
            
            # Process query and get response
            response = rag_system.query(user_input)
            
            if 'error' in response:
                print(f"❌ Error: {response['error']}")
            else:
                print(response['answer'])
                
                # Show sources if available
                if response.get('sources'):
                    print(f"\n📚 Sources ({len(response['sources'])}):")
                    for i, source in enumerate(response['sources'][:3], 1):
                        print(f"   {i}. Section: {source['section']} (Score: {source['similarity_score']:.2f})")
            
            print("\n" + "-" * 30 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
