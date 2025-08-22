"""
Groq API Integration Module for KPI GPT RAG System
Created by: Famim Farhaz

This module handles integration with Groq API for text generation
in the RAG pipeline.
"""

import os
from groq import Groq
from typing import List, Dict, Any, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqClient:
    """Groq API client for KPI GPT RAG system"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-8b-8192"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        
        # Initialize Groq client
        try:
            self.client = Groq(api_key=self.api_key)
            logger.info(f"Groq client initialized successfully with model: {model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 1024, 
                         temperature: float = 0.7) -> str:
        """Generate response using Groq API"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False
            )
            
            generated_text = response.choices[0].message.content
            logger.info("Response generated successfully")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def generate_stream_response(self, prompt: str, max_tokens: int = 1024,
                                temperature: float = 0.7):
        """Generate streaming response using Groq API"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            raise

class RAGGenerator:
    """RAG (Retrieval-Augmented Generation) system using Groq API"""
    
    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client
        
    def create_rag_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Create an enhanced RAG prompt with query and retrieved documents"""
        
        # Enhanced system prompt for KPI GPT
        system_prompt = """You are KPI GPT, a specialized AI assistant for Khulna Polytechnic Institute (KPI). You have extensive knowledge about the institute and can answer ANY question about:

🏫 KHULNA POLYTECHNIC INSTITUTE (KPI) EXPERTISE:
• Teachers, instructors, staff, and officials (names, contacts, departments)
• Departments: Computer, Civil, Electrical, Electronics, Mechanical, Power, RAC, etc.
• Student information, class captains, and academic details
• Institute facilities, clubs, activities (BNCC, Rover Scout, Debate Club, etc.)
• Contact information (phone numbers, emails, addresses)
• Policies, procedures, and general institute information
• Principal and administrative details

📋 YOUR CAPABILITIES:
✓ Find specific people by name (exact or partial matches)
✓ Provide contact details (phones, emails) 
✓ Explain roles and designations
✓ List department members
✓ Answer about any aspect of KPI
✓ Handle various question formats and styles

🎯 RESPONSE GUIDELINES:
• Answer directly and comprehensively
• Include specific details like phone numbers, emails when available
• If asking about a person, provide their full details
• Use the context information to give accurate answers
• Be helpful, friendly, and professional
• If information is incomplete, say what you know and acknowledge limitations"""

        # Context from retrieved documents with better formatting
        context_sections = []
        for i, doc in enumerate(retrieved_docs, 1):
            section = doc.get('metadata', {}).get('section', 'Unknown')
            content = doc.get('content', '').strip()
            similarity = doc.get('similarity_score', 0)
            
            context_sections.append(f"""--- CONTEXT {i} (Section: {section}, Relevance: {similarity:.3f}) ---
{content}""")
        
        context = "\n\n".join(context_sections)
        
        # Create the enhanced full prompt
        full_prompt = f"""{system_prompt}

=== RELEVANT CONTEXT INFORMATION ===
{context}

=== USER QUESTION ===
{query}

=== INSTRUCTIONS ===
Using the context information above, provide a detailed and accurate answer about Khulna Polytechnic Institute. Extract all relevant information from the context to answer the user's question completely. Include specific details like names, phone numbers, emails, designations, and departments when available."""

        return full_prompt
    
    def generate_answer(self, query: str, retrieved_docs: List[Dict[str, Any]], 
                       max_tokens: int = 1024, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate answer using RAG approach"""
        try:
            # Create RAG prompt
            rag_prompt = self.create_rag_prompt(query, retrieved_docs)
            
            # Generate response
            logger.info(f"Generating answer for query: {query[:50]}...")
            answer = self.groq_client.generate_response(
                prompt=rag_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Prepare response
            response = {
                'query': query,
                'answer': answer,
                'sources': [
                    {
                        'section': doc['metadata']['section'],
                        'similarity_score': doc.get('similarity_score', 0.0),
                        'content_preview': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
                    }
                    for doc in retrieved_docs
                ],
                'model_used': 'KPI-GPT V1.0',
                'context_length': len(rag_prompt)
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating RAG answer: {e}")
            raise
    
    def generate_stream_answer(self, query: str, retrieved_docs: List[Dict[str, Any]], 
                              max_tokens: int = 1024, temperature: float = 0.7):
        """Generate streaming answer using RAG approach"""
        try:
            # Create RAG prompt
            rag_prompt = self.create_rag_prompt(query, retrieved_docs)
            
            # Generate streaming response
            logger.info(f"Generating streaming answer for query: {query[:50]}...")
            
            for chunk in self.groq_client.generate_stream_response(
                prompt=rag_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error generating streaming RAG answer: {e}")
            raise
    
    def evaluate_answer_quality(self, query: str, answer: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate the quality of generated answer"""
        try:
            # Simple quality metrics
            metrics = {
                'answer_length': len(answer),
                'sources_used': len(sources),
                'avg_similarity': sum(s.get('similarity_score', 0) for s in sources) / len(sources) if sources else 0,
                'query_length': len(query),
                'has_specific_info': any(keyword in answer.lower() for keyword in ['contact', 'email', 'phone', 'department', 'teacher'])
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating answer quality: {e}")
            return {}

def create_rag_system(api_key: Optional[str] = None, model: str = "llama3-8b-8192") -> RAGGenerator:
    """Create a complete RAG system"""
    try:
        groq_client = GroqClient(api_key=api_key, model=model)
        rag_generator = RAGGenerator(groq_client)
        logger.info("RAG system created successfully")
        return rag_generator
    except Exception as e:
        logger.error(f"Failed to create RAG system: {e}")
        raise

if __name__ == "__main__":
    # Test the Groq client
    try:
        # Create RAG system
        rag_system = create_rag_system()
        
        # Mock retrieved documents for testing
        mock_docs = [
            {
                'content': 'Sheikh Mustafizur Rahman is the Principal of Khulna Polytechnic Institute. Mobile Number: 01765696900, Telephone Number: +8802477795024',
                'metadata': {'section': 'principal'},
                'similarity_score': 0.95
            }
        ]
        
        # Test query
        query = "Who is the principal of KPI?"
        
        # Generate answer
        response = rag_system.generate_answer(query, mock_docs)
        
        print(f"Query: {response['query']}")
        print(f"Answer: {response['answer']}")
        print(f"Sources: {len(response['sources'])}")
        print(f"Model: {response['model_used']}")
        
    except Exception as e:
        print(f"Error testing Groq client: {e}")
