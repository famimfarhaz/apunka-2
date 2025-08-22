"""
Semantic Document Retrieval System
Works with AI-interpreted queries for natural language understanding
"""

import logging
from typing import Dict, Any, List, Optional
from vector_database import VectorDatabase

class SemanticRetrieval:
    """Enhanced document retrieval using AI intent understanding"""
    
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
        self.logger = logging.getLogger(__name__)
    
    def retrieve_documents(self, intent_data: Dict[str, Any], max_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents based on AI-interpreted intent"""
        try:
            intent = intent_data.get('intent', '')
            entities = intent_data.get('entities', {})
            confidence = intent_data.get('confidence', 0)
            natural_query = intent_data.get('natural_query', '')
            
            self.logger.info(f"Semantic retrieval for intent: {intent}, confidence: {confidence:.2f}")
            
            # Strategy 1: Direct semantic search with natural query
            primary_results = self._semantic_search(natural_query, max_results)
            
            # Strategy 2: Entity-based search if we have specific entities
            entity_results = self._entity_based_search(entities, max_results)
            
            # Strategy 3: Intent-specific search strategies
            intent_results = self._intent_specific_search(intent, entities, max_results)
            
            # Combine and rank results
            combined_results = self._combine_and_rank_results(
                primary_results, entity_results, intent_results, intent_data
            )
            
            return combined_results[:max_results]
            
        except Exception as e:
            self.logger.error(f"Error in semantic retrieval: {e}")
            # Fallback to basic search
            return self.vector_db.search_similar(natural_query or "KPI information", max_results)
    
    def _semantic_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Basic semantic search using the query"""
        if not query.strip():
            return []
        
        try:
            results = self.vector_db.search_similar(query, max_results)
            # Add source info
            for result in results:
                result['retrieval_method'] = 'semantic_search'
                result['search_query'] = query
            return results
        except Exception as e:
            self.logger.warning(f"Semantic search failed: {e}")
            return []
    
    def _entity_based_search(self, entities: Dict[str, Any], max_results: int) -> List[Dict[str, Any]]:
        """Search based on extracted entities"""
        results = []
        
        try:
            # Person-based search
            person_name = entities.get('person_name')
            if person_name:
                person_query = f"{person_name} teacher instructor staff"
                person_results = self.vector_db.search_similar(person_query, max_results)
                
                # Filter results that actually contain the person name
                filtered_results = []
                for result in person_results:
                    content_lower = result.get('content', '').lower()
                    name_parts = person_name.lower().split()
                    
                    # Check if at least 2 name parts are found (or all if less than 2)
                    found_parts = sum(1 for part in name_parts if part in content_lower and len(part) > 2)
                    if found_parts >= min(2, len(name_parts)):
                        result['retrieval_method'] = 'entity_person'
                        result['matched_entity'] = person_name
                        result['name_match_score'] = found_parts / len(name_parts)
                        filtered_results.append(result)
                
                results.extend(filtered_results)
            
            # Department-based search
            department = entities.get('department')
            if department:
                dept_query = f"{department} department teachers instructors"
                dept_results = self.vector_db.search_similar(dept_query, max_results)
                for result in dept_results:
                    result['retrieval_method'] = 'entity_department'
                    result['matched_entity'] = department
                results.extend(dept_results)
        
        except Exception as e:
            self.logger.warning(f"Entity-based search failed: {e}")
        
        return results
    
    def _intent_specific_search(self, intent: str, entities: Dict[str, Any], max_results: int) -> List[Dict[str, Any]]:
        """Apply intent-specific search strategies"""
        results = []
        
        try:
            if intent == 'PERSON_INFO':
                # Focus on teacher and staff sections
                section_filter = {'section': {'$in': ['teachers', 'officials']}}
                section_results = self.vector_db.search_similar(
                    entities.get('person_name', '') + " information", 
                    max_results, 
                    where=section_filter
                )
                for result in section_results:
                    result['retrieval_method'] = 'intent_person'
                results.extend(section_results)
            
            elif intent == 'CONTACT_INFO':
                # Search for contact-related information
                contact_query = "phone email contact mobile address"
                person_name = entities.get('person_name', '')
                if person_name:
                    contact_query = f"{person_name} {contact_query}"
                
                contact_results = self.vector_db.search_similar(contact_query, max_results)
                for result in contact_results:
                    result['retrieval_method'] = 'intent_contact'
                results.extend(contact_results)
            
            elif intent == 'DEPARTMENT_INFO':
                # Search in specific department sections
                dept_name = entities.get('department', '')
                if dept_name:
                    dept_query = f"{dept_name} department faculty staff teachers"
                    dept_results = self.vector_db.search_similar(dept_query, max_results)
                    for result in dept_results:
                        result['retrieval_method'] = 'intent_department'
                    results.extend(dept_results)
        
        except Exception as e:
            self.logger.warning(f"Intent-specific search failed: {e}")
        
        return results
    
    def _combine_and_rank_results(self, primary: List, entity: List, intent: List, 
                                intent_data: Dict) -> List[Dict[str, Any]]:
        """Combine and rank results from different search strategies"""
        
        # Create a dictionary to avoid duplicates and combine scores
        result_map = {}
        
        # Add results with different weights
        all_results = [
            (primary, 1.0, 'primary'),
            (entity, 1.2, 'entity'),  # Slightly higher weight for entity matches
            (intent, 1.1, 'intent')   # Slight boost for intent-specific results
        ]
        
        for results, weight, source in all_results:
            for result in results:
                content = result.get('content', '')
                doc_id = result.get('id', hash(content[:100]))  # Use hash as ID if not available
                
                if doc_id not in result_map:
                    result_map[doc_id] = result.copy()
                    result_map[doc_id]['combined_score'] = result.get('similarity_score', 0) * weight
                    result_map[doc_id]['sources'] = [source]
                else:
                    # Boost score if found by multiple methods
                    existing_score = result_map[doc_id]['combined_score']
                    new_score = result.get('similarity_score', 0) * weight
                    result_map[doc_id]['combined_score'] = max(existing_score, new_score) + (new_score * 0.1)
                    result_map[doc_id]['sources'].append(source)
        
        # Special boosting for entity matches
        person_name = intent_data.get('entities', {}).get('person_name')
        if person_name:
            name_parts = person_name.lower().split()
            for doc_id, result in result_map.items():
                content_lower = result.get('content', '').lower()
                name_matches = sum(1 for part in name_parts if part in content_lower and len(part) > 2)
                
                if name_matches >= min(2, len(name_parts)):
                    # Significant boost for documents that contain the person name
                    result['combined_score'] += 0.3
                    result['name_match_boost'] = True
        
        # Sort by combined score
        ranked_results = sorted(
            result_map.values(), 
            key=lambda x: x.get('combined_score', 0), 
            reverse=True
        )
        
        self.logger.info(f"Combined {len(ranked_results)} unique documents from semantic retrieval")
        return ranked_results
    
    def get_retrieval_info(self, results: List[Dict]) -> Dict[str, Any]:
        """Get information about the retrieval process"""
        if not results:
            return {'total_results': 0, 'methods_used': [], 'has_name_matches': False}
        
        methods_used = set()
        name_matches = 0
        
        for result in results:
            if 'retrieval_method' in result:
                methods_used.add(result['retrieval_method'])
            if result.get('name_match_boost', False):
                name_matches += 1
        
        return {
            'total_results': len(results),
            'methods_used': list(methods_used),
            'has_name_matches': name_matches > 0,
            'name_match_count': name_matches,
            'best_score': results[0].get('combined_score', 0) if results else 0
        }
