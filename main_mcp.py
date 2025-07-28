"""
Serveur MCP (Model Context Protocol) pour SAP PM
Agent intelligent qui interprète les requêtes en langage naturel et interagit avec l'API SAP PM
"""

import os
import asyncio
import json
import uuid
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'application
app = FastAPI(
    title="SAP PM MCP Server",
    description="Serveur MCP pour interagir avec l'API SAP Plant Maintenance via langage naturel",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CLASSES INTÉGRÉES =====

class IntentAnalysis(BaseModel):
    """Modèle pour l'analyse d'intention"""
    intent: str
    confidence: float
    parameters: Dict[str, Any]
    entities: List[Dict[str, Any]]
    action_type: str  # 'get', 'create', 'update', 'delete'

class OpenAIHandler:
    """Gestionnaire OpenAI pour l'analyse d'intention"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Définition des intents supportés
        self.supported_intents = {
            "get_open_orders": {
                "description": "Récupérer les ordres de maintenance ouverts",
                "parameters": ["status", "priority", "equipment_id", "work_center_id"]
            },
            "get_equipment_by_id": {
                "description": "Récupérer un équipement par son ID",
                "parameters": ["equipment_id"]
            },
            "get_equipment_list": {
                "description": "Récupérer la liste des équipements",
                "parameters": ["functional_location_id", "equipment_type", "status"]
            },
            "create_notification": {
                "description": "Créer une nouvelle notification",
                "parameters": ["equipment_id", "functional_location_id", "short_text", "long_text", "priority"]
            },
            "create_order": {
                "description": "Créer un nouvel ordre de maintenance",
                "parameters": ["equipment_id", "functional_location_id", "work_center_id", "description", "order_type", "priority", "planned_start_date", "planned_end_date", "estimated_hours"]
            },
            "get_notifications": {
                "description": "Récupérer les notifications",
                "parameters": ["status", "priority", "equipment_id", "functional_location_id"]
            },
            "get_work_centers": {
                "description": "Récupérer les centres de travail",
                "parameters": ["hierarchy_id", "cost_center"]
            },
            "get_functional_locations": {
                "description": "Récupérer les emplacements fonctionnels",
                "parameters": ["hierarchy_id", "equipment_id"]
            },
            "get_materials": {
                "description": "Récupérer les matériaux",
                "parameters": ["material_type", "status"]
            },
            "get_maintenance_strategies": {
                "description": "Récupérer les stratégies de maintenance",
                "parameters": ["equipment_id", "strategy_type"]
            },
            "get_catalogs": {
                "description": "Récupérer les catalogues",
                "parameters": ["code_group", "code"]
            },
            "get_characteristics": {
                "description": "Récupérer les caractéristiques",
                "parameters": ["name", "unit_of_measurement"]
            }
        }
    
    def analyze_intent(self, user_query: str) -> IntentAnalysis:
        """Analyse l'intention de l'utilisateur"""
        
        system_prompt = f"""
Tu es un assistant spécialisé dans l'analyse d'intentions pour un système SAP Plant Maintenance.
Tu dois analyser la requête de l'utilisateur et extraire l'intention et les paramètres.

Intents supportés:
{json.dumps(self.supported_intents, indent=2, ensure_ascii=False)}

Instructions:
1. Identifie l'intention principale de la requête
2. Extrais tous les paramètres pertinents
3. Identifie les entités mentionnées (IDs, noms, etc.)
4. Détermine le type d'action (get, create, update, delete)
5. Retourne une réponse JSON structurée

Format de réponse attendu:
{{
    "intent": "nom_de_l_intent",
    "confidence": 0.95,
    "parameters": {{
        "param1": "valeur1",
        "param2": "valeur2"
    }},
    "entities": [
        {{"type": "equipment_id", "value": "EQ-001"}},
        {{"type": "priority", "value": "HIGH"}}
    ],
    "action_type": "get"
}}

Requête utilisateur: {user_query}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
                return IntentAnalysis(**result)
            except json.JSONDecodeError:
                return self._fallback_analysis(user_query)
                
        except Exception as e:
            return self._fallback_analysis(user_query)
    
    def _fallback_analysis(self, user_query: str) -> IntentAnalysis:
        """Analyse de fallback en cas d'erreur OpenAI"""
        user_query_lower = user_query.lower()
        
        # Analyse simple basée sur les mots-clés
        if "ordre" in user_query_lower or "work order" in user_query_lower:
            return IntentAnalysis(
                intent="get_open_orders",
                confidence=0.7,
                parameters={},
                entities=[],
                action_type="get"
            )
        elif "équipement" in user_query_lower or "equipment" in user_query_lower:
            return IntentAnalysis(
                intent="get_equipment_list",
                confidence=0.7,
                parameters={},
                entities=[],
                action_type="get"
            )
        elif "notification" in user_query_lower:
            return IntentAnalysis(
                intent="get_notifications",
                confidence=0.7,
                parameters={},
                entities=[],
                action_type="get"
            )
        else:
            return IntentAnalysis(
                intent="unknown",
                confidence=0.1,
                parameters={},
                entities=[],
                action_type="unknown"
            )

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
        return entities
    
    def delete_session(self, session_id: str) -> bool:
        """Supprime une session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Nettoie les sessions expirées"""
        expired_count = 0
        current_time = datetime.now()
        
        for session_id in list(self.sessions.keys()):
            session = self.sessions[session_id]
            if current_time - session.last_activity > self.session_timeout:
                self.delete_session(session_id)
                expired_count += 1
        
        return expired_count
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques des sessions"""
        current_time = datetime.now()
        active_sessions = 0
        total_conversations = 0
        
        for session in self.sessions.values():
            if current_time - session.last_activity <= self.session_timeout:
                active_sessions += 1
                total_conversations += len(session.conversation_history)
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "total_conversations": total_conversations,
            "expired_sessions_cleaned": self.cleanup_expired_sessions()
        }

class SAPPMClient:
    """
    Client asynchrone pour interagir avec l'API SAP Plant Maintenance
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialise le client SAP PM
        
        Args:
            base_url: URL de base de l'API SAP PM
        """
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        """Support pour le context manager"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fermeture propre du client"""
        await self.close()
    
    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Effectue une requête HTTP vers l'API SAP PM
        
        Args:
            method: Méthode HTTP (GET, POST, PUT, DELETE)
            endpoint: Point de terminaison de l'API
            **kwargs: Arguments supplémentaires pour la requête
        
        Returns:
            Réponse de l'API sous forme de dictionnaire
        
        Raises:
            Exception: En cas d'erreur de communication avec l'API
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Tentative de parsing JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"message": response.text, "status": response.status_code}
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"Erreur API SAP PM: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Erreur de communication avec SAP PM: {str(e)}")
        except Exception as e:
            raise
    
    # === MÉTHODES SAP PM ===
    
    async def get_open_orders(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les ordres de maintenance ouverts"""
        try:
            result = await self._make_request("GET", "/orders/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_equipment_by_id(self, equipment_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un équipement par son ID"""
        try:
            result = await self._make_request("GET", f"/equipment/{equipment_id}")
            return result
        except Exception:
            return None
    
    async def get_equipment_list(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère la liste des équipements"""
        try:
            result = await self._make_request("GET", "/equipment/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def create_notification(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle notification"""
        try:
            result = await self._make_request("POST", "/notifications/", json=parameters)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def create_order(self, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crée un nouvel ordre de maintenance"""
        try:
            result = await self._make_request("POST", "/orders/", json=parameters)
            return result
        except Exception:
            return None
    
    async def get_notifications(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les notifications"""
        try:
            result = await self._make_request("GET", "/notifications/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_work_centers(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les centres de travail"""
        try:
            result = await self._make_request("GET", "/work-centers/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_functional_locations(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les emplacements fonctionnels"""
        try:
            result = await self._make_request("GET", "/functional-locations/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_materials(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les matériaux"""
        try:
            result = await self._make_request("GET", "/materials/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_maintenance_strategies(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les stratégies de maintenance"""
        try:
            result = await self._make_request("GET", "/maintenance-strategies/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_catalogs(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les catalogues"""
        try:
            result = await self._make_request("GET", "/catalogs/")
            return result if isinstance(result, list) else []
        except Exception:
            return []
    
    async def get_characteristics(self, **parameters) -> List[Dict[str, Any]]:
        """Récupère les caractéristiques"""
        try:
            result = await self._make_request("GET", "/characteristics/")
            return result if isinstance(result, list) else []
        except Exception:
            return []

# Initialisation des composants
openai_handler = OpenAIHandler()
session_manager = SessionManager()

# Modèles Pydantic
class AskRequest(BaseModel):
    """Requête utilisateur"""
    query: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class AskResponse(BaseModel):
    """Réponse à la requête utilisateur"""
    success: bool
    intent: str
    confidence: float
    response: Dict[str, Any]
    session_id: str
    timestamp: str
    context: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class SessionRequest(BaseModel):
    """Requête de création de session"""
    user_id: Optional[str] = None

class SessionResponse(BaseModel):
    """Réponse de session"""
    session_id: str
    created_at: str
    user_id: Optional[str] = None

# Fonctions utilitaires
async def get_sap_pm_client() -> SAPPMClient:
    """Retourne un client SAP PM"""
    return SAPPMClient()

async def process_intent(intent_analysis: IntentAnalysis, sap_client: SAPPMClient, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Traite l'intention et exécute l'action correspondante"""
    
    intent = intent_analysis.intent
    parameters = intent_analysis.parameters
    
    # Enrichir les paramètres avec le contexte de session
    if session_context:
        # Utiliser les entités mentionnées précédemment si disponibles
        mentioned_entities = session_context.get("mentioned_entities", [])
        for entity in mentioned_entities:
            if entity.get("type") == "equipment_id" and "equipment_id" not in parameters:
                parameters["equipment_id"] = entity.get("value")
    
    try:
        if intent == "get_open_orders":
            result = await sap_client.get_open_orders(**parameters)
            return {
                "action": "get_open_orders",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} ordres de maintenance ouverts"
            }
        
        elif intent == "get_equipment_by_id":
            equipment_id = parameters.get("equipment_id")
            if not equipment_id:
                raise ValueError("ID d'équipement requis")
            
            result = await sap_client.get_equipment_by_id(equipment_id)
            if result:
                return {
                    "action": "get_equipment_by_id",
                    "data": result,
                    "message": f"Équipement {equipment_id} récupéré avec succès"
                }
            else:
                return {
                    "action": "get_equipment_by_id",
                    "data": None,
                    "message": f"Équipement {equipment_id} non trouvé"
                }
        
        elif intent == "get_equipment_list":
            result = await sap_client.get_equipment_list(**parameters)
            return {
                "action": "get_equipment_list",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} équipements"
            }
        
        elif intent == "create_notification":
            result = await sap_client.create_notification(parameters)
            return {
                "action": "create_notification",
                "data": result,
                "message": f"Notification {result.get('id')} créée avec succès"
            }
        
        elif intent == "create_order":
            result = await sap_client.create_order(parameters)
            if result:
                return {
                    "action": "create_order",
                    "data": result,
                    "message": f"Ordre de maintenance {result.get('id')} créé avec succès"
                }
            else:
                return {
                    "action": "create_order",
                    "data": None,
                    "message": "Erreur lors de la création de l'ordre de maintenance"
                }
        
        elif intent == "get_notifications":
            result = await sap_client.get_notifications(**parameters)
            return {
                "action": "get_notifications",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} notifications"
            }
        
        elif intent == "get_work_centers":
            result = await sap_client.get_work_centers(**parameters)
            return {
                "action": "get_work_centers",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} centres de travail"
            }
        
        elif intent == "get_functional_locations":
            result = await sap_client.get_functional_locations(**parameters)
            return {
                "action": "get_functional_locations",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} emplacements fonctionnels"
            }
        
        elif intent == "get_materials":
            result = await sap_client.get_materials(**parameters)
            return {
                "action": "get_materials",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} matériaux"
            }
        
        elif intent == "get_maintenance_strategies":
            result = await sap_client.get_maintenance_strategies(**parameters)
            return {
                "action": "get_maintenance_strategies",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} stratégies de maintenance"
            }
        
        elif intent == "get_catalogs":
            result = await sap_client.get_catalogs(**parameters)
            return {
                "action": "get_catalogs",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} catalogues"
            }
        
        elif intent == "get_characteristics":
            result = await sap_client.get_characteristics(**parameters)
            return {
                "action": "get_characteristics",
                "data": result,
                "count": len(result),
                "message": f"Récupération de {len(result)} caractéristiques"
            }
        
        else:
            return {
                "action": "unknown_intent",
                "data": None,
                "message": f"Intention '{intent}' non reconnue ou non implémentée"
            }
    
    except Exception as e:
        return {
            "action": intent,
            "data": None,
            "message": f"Erreur lors de l'exécution de l'action: {str(e)}"
        }

# Endpoints
@app.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    sap_client: SAPPMClient = Depends(get_sap_pm_client)
):
    """Endpoint principal pour poser des questions en langage naturel"""
    
    try:
        # Gestion de la session
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session(request.user_id)
        
        # Récupérer le contexte de session
        session_context = session_manager.get_conversation_context(session_id)
        
        # Analyser l'intention avec OpenAI
        intent_analysis = openai_handler.analyze_intent(request.query)
        
        # Traiter l'intention
        result = await process_intent(intent_analysis, sap_client, session_context)
        
        # Préparer la réponse
        response_data = {
            "intent": intent_analysis.intent,
            "confidence": intent_analysis.confidence,
            "parameters": intent_analysis.parameters,
            "entities": intent_analysis.entities,
            "action_type": intent_analysis.action_type,
            "result": result
        }
        
        # Mettre à jour le contexte de session
        if session_context:
            session_manager.update_session_context(session_id, {
                "last_intent": intent_analysis.intent,
                "last_parameters": intent_analysis.parameters
            })
        
        # Ajouter à l'historique de conversation
        session_manager.add_conversation_history(session_id, request.query, response_data)
        
        return AskResponse(
            success=True,
            intent=intent_analysis.intent,
            confidence=intent_analysis.confidence,
            response=response_data,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            context=session_context
        )
    
    except Exception as e:
        return AskResponse(
            success=False,
            intent="error",
            confidence=0.0,
            response={},
            session_id=session_id if 'session_id' in locals() else None,
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@app.post("/session", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """Crée une nouvelle session utilisateur"""
    session_id = session_manager.create_session(request.user_id)
    session = session_manager.get_session(session_id)
    
    return SessionResponse(
        session_id=session_id,
        created_at=session.created_at.isoformat(),
        user_id=session.user_id
    )

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Récupère les informations d'une session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    return {
        "session_id": session.session_id,
        "user_id": session.user_id,
        "created_at": session.created_at.isoformat(),
        "last_activity": session.last_activity.isoformat(),
        "conversation_count": len(session.conversation_history),
        "current_context": session.current_context
    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Supprime une session"""
    success = session_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    return {"message": "Session supprimée avec succès"}

@app.get("/stats")
async def get_stats():
    """Récupère les statistiques du serveur"""
    return session_manager.get_session_stats()

@app.get("/health")
async def health_check():
    """Vérification de l'état du serveur"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "sap_pm_url": os.getenv("SAP_PM_API_URL", "http://localhost:8000")
    }

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "SAP PM MCP Server",
        "version": "1.0.0",
        "description": "Serveur MCP pour interagir avec l'API SAP Plant Maintenance",
        "endpoints": {
            "ask": "/ask - Poser une question en langage naturel",
            "session": "/session - Gérer les sessions utilisateur",
            "stats": "/stats - Statistiques du serveur",
            "health": "/health - État du serveur"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_mcp:app", host="0.0.0.0", port=8001, reload=True) 