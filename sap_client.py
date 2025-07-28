"""
Client SAP PM pour les interactions avec l'API SAP Plant Maintenance
"""

import httpx
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"SAP PM Client initialisé avec l'URL: {self.base_url}")
    
    async def __aenter__(self):
        """Support pour le context manager"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fermeture propre du client"""
        await self.close()
    
    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()
        logger.info("SAP PM Client fermé")
    
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
            logger.debug(f"Requête {method} vers {url}")
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Tentative de parsing JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.warning(f"Réponse non-JSON reçue de {url}")
                return {"message": response.text, "status": response.status_code}
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP {e.response.status_code} pour {url}: {e.response.text}")
            raise Exception(f"Erreur API SAP PM: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Erreur de requête pour {url}: {str(e)}")
            raise Exception(f"Erreur de communication avec SAP PM: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur inattendue pour {url}: {str(e)}")
            raise
    
    # === ORDRES DE TRAVAIL ===
    
    async def create_order(self, description: str, equipment: str, priority: str = "MEDIUM", 
                          due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Crée un nouvel ordre de travail
        
        Args:
            description: Description du travail à effectuer
            equipment: ID de l'équipement concerné
            priority: Priorité (LOW, MEDIUM, HIGH, CRITICAL)
            due_date: Date d'échéance (format YYYY-MM-DD)
        
        Returns:
            Détails de l'ordre créé
        """
        data = {
            "description": description,
            "equipment": equipment,
            "priority": priority.upper()
        }
        
        if due_date:
            data["due_date"] = due_date
        
        return await self._make_request("POST", "/orders", json=data)
    
    async def get_open_work_orders(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Récupère les ordres de travail ouverts
        
        Args:
            limit: Nombre maximum d'ordres à récupérer
            offset: Décalage pour la pagination
        
        Returns:
            Liste des ordres ouverts
        """
        params = {"limit": limit, "offset": offset}
        return await self._make_request("GET", "/orders/open", params=params)
    
    # === NOTIFICATIONS ===
    
    async def create_notification(self, equipment: str, text: str, priority: str = "MEDIUM") -> Dict[str, Any]:
        """
        Crée une nouvelle notification
        
        Args:
            equipment: ID de l'équipement concerné
            text: Texte de la notification
            priority: Priorité (LOW, MEDIUM, HIGH, CRITICAL)
        
        Returns:
            Détails de la notification créée
        """
        data = {
            "equipment": equipment,
            "text": text,
            "priority": priority.upper()
        }
        
        return await self._make_request("POST", "/notifications", json=data)
    
    async def get_notifications(self, status: str = "OPEN", limit: int = 50) -> Dict[str, Any]:
        """
        Récupère les notifications
        
        Args:
            status: Statut des notifications (OPEN, CLOSED, ALL)
            limit: Nombre maximum de notifications à récupérer
        
        Returns:
            Liste des notifications
        """
        params = {"status": status.upper(), "limit": limit}
        return await self._make_request("GET", "/notifications", params=params)
    
    # === ÉQUIPEMENTS ===
    
    async def get_equipment_by_id(self, equipment_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'un équipement par son ID
        
        Args:
            equipment_id: ID de l'équipement
        
        Returns:
            Détails de l'équipement
        """
        return await self._make_request("GET", f"/equipment/{equipment_id}")
    
    async def get_equipment_list(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Récupère la liste des équipements
        
        Args:
            limit: Nombre maximum d'équipements à récupérer
            offset: Décalage pour la pagination
        
        Returns:
            Liste des équipements
        """
        params = {"limit": limit, "offset": offset}
        return await self._make_request("GET", "/equipment", params=params)
    
    async def get_functional_locations(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les emplacements fonctionnels
        
        Args:
            limit: Nombre maximum d'emplacements à récupérer
        
        Returns:
            Liste des emplacements fonctionnels
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/functional-locations", params=params)
    
    # === CENTRES DE TRAVAIL ===
    
    async def get_work_centers(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les centres de travail
        
        Args:
            limit: Nombre maximum de centres à récupérer
        
        Returns:
            Liste des centres de travail
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/work-centers", params=params)
    
    # === MATÉRIAUX ===
    
    async def get_materials(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les matériaux
        
        Args:
            limit: Nombre maximum de matériaux à récupérer
        
        Returns:
            Liste des matériaux
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/materials", params=params)
    
    # === CATALOGUES ===
    
    async def get_catalogs(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les catalogues de maintenance
        
        Args:
            limit: Nombre maximum de catalogues à récupérer
        
        Returns:
            Liste des catalogues
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/catalogs", params=params)
    
    # === CARACTÉRISTIQUES ===
    
    async def get_characteristics(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les caractéristiques techniques
        
        Args:
            limit: Nombre maximum de caractéristiques à récupérer
        
        Returns:
            Liste des caractéristiques
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/characteristics", params=params)
    
    # === STRATÉGIES ===
    
    async def get_maintenance_strategies(self, limit: int = 100) -> Dict[str, Any]:
        """
        Récupère les stratégies de maintenance
        
        Args:
            limit: Nombre maximum de stratégies à récupérer
        
        Returns:
            Liste des stratégies
        """
        params = {"limit": limit}
        return await self._make_request("GET", "/maintenance-strategies", params=params)
    
    # === MÉTHODES UTILITAIRES ===
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Vérifie la santé de l'API SAP PM
        
        Returns:
            Statut de santé de l'API
        """
        try:
            return await self._make_request("GET", "/health")
        except Exception as e:
            logger.error(f"Erreur lors du health check: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def get_api_info(self) -> Dict[str, Any]:
        """
        Récupère les informations sur l'API
        
        Returns:
            Informations sur l'API
        """
        return await self._make_request("GET", "/info")


# Instance globale du client (pour compatibilité)
sap_client = SAPPMClient() 