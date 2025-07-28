"""
Module de gestion OpenAI pour l'analyse d'intention et l'extraction de paramètres
"""

import json
import os
from typing import Dict, Any, Optional, List
from openai import OpenAI
from pydantic import BaseModel

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
        {{"type": "equipment_id", "value": "EQ001", "confidence": 0.9}}
    ],
    "action_type": "get"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse la réponse JSON
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
                return IntentAnalysis(**result)
            except json.JSONDecodeError:
                # Fallback si le JSON n'est pas valide
                return self._fallback_analysis(user_query)
                
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return self._fallback_analysis(user_query)
    
    def _fallback_analysis(self, user_query: str) -> IntentAnalysis:
        """Analyse de fallback basée sur des mots-clés"""
        query_lower = user_query.lower()
        
        # Analyse basique par mots-clés
        if "ordre" in query_lower or "order" in query_lower:
            intent = "get_open_orders"
            action_type = "get"
        elif "équipement" in query_lower or "equipment" in query_lower:
            intent = "get_equipment_list"
            action_type = "get"
        elif "notification" in query_lower:
            if "créer" in query_lower or "create" in query_lower:
                intent = "create_notification"
                action_type = "create"
            else:
                intent = "get_notifications"
                action_type = "get"
        elif "centre" in query_lower or "work center" in query_lower:
            intent = "get_work_centers"
            action_type = "get"
        elif "emplacement" in query_lower or "location" in query_lower:
            intent = "get_functional_locations"
            action_type = "get"
        elif "matériau" in query_lower or "material" in query_lower:
            intent = "get_materials"
            action_type = "get"
        else:
            intent = "unknown"
            action_type = "unknown"
        
        return IntentAnalysis(
            intent=intent,
            confidence=0.5,
            parameters={},
            entities=[],
            action_type=action_type
        )
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extrait les entités du texte"""
        entities = []
        
        # Extraction basique d'IDs (format: lettres + chiffres)
        import re
        id_pattern = r'\b[A-Z]{2,}\d+\b'
        ids = re.findall(id_pattern, text)
        
        for id_match in ids:
            entities.append({
                "type": "id",
                "value": id_match,
                "confidence": 0.8
            })
        
        return entities 