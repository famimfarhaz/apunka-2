"""
Natural Language Processor for KPI GPT RAG System
Handles casual, conversational queries and makes them more natural
"""

import re
from typing import Dict, List, Tuple
import logging

class NaturalLanguageProcessor:
    """Processes natural language queries to make them more conversational"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Casual query patterns and their more formal equivalents
        self.query_transformations = {
            # Basic info requests
            r'\b(tell me about|info about|about)\s+(.+)': r'What information do you have about \2?',
            r'\b(who is|who\'s)\s+(.+)\?*': r'Who is \2?',
            r'\b(what about|how about)\s+(.+)\?*': r'Tell me about \2',
            
            # Casual greetings and responses
            r'^(hi|hello|hey)\b.*': r'Hello! How can I help you with KPI information?',
            r'^(thanks|thank you)\b.*': r'You\'re welcome! Is there anything else you\'d like to know?',
            
            # Follow-up questions
            r'\b(more info|more details|tell me more)\b.*': r'Can you provide more details?',
            r'\b(anything else|what else)\b.*': r'What else can you tell me?',
            
            # Department/staff queries
            r'\b(teachers in|instructors in|staff in)\s+(.+)': r'Who are the teachers in \2 department?',
            r'\b(civil dept|civil department)\b': r'Civil department',
            r'\b(electrical dept|electrical department)\b': r'Electrical department',
        }
        
        # Pronouns that need context resolution
        self.pronouns = ['him', 'her', 'he', 'she', 'they', 'this person', 'that person', 'this teacher', 'that teacher']
        
        # Casual expressions for different types of information
        self.casual_patterns = {
            'contact': ['phone', 'number', 'contact', 'call', 'mobile'],
            'department': ['dept', 'department', 'works in', 'belongs to'],
            'position': ['job', 'position', 'role', 'designation', 'what does', 'what is'],
            'email': ['email', 'mail', 'contact']
        }
    
    def is_conversational_query(self, query: str) -> bool:
        """Check if the query is conversational/casual"""
        casual_indicators = [
            # Pronouns
            r'\b(him|her|he|she|they)\b',
            # Casual starters
            r'^(tell me|what about|how about|more about)',
            # Incomplete sentences
            r'^(his|her|their)\s+\w+\?*$',
            # Single words or very short phrases
            r'^\w{1,15}\?*$',
            # Questions without proper structure
            r'\?$' if len(query.split()) <= 3 else None
        ]
        
        return any(re.search(pattern, query.lower()) for pattern in casual_indicators if pattern)
    
    def transform_casual_query(self, query: str) -> str:
        """Transform casual query to more structured format"""
        transformed = query.strip()
        
        # Apply transformation patterns
        for pattern, replacement in self.query_transformations.items():
            if re.search(pattern, transformed, re.IGNORECASE):
                transformed = re.sub(pattern, replacement, transformed, flags=re.IGNORECASE)
                self.logger.info(f"Transformed query: '{query}' -> '{transformed}'")
                break
        
        return transformed.strip()
    
    def extract_intent(self, query: str) -> Dict[str, any]:
        """Extract user intent from the query"""
        query_lower = query.lower()
        
        intent = {
            'type': 'general',
            'subject': None,
            'focus': None,
            'is_followup': False,
            'requires_context': False
        }
        
        # Check for person-focused queries
        if any(word in query_lower for word in ['who', 'person', 'teacher', 'instructor']):
            intent['type'] = 'person'
        
        # Check for department queries
        if any(word in query_lower for word in ['department', 'dept', 'civil', 'electrical', 'mechanical']):
            intent['type'] = 'department'
        
        # Check for contact information queries
        if any(word in query_lower for word in self.casual_patterns['contact']):
            intent['focus'] = 'contact'
        
        # Check for position/role queries
        if any(word in query_lower for word in self.casual_patterns['position']):
            intent['focus'] = 'position'
        
        # Check if it's a follow-up question
        followup_indicators = ['more', 'else', 'also', 'what about', 'how about', 'tell me more']
        if any(indicator in query_lower for indicator in followup_indicators):
            intent['is_followup'] = True
        
        # Check if requires context (has pronouns)
        if any(pronoun in query_lower for pronoun in self.pronouns):
            intent['requires_context'] = True
        
        return intent
    
    def make_response_conversational(self, response: str, query: str) -> str:
        """Make the AI response more conversational and natural"""
        # Remove overly formal introductions if the query is casual
        if len(query.split()) <= 4:  # Short, casual query
            response = re.sub(r'^I\'m KPI GPT.*?\. ', '', response)
            response = re.sub(r'^According to.*?, ', '', response)
            response = re.sub(r'^Based on.*?, ', '', response)
        
        # Make it more conversational for follow-up questions
        if any(word in query.lower() for word in ['more', 'else', 'also']):
            if response.startswith('According to'):
                response = re.sub(r'^According to.*?, ', 'Also, ', response)
        
        # Add conversational elements for very short responses
        if len(response) < 100 and 'no information' not in response.lower():
            response = f"Sure! {response}"
        
        return response
    
    def suggest_followup_questions(self, query: str, response: str) -> List[str]:
        """Suggest relevant follow-up questions based on the context"""
        suggestions = []
        
        query_lower = query.lower()
        response_lower = response.lower()
        
        # If discussing a person, suggest related queries
        if 'instructor' in response_lower or 'teacher' in response_lower:
            if 'department' not in query_lower:
                suggestions.append("What department does he/she work in?")
            if 'contact' not in query_lower and 'phone' not in query_lower:
                suggestions.append("What's his/her contact information?")
            if 'email' not in query_lower:
                suggestions.append("What's the email address?")
        
        # If discussing a department
        if 'department' in response_lower:
            suggestions.append("Who are the other teachers in this department?")
            suggestions.append("What courses does this department offer?")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def detect_query_type(self, query: str) -> str:
        """Detect the type of query for better processing"""
        query_lower = query.lower()
        
        # Greeting
        if re.match(r'^(hi|hello|hey)', query_lower):
            return 'greeting'
        
        # Thank you
        if re.match(r'^(thanks|thank you)', query_lower):
            return 'thanks'
        
        # Person query
        if re.search(r'\b(who is|tell me about|info about)\b', query_lower):
            return 'person_info'
        
        # Pronoun query (requires context)
        if any(pronoun in query_lower for pronoun in self.pronouns):
            return 'pronoun_reference'
        
        # Department query
        if 'department' in query_lower or 'dept' in query_lower:
            return 'department_info'
        
        # Contact query
        if any(word in query_lower for word in ['phone', 'contact', 'email', 'number']):
            return 'contact_info'
        
        return 'general'
