"""
Memory Management - Handles conversation history, context, and knowledge storage
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

class MemoryManager:
    """Manages AI memory, context, and conversation history."""
    
    def __init__(self, storage_path: str = 'data/memory'):
        """Initialize the memory manager."""
        self.storage_path = storage_path
        self.logger = logging.getLogger(__name__)
        
        # In-memory caches
        self.short_term_memory = {}  # Active session data
        self.context_cache = {}      # Frequently accessed context
        self.knowledge_base = {}     # Persistent knowledge
        
        # Memory limits
        self.max_short_term_items = 1000
        self.max_context_items = 500
        self.max_session_age_hours = 24
        
        # Initialize storage
        self._initialize_storage()
        self._load_persistent_memory()
    
    def _initialize_storage(self):
        """Initialize storage directories."""
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(f"{self.storage_path}/sessions", exist_ok=True)
        os.makedirs(f"{self.storage_path}/knowledge", exist_ok=True)
        os.makedirs(f"{self.storage_path}/context", exist_ok=True)
    
    def _load_persistent_memory(self):
        """Load persistent memory from storage."""
        try:
            # Load knowledge base
            knowledge_file = f"{self.storage_path}/knowledge/base.json"
            if os.path.exists(knowledge_file):
                with open(knowledge_file, 'r') as f:
                    self.knowledge_base = json.load(f)
                self.logger.info(f"Loaded {len(self.knowledge_base)} knowledge items")
            
            # Load context cache
            context_file = f"{self.storage_path}/context/cache.json"
            if os.path.exists(context_file):
                with open(context_file, 'r') as f:
                    self.context_cache = json.load(f)
                self.logger.info(f"Loaded {len(self.context_cache)} context items")
                
        except Exception as e:
            self.logger.error(f"Failed to load persistent memory: {e}")
    
    async def store_interaction(self, session_id: str, user_message: str, assistant_response: str, context: Dict = None):
        """Store a user-assistant interaction."""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'assistant_response': assistant_response,
            'context': context or {},
            'session_id': session_id
        }
        
        # Add to short-term memory
        if session_id not in self.short_term_memory:
            self.short_term_memory[session_id] = []
        
        self.short_term_memory[session_id].append(interaction)
        
        # Update context cache
        await self._update_context_cache(session_id, interaction)
        
        # Extract and store knowledge
        await self._extract_knowledge(interaction)
        
        # Clean up old memory if needed
        await self._cleanup_memory()
        
        self.logger.debug(f"Stored interaction for session {session_id}")
    
    async def get_session_context(self, session_id: str, max_interactions: int = 10) -> List[Dict]:
        """Get recent context for a session."""
        if session_id not in self.short_term_memory:
            # Try loading from persistent storage
            await self._load_session_from_storage(session_id)
        
        session_memory = self.short_term_memory.get(session_id, [])
        
        # Return most recent interactions
        return session_memory[-max_interactions:] if session_memory else []
    
    async def get_relevant_knowledge(self, query: str, max_items: int = 5) -> List[Dict]:
        """Retrieve relevant knowledge items for a query."""
        if not self.knowledge_base:
            return []
        
        # Simple keyword-based matching (can be enhanced with semantic search)
        query_words = set(query.lower().split())
        relevant_items = []
        
        for key, knowledge_item in self.knowledge_base.items():
            # Calculate relevance score
            item_text = f"{knowledge_item.get('content', '')} {knowledge_item.get('tags', [])}".lower()
            item_words = set(item_text.split())
            
            # Calculate word overlap
            overlap = len(query_words.intersection(item_words))
            if overlap > 0:
                relevance_score = overlap / len(query_words)
                relevant_items.append({
                    'knowledge_item': knowledge_item,
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance and return top items
        relevant_items.sort(key=lambda x: x['relevance_score'], reverse=True)
        return [item['knowledge_item'] for item in relevant_items[:max_items]]
    
    async def store_knowledge(self, knowledge_type: str, content: str, tags: List[str] = None, metadata: Dict = None):
        """Store a knowledge item."""
        knowledge_id = f"{knowledge_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        knowledge_item = {
            'id': knowledge_id,
            'type': knowledge_type,
            'content': content,
            'tags': tags or [],
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'access_count': 0,
            'last_accessed': None
        }
        
        self.knowledge_base[knowledge_id] = knowledge_item
        
        # Persist to storage
        await self._save_knowledge_base()
        
        self.logger.info(f"Stored knowledge item: {knowledge_id}")
    
    async def update_context(self, session_id: str, key: str, value: Any):
        """Update context for a session."""
        if session_id not in self.context_cache:
            self.context_cache[session_id] = {}
        
        self.context_cache[session_id][key] = {
            'value': value,
            'updated_at': datetime.now().isoformat()
        }
        
        # Persist context cache periodically
        if len(self.context_cache) % 50 == 0:  # Every 50 updates
            await self._save_context_cache()
    
    async def get_context(self, session_id: str, key: str = None) -> Any:
        """Get context for a session."""
        session_context = self.context_cache.get(session_id, {})
        
        if key:
            context_item = session_context.get(key)
            return context_item['value'] if context_item else None
        
        # Return all context with values only
        return {k: v['value'] for k, v in session_context.items()}
    
    async def archive_session(self, session_data: Dict):
        """Archive a completed session."""
        session_id = session_data['id']
        
        # Save session to persistent storage
        session_file = f"{self.storage_path}/sessions/{session_id}.json"
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Remove from short-term memory
            if session_id in self.short_term_memory:
                del self.short_term_memory[session_id]
            
            # Keep context in cache for a while longer
            # (context cleanup happens in _cleanup_memory)
            
            self.logger.info(f"Archived session {session_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to archive session {session_id}: {e}")
    
    async def search_memory(self, query: str, memory_types: List[str] = None, max_results: int = 10) -> List[Dict]:
        """Search across all memory types."""
        results = []
        
        memory_types = memory_types or ['interactions', 'knowledge', 'context']
        
        # Search interactions
        if 'interactions' in memory_types:
            interaction_results = await self._search_interactions(query, max_results // 3)
            results.extend(interaction_results)
        
        # Search knowledge
        if 'knowledge' in memory_types:
            knowledge_results = await self.get_relevant_knowledge(query, max_results // 3)
            results.extend([{'type': 'knowledge', 'data': k} for k in knowledge_results])
        
        # Search context
        if 'context' in memory_types:
            context_results = await self._search_context(query, max_results // 3)
            results.extend(context_results)
        
        # Sort by relevance (if available) and timestamp
        results.sort(key=lambda x: (
            x.get('relevance_score', 0),
            x.get('data', {}).get('timestamp', '')
        ), reverse=True)
        
        return results[:max_results]
    
    async def _search_interactions(self, query: str, max_results: int) -> List[Dict]:
        """Search through stored interactions."""
        query_words = set(query.lower().split())
        results = []
        
        for session_id, interactions in self.short_term_memory.items():
            for interaction in interactions:
                # Search in user message and assistant response
                text = f"{interaction['user_message']} {interaction['assistant_response']}".lower()
                text_words = set(text.split())
                
                overlap = len(query_words.intersection(text_words))
                if overlap > 0:
                    relevance_score = overlap / len(query_words)
                    results.append({
                        'type': 'interaction',
                        'data': interaction,
                        'relevance_score': relevance_score
                    })
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:max_results]
    
    async def _search_context(self, query: str, max_results: int) -> List[Dict]:
        """Search through context cache."""
        query_words = set(query.lower().split())
        results = []
        
        for session_id, context in self.context_cache.items():
            for key, context_item in context.items():
                # Search in context key and value
                text = f"{key} {str(context_item['value'])}".lower()
                text_words = set(text.split())
                
                overlap = len(query_words.intersection(text_words))
                if overlap > 0:
                    relevance_score = overlap / len(query_words)
                    results.append({
                        'type': 'context',
                        'data': {
                            'session_id': session_id,
                            'key': key,
                            'value': context_item['value'],
                            'updated_at': context_item['updated_at']
                        },
                        'relevance_score': relevance_score
                    })
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:max_results]
    
    async def _update_context_cache(self, session_id: str, interaction: Dict):
        """Update context cache based on interaction."""
        # Extract potential context from the interaction
        user_message = interaction['user_message'].lower()
        
        # Update session activity
        await self.update_context(session_id, 'last_activity', datetime.now().isoformat())
        
        # Extract entities and update context
        entities = self._extract_entities_from_text(user_message)
        for entity_type, entity_value in entities.items():
            await self.update_context(session_id, f'entity_{entity_type}', entity_value)
    
    def _extract_entities_from_text(self, text: str) -> Dict[str, str]:
        """Extract entities from text for context storage."""
        entities = {}
        
        # Simple entity extraction (can be enhanced)
        import re
        
        # Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if urls:
            entities['url'] = urls[0]
        
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if emails:
            entities['email'] = emails[0]
        
        # Extract potential names (capitalized words)
        names = re.findall(r'\b[A-Z][a-z]+\b', text)
        if names:
            entities['name'] = ' '.join(names[:2])  # First two names
        
        return entities
    
    async def _extract_knowledge(self, interaction: Dict):
        """Extract knowledge from interactions for storage."""
        user_message = interaction['user_message']
        assistant_response = interaction['assistant_response']
        
        # Look for knowledge indicators
        if any(indicator in user_message.lower() for indicator in ['what is', 'how to', 'explain', 'define']):
            # This looks like a knowledge request/response
            await self.store_knowledge(
                knowledge_type='qa',
                content=f"Q: {user_message}\nA: {assistant_response}",
                tags=['conversation', 'qa'],
                metadata={'session_id': interaction['session_id']}
            )
        
        # Extract code snippets
        if '```' in assistant_response:
            code_blocks = re.findall(r'```(\w+)?\n(.*?)```', assistant_response, re.DOTALL)
            for lang, code in code_blocks:
                await self.store_knowledge(
                    knowledge_type='code',
                    content=code.strip(),
                    tags=['code', lang or 'unknown'],
                    metadata={'session_id': interaction['session_id'], 'language': lang}
                )
    
    async def _cleanup_memory(self):
        """Clean up old memory items."""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=self.max_session_age_hours)
        
        # Clean up short-term memory
        sessions_to_remove = []
        for session_id, interactions in self.short_term_memory.items():
            if not interactions:
                sessions_to_remove.append(session_id)
                continue
            
            # Check if session is too old
            last_interaction = interactions[-1]
            interaction_time = datetime.fromisoformat(last_interaction['timestamp'])
            
            if interaction_time < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.short_term_memory[session_id]
            if session_id in self.context_cache:
                del self.context_cache[session_id]
        
        # Limit memory size
        if len(self.short_term_memory) > self.max_short_term_items:
            # Remove oldest sessions
            oldest_sessions = sorted(
                self.short_term_memory.items(),
                key=lambda x: x[1][-1]['timestamp'] if x[1] else ''
            )[:len(self.short_term_memory) - self.max_short_term_items]
            
            for session_id, _ in oldest_sessions:
                del self.short_term_memory[session_id]
        
        if sessions_to_remove:
            self.logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
    
    async def _save_knowledge_base(self):
        """Save knowledge base to persistent storage."""
        try:
            knowledge_file = f"{self.storage_path}/knowledge/base.json"
            with open(knowledge_file, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save knowledge base: {e}")
    
    async def _save_context_cache(self):
        """Save context cache to persistent storage."""
        try:
            context_file = f"{self.storage_path}/context/cache.json"
            with open(context_file, 'w') as f:
                json.dump(self.context_cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save context cache: {e}")
    
    async def _load_session_from_storage(self, session_id: str):
        """Load session from persistent storage."""
        session_file = f"{self.storage_path}/sessions/{session_id}.json"
        
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Convert to interaction format
                interactions = []
                for msg in session_data.get('messages', []):
                    if msg['type'] == 'user':
                        # Find corresponding assistant message
                        assistant_msg = next(
                            (m for m in session_data['messages'] 
                             if m['id'] == msg['id'] + 1 and m['type'] == 'assistant'),
                            None
                        )
                        
                        if assistant_msg:
                            interactions.append({
                                'timestamp': msg['timestamp'],
                                'user_message': msg['content'],
                                'assistant_response': assistant_msg['content'],
                                'context': assistant_msg.get('metadata', {}),
                                'session_id': session_id
                            })
                
                self.short_term_memory[session_id] = interactions
                
            except Exception as e:
                self.logger.error(f"Failed to load session {session_id}: {e}")
    
    def get_usage_stats(self) -> Dict:
        """Get memory usage statistics."""
        return {
            'short_term_sessions': len(self.short_term_memory),
            'short_term_interactions': sum(len(interactions) for interactions in self.short_term_memory.values()),
            'context_cache_items': len(self.context_cache),
            'knowledge_base_items': len(self.knowledge_base),
            'storage_path': self.storage_path
        }
    
    async def export_memory(self, export_path: str, include_sessions: bool = True, include_knowledge: bool = True):
        """Export memory data for backup or analysis."""
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'stats': self.get_usage_stats()
        }
        
        if include_sessions:
            export_data['sessions'] = self.short_term_memory
            export_data['context'] = self.context_cache
        
        if include_knowledge:
            export_data['knowledge_base'] = self.knowledge_base
        
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Memory exported to {export_path}")

# Import for entity extraction
import re