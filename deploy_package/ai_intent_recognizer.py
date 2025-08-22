"""
AI-Powered Intent Recognition System
Uses Groq API to understand user intent from natural language without pattern matching
"""

import json
import logging
from typing import Dict, Any, List, Optional
from groq_client import GroqClient

class AIIntentRecognizer:
    """Uses AI to understand user intent from natural language queries"""
    
    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client
        self.logger = logging.getLogger(__name__)
        
        # System prompt for intent recognition
        self.intent_prompt = """You are an AI assistant that analyzes user queries about Khulna Polytechnic Institute (KPI) and extracts intent and entities.

Your job is to understand what the user is asking for and return a structured JSON response.

Available entity types in KPI database:
- PERSON: Teachers, instructors, staff, officials, students
- DEPARTMENT: Civil, Electrical, Mechanical, Computer, etc.
- CONTACT_INFO: Phone, email, address
- GENERAL_INFO: About KPI, courses, facilities

Possible intents:
- PERSON_INFO: User wants information about a specific person
- CONTACT_INFO: User wants contact details
- DEPARTMENT_INFO: User wants information about a department
- GENERAL_KPI_INFO: General questions about KPI
- GREETING: User is greeting
- THANKS: User is expressing gratitude

Always return valid JSON in this exact format:
{
  "intent": "PERSON_INFO|CONTACT_INFO|DEPARTMENT_INFO|GENERAL_KPI_INFO|GREETING|THANKS",
  "entities": {
    "person_name": "extracted person name or null",
    "department": "extracted department or null",
    "info_type": "contact|general|specific_detail or null"
  },
  "query_type": "question|request|greeting|thanks",
  "confidence": 0.0-1.0,
  "natural_query": "reformulated natural query for database search"
}

Examples:

User: "did you have any information about Md. Al-Emran"
Response: {"intent": "PERSON_INFO", "entities": {"person_name": "Md. Al-Emran", "department": null, "info_type": "general"}, "query_type": "question", "confidence": 0.9, "natural_query": "Md. Al-Emran teacher instructor information"}

User: "tell me about civil department teachers"
Response: {"intent": "DEPARTMENT_INFO", "entities": {"person_name": null, "department": "Civil", "info_type": "general"}, "query_type": "request", "confidence": 0.9, "natural_query": "Civil department teachers instructors staff"}

User: "what's his phone number"
Response: {"intent": "CONTACT_INFO", "entities": {"person_name": null, "department": null, "info_type": "contact"}, "query_type": "question", "confidence": 0.8, "natural_query": "phone number contact information"}

Analyze the following user query and return only the JSON response:"""

    def analyze_intent(self, user_query: str, conversation_context: str = "") -> Dict[str, Any]:
        """Analyze user intent using AI"""
        try:
            # Prepare the full prompt
            full_prompt = self.intent_prompt
            
            if conversation_context:
                full_prompt += f"\n\nConversation context: {conversation_context}\n"
            
            full_prompt += f"\nUser query: \"{user_query}\""
            
            # Get AI analysis
            response = self.groq_client.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert at understanding user intent and extracting entities from natural language queries."},
                    {"role": "user", "content": full_prompt}
                ],
                model=self.groq_client.model,
                temperature=0.1,  # Low temperature for consistent structured output
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content.strip()
            self.logger.info(f"AI intent analysis: {ai_response[:200]}...")
            
            # Parse JSON response
            try:
                intent_data = json.loads(ai_response)
                
                # Validate required fields
                required_fields = ['intent', 'entities', 'query_type', 'confidence', 'natural_query']
                if not all(field in intent_data for field in required_fields):
                    self.logger.warning("AI response missing required fields, using fallback")
                    return self._fallback_intent_analysis(user_query)
                
                return intent_data
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse AI intent response as JSON: {e}")
                # Try to extract JSON from response
                return self._extract_json_from_response(ai_response, user_query)
                
        except Exception as e:
            self.logger.error(f"Error in AI intent analysis: {e}")
            return self._fallback_intent_analysis(user_query)
    
    def _extract_json_from_response(self, response: str, user_query: str) -> Dict[str, Any]:
        """Try to extract JSON from AI response"""
        try:
            # Look for JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass
        
        return self._fallback_intent_analysis(user_query)
    
    def _fallback_intent_analysis(self, user_query: str) -> Dict[str, Any]:
        """Fallback intent analysis when AI fails"""
        query_lower = user_query.lower()
        
        # Simple heuristics as fallback
        if any(greeting in query_lower for greeting in ['hi', 'hello', 'hey']):
            return {
                "intent": "GREETING",
                "entities": {"person_name": None, "department": None, "info_type": None},
                "query_type": "greeting",
                "confidence": 0.7,
                "natural_query": user_query
            }
        
        if any(thanks in query_lower for thanks in ['thank', 'thanks']):
            return {
                "intent": "THANKS",
                "entities": {"person_name": None, "department": None, "info_type": None},
                "query_type": "thanks",
                "confidence": 0.7,
                "natural_query": user_query
            }
        
        # Check for person names (simple heuristic)
        words = user_query.split()
        potential_names = [word for word in words if word and word[0].isupper()]
        
        if len(potential_names) >= 2:  # Likely contains a name
            return {
                "intent": "PERSON_INFO",
                "entities": {
                    "person_name": ' '.join(potential_names),
                    "department": None,
                    "info_type": "general"
                },
                "query_type": "question",
                "confidence": 0.6,
                "natural_query": f"{' '.join(potential_names)} teacher instructor information"
            }
        
        # Default to general info
        return {
            "intent": "GENERAL_KPI_INFO",
            "entities": {"person_name": None, "department": None, "info_type": "general"},
            "query_type": "question",
            "confidence": 0.5,
            "natural_query": user_query
        }
    
    def enhance_query_for_search(self, intent_data: Dict[str, Any]) -> str:
        """Generate enhanced query for database search based on intent"""
        intent = intent_data.get('intent', '')
        entities = intent_data.get('entities', {})
        natural_query = intent_data.get('natural_query', '')
        
        # Build search query based on intent and entities
        search_terms = []
        
        if intent == 'PERSON_INFO':
            person_name = entities.get('person_name')
            if person_name:
                search_terms.append(person_name)
                search_terms.extend(['teacher', 'instructor', 'staff', 'official'])
        
        elif intent == 'CONTACT_INFO':
            search_terms.extend(['phone', 'email', 'contact', 'mobile'])
            person_name = entities.get('person_name')
            if person_name:
                search_terms.append(person_name)
        
        elif intent == 'DEPARTMENT_INFO':
            department = entities.get('department')
            if department:
                search_terms.extend([department, 'department', 'faculty'])
                search_terms.extend(['teachers', 'instructors', 'staff'])
        
        # Use natural query if we couldn't build specific terms
        if not search_terms:
            return natural_query
        
        return ' '.join(search_terms)
    
    def should_use_ai_retrieval(self, intent_data: Dict[str, Any]) -> bool:
        """Determine if we should use AI-enhanced retrieval"""
        intent = intent_data.get('intent', '')
        confidence = intent_data.get('confidence', 0)
        
        # Use AI retrieval for person info and contact info with reasonable confidence
        if intent in ['PERSON_INFO', 'CONTACT_INFO'] and confidence > 0.6:
            return True
        
        # Use for department info
        if intent == 'DEPARTMENT_INFO' and confidence > 0.5:
            return True
        
        return False
