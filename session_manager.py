"""
Gestionnaire de session pour maintenir le contexte utilisateur
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class SessionContext(BaseModel):
    """Contexte de session utilisateur"""
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    conversation_history: List[Dict[str, Any]] = []
    current_context: Dict[str, Any] = {}
    preferences: Dict[str, Any] = {}

class SessionManager:
    """Gestionnaire de sessions utilisateur"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionContext] = {}
        self.session_timeout = timedelta(hours=24)  # 24 heures
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Crée une nouvelle session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = SessionContext(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            last_activity=now
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Récupère une session par son ID"""
        session = self.sessions.get(session_id)
        if session:
            # Vérifier si la session n'a pas expiré
            if datetime.now() - session.last_activity > self.session_timeout:
                self.delete_session(session_id)
                return None
            
            # Mettre à jour l'activité
            session.last_activity = datetime.now()
            return session
        return None
    
    def update_session_context(self, session_id: str, context_update: Dict[str, Any]) -> bool:
        """Met à jour le contexte d'une session"""
        session = self.get_session(session_id)
        if session:
            session.current_context.update(context_update)
            session.last_activity = datetime.now()
            return True
        return False
    
    def add_conversation_history(self, session_id: str, user_query: str, response: Dict[str, Any]) -> bool:
        """Ajoute une entrée à l'historique de conversation"""
        session = self.get_session(session_id)
        if session:
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_query": user_query,
                "response": response,
                "intent": response.get("intent"),
                "confidence": response.get("confidence", 0.0)
            }
            session.conversation_history.append(history_entry)
            
            # Limiter l'historique à 50 entrées
            if len(session.conversation_history) > 50:
                session.conversation_history = session.conversation_history[-50:]
            
            session.last_activity = datetime.now()
            return True
        return False
    
    def get_conversation_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Récupère le contexte de conversation pour aider à l'analyse d'intention"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Analyser l'historique récent pour extraire le contexte
        recent_history = session.conversation_history[-5:]  # 5 dernières entrées
        
        context = {
            "current_session": session.current_context,
            "recent_intents": [entry.get("intent") for entry in recent_history if entry.get("intent")],
            "mentioned_entities": self._extract_entities_from_history(recent_history),
            "user_preferences": session.preferences,
            "session_duration": (datetime.now() - session.created_at).total_seconds()
        }
        
        return context
    
    def _extract_entities_from_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrait les entités mentionnées dans l'historique"""
        entities = []
        
        for entry in history:
            response = entry.get("response", {})
            if "entities" in response:
                entities.extend(response["entities"])
        
        # Dédupliquer les entités
        unique_entities = []
        seen_values = set()
        
        for entity in entities:
            if entity.get("value") not in seen_values:
                unique_entities.append(entity)
                seen_values.add(entity.get("value"))
        
        return unique_entities
    
    def delete_session(self, session_id: str) -> bool:
        """Supprime une session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Nettoie les sessions expirées et retourne le nombre de sessions supprimées"""
        now = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if now - session.last_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        return len(expired_sessions)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques des sessions"""
        now = datetime.now()
        active_sessions = 0
        total_conversations = 0
        
        for session in self.sessions.values():
            if now - session.last_activity <= self.session_timeout:
                active_sessions += 1
                total_conversations += len(session.conversation_history)
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "total_conversations": total_conversations,
            "session_timeout_hours": self.session_timeout.total_seconds() / 3600
        } 