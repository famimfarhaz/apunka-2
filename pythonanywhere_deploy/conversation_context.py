"""
Conversation Context Manager for KPI GPT RAG System
Handles conversation history, context tracking, and pronoun resolution
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

class ConversationContext:
    """Manages conversation history and context for natural dialogue"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conversation_history = []
        self.current_person_context = None  # Currently discussed person
        self.mentioned_people = {}  # Track people mentioned in conversation
        self.session_start = datetime.now()
        
    def extract_person_names(self, text: str) -> List[str]:
        """Extract person names from text using patterns"""
        # Common patterns for names at KPI
        patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]*)*\s+[A-Z][a-z]+\b',  # Full names
            r'\b(?:Md\.|Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]*)*\b',  # Titles with names
            r'\b[A-Z]\.[A-Z]\.\s*[A-Z][a-z]+\b',  # Initials like S.M. Kamruzzaman
        ]
        
        names = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)
        
        # Filter out common false positives
        false_positives = ['Khulna Polytechnic', 'Chief Instructor', 'Junior Instructor', 'Non Tech']
        names = [name for name in names if name not in false_positives and len(name.split()) <= 4]
        
        return list(set(names))  # Remove duplicates
    
    def add_interaction(self, user_query: str, ai_response: str, sources: List[Dict] = None):
        """Add a new interaction to conversation history"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_query': user_query,
            'ai_response': ai_response,
            'sources': sources or [],
            'extracted_names': []
        }
        
        # Extract person names from both query and response
        query_names = self.extract_person_names(user_query)
        response_names = self.extract_person_names(ai_response)
        all_names = list(set(query_names + response_names))
        
        interaction['extracted_names'] = all_names
        
        # Update mentioned people and current context
        for name in all_names:
            self.mentioned_people[name.lower()] = {
                'original_name': name,
                'last_mentioned': datetime.now().isoformat(),
                'mention_count': self.mentioned_people.get(name.lower(), {}).get('mention_count', 0) + 1
            }
            
            # Set as current person if this seems to be about them
            if self.is_person_focused_query(user_query, name):
                self.current_person_context = name
                self.logger.info(f"Setting current person context to: {name}")
        
        self.conversation_history.append(interaction)
        
        # Keep only last 10 interactions to avoid memory bloat
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def is_person_focused_query(self, query: str, name: str) -> bool:
        """Check if the query is focused on a specific person"""
        query_lower = query.lower()
        name_parts = name.lower().split()
        
        # Check if query contains the person's name
        for part in name_parts:
            if part in query_lower and len(part) > 2:  # Avoid short words like "Md"
                return True
        
        # Check for person-focused question patterns
        person_patterns = [
            r'\bwho\s+is\b',
            r'\btell\s+me\s+about\b',
            r'\bwhat\s+do\s+you\s+know\s+about\b',
            r'\binformation\s+about\b'
        ]
        
        return any(re.search(pattern, query_lower) for pattern in person_patterns)
    
    def resolve_pronouns(self, query: str) -> str:
        """Resolve pronouns in the query to actual names"""
        if not self.current_person_context:
            return query
        
        query_lower = query.lower()
        resolved_query = query
        
        # Pronoun patterns and their replacements
        pronoun_patterns = [
            (r'\bhim\b', self.current_person_context),
            (r'\bher\b', self.current_person_context),
            (r'\bhe\b', self.current_person_context),
            (r'\bshe\b', self.current_person_context),
            (r'\bthis\s+person\b', self.current_person_context),
            (r'\bthis\s+teacher\b', self.current_person_context),
            (r'\bthis\s+instructor\b', self.current_person_context),
        ]
        
        for pattern, replacement in pronoun_patterns:
            if re.search(pattern, query_lower):
                resolved_query = re.sub(pattern, replacement, resolved_query, flags=re.IGNORECASE)
                self.logger.info(f"Resolved pronoun in query: '{query}' -> '{resolved_query}'")
                break
        
        return resolved_query
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation context for AI"""
        if not self.conversation_history:
            return ""
        
        context_lines = ["Recent conversation context:"]
        
        # Add last 3 interactions for context
        for interaction in self.conversation_history[-3:]:
            context_lines.append(f"User: {interaction['user_query']}")
            context_lines.append(f"AI: {interaction['ai_response'][:200]}...")
            context_lines.append("")
        
        if self.current_person_context:
            context_lines.append(f"Currently discussing: {self.current_person_context}")
        
        return "\n".join(context_lines)
    
    def enhance_query_with_context(self, query: str) -> str:
        """Enhance query with conversation context"""
        # First resolve pronouns
        enhanced_query = self.resolve_pronouns(query)
        
        # Add context if the query is vague or context-dependent
        vague_patterns = [
            r'^(what about|how about|tell me more|more info|details)',
            r'\b(him|her|he|she|this person|that person)\b'
        ]
        
        is_vague = any(re.search(pattern, query.lower()) for pattern in vague_patterns)
        
        if is_vague and self.current_person_context:
            enhanced_query = f"{enhanced_query} {self.current_person_context}"
        
        return enhanced_query
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of current conversation context"""
        return {
            'session_duration': str(datetime.now() - self.session_start),
            'total_interactions': len(self.conversation_history),
            'current_person': self.current_person_context,
            'mentioned_people': list(self.mentioned_people.keys()),
            'last_query': self.conversation_history[-1]['user_query'] if self.conversation_history else None
        }
    
    def clear_context(self):
        """Clear conversation context (for new session)"""
        self.conversation_history = []
        self.current_person_context = None
        self.mentioned_people = {}
        self.session_start = datetime.now()
        self.logger.info("Conversation context cleared")
