"""
Outils SAP PM pour l'ADK (Agent Development Kit)
Transforme les fonctions du client SAP PM en outils utilisables par les agents
"""

import asyncio
from typing import Dict, Any, List, Optional
from adk.api.tool_manager import tool
from sap_pm_client import SAPPMClient

# Initialisation du client SAP PM
sap_client = SAPPMClient()

@tool
async def create_sap_work_order(
    description: str,
    equipment_id: str,
    priority: str = "MEDIUM",
    order_type: str = "PM01",
    work_center_id: str = None,
    planned_start_date: str = None,
    planned_end_date: str = None,
    estimated_hours: float = None
) -> str:
    """
    Crée un ordre de travail dans SAP PM.
    Utilisez cet outil lorsque vous devez créer une nouvelle tâche de maintenance.

    Args:
        description: Une description détaillée du travail à effectuer
        equipment_id: L'ID de l'équipement concerné
        priority: La priorité de l'ordre (LOW, MEDIUM, HIGH, CRITICAL)
        order_type: Type d'ordre (PM01 pour maintenance préventive, PM02 pour corrective)
        work_center_id: ID du centre de travail responsable
        planned_start_date: Date de début prévue (format: YYYY-MM-DD)
        planned_end_date: Date de fin prévue (format: YYYY-MM-DD)
        estimated_hours: Nombre d'heures estimées

    Returns:
        Une chaîne de caractères confirmant la création et l'ID du nouvel ordre
    """
    try:
        order_data = {
            "equipment_id": equipment_id,
            "description": description,
            "order_type": order_type,
            "priority": priority
        }
        
        if work_center_id:
            order_data["work_center_id"] = work_center_id
        if planned_start_date:
            order_data["planned_start_date"] = planned_start_date
        if planned_end_date:
            order_data["planned_end_date"] = planned_end_date
        if estimated_hours:
            order_data["estimated_hours"] = estimated_hours

        result = await sap_client.create_order(order_data)
        
        if result and result.get('id'):
            return f"✅ Ordre de travail créé avec succès. ID: {result['id']}, Description: {description}"
        else:
            return f"❌ Erreur lors de la création de l'ordre de travail: Aucun ID retourné"
            
    except Exception as e:
        return f"❌ Erreur lors de la création de l'ordre de travail: {str(e)}"

@tool
async def create_sap_notification(
    equipment_id: str,
    short_text: str,
    long_text: str = "",
    priority: str = "MEDIUM",
    functional_location_id: str = None
) -> str:
    """
    Crée une notification de maintenance dans SAP PM.

    Args:
        equipment_id: L'ID de l'équipement concerné
        short_text: Texte court de la notification
        long_text: Description détaillée (optionnel)
        priority: Priorité de la notification (LOW, MEDIUM, HIGH, CRITICAL)
        functional_location_id: ID de l'emplacement fonctionnel (optionnel)

    Returns:
        Confirmation de création avec l'ID de la notification
    """
    try:
        notification_data = {
            "equipment_id": equipment_id,
            "short_text": short_text,
            "long_text": long_text,
            "priority": priority
        }
        
        if functional_location_id:
            notification_data["functional_location_id"] = functional_location_id

        result = await sap_client.create_notification(notification_data)
        
        if result and result.get('id'):
            return f"✅ Notification créée avec succès. ID: {result['id']}, Texte: {short_text}"
        else:
            return f"❌ Erreur lors de la création de la notification: Aucun ID retourné"
            
    except Exception as e:
        return f"❌ Erreur lors de la création de la notification: {str(e)}"

@tool
async def get_equipment_details(equipment_id: str) -> str:
    """
    Récupère les détails d'un équipement spécifique depuis SAP.

    Args:
        equipment_id: L'ID technique de l'équipement à rechercher

    Returns:
        Une chaîne formatée avec les détails de l'équipement
    """
    try:
        details = await sap_client.get_equipment_by_id(equipment_id)
        
        if details:
            return f"📋 Détails pour l'équipement {equipment_id}:\n" + \
                   f"   Nom: {details.get('name', 'N/A')}\n" + \
                   f"   Type: {details.get('equipment_type', 'N/A')}\n" + \
                   f"   Statut: {details.get('status', 'N/A')}\n" + \
                   f"   Emplacement: {details.get('functional_location_id', 'N/A')}\n" + \
                   f"   Centre de travail: {details.get('work_center_id', 'N/A')}"
        else:
            return f"❌ Équipement {equipment_id} non trouvé"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération de l'équipement: {str(e)}"

@tool
async def get_open_work_orders(
    status: str = "OPEN",
    priority: str = None,
    equipment_id: str = None,
    work_center_id: str = None
) -> str:
    """
    Récupère les ordres de travail ouverts depuis SAP PM.

    Args:
        status: Statut des ordres à récupérer (OPEN, CLOSED, IN_PROGRESS)
        priority: Filtrer par priorité (LOW, MEDIUM, HIGH, CRITICAL)
        equipment_id: Filtrer par équipement
        work_center_id: Filtrer par centre de travail

    Returns:
        Liste formatée des ordres de travail
    """
    try:
        params = {"status": status}
        if priority:
            params["priority"] = priority
        if equipment_id:
            params["equipment_id"] = equipment_id
        if work_center_id:
            params["work_center_id"] = work_center_id

        orders = await sap_client.get_open_orders(**params)
        
        if orders:
            result = f"📋 {len(orders)} ordre(s) de travail trouvé(s):\n"
            for order in orders[:10]:  # Limiter à 10 pour la lisibilité
                result += f"   • ID: {order.get('id', 'N/A')} - {order.get('description', 'N/A')} " + \
                         f"(Priorité: {order.get('priority', 'N/A')})\n"
            
            if len(orders) > 10:
                result += f"   ... et {len(orders) - 10} autres ordres"
            
            return result
        else:
            return f"📭 Aucun ordre de travail trouvé avec les critères spécifiés"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des ordres: {str(e)}"

@tool
async def get_equipment_list(
    functional_location_id: str = None,
    equipment_type: str = None,
    status: str = None
) -> str:
    """
    Récupère la liste des équipements depuis SAP PM.

    Args:
        functional_location_id: Filtrer par emplacement fonctionnel
        equipment_type: Filtrer par type d'équipement
        status: Filtrer par statut

    Returns:
        Liste formatée des équipements
    """
    try:
        params = {}
        if functional_location_id:
            params["functional_location_id"] = functional_location_id
        if equipment_type:
            params["equipment_type"] = equipment_type
        if status:
            params["status"] = status

        equipment_list = await sap_client.get_equipment_list(**params)
        
        if equipment_list:
            result = f"📋 {len(equipment_list)} équipement(s) trouvé(s):\n"
            for equipment in equipment_list[:10]:  # Limiter à 10
                result += f"   • {equipment.get('id', 'N/A')} - {equipment.get('name', 'N/A')} " + \
                         f"({equipment.get('equipment_type', 'N/A')})\n"
            
            if len(equipment_list) > 10:
                result += f"   ... et {len(equipment_list) - 10} autres équipements"
            
            return result
        else:
            return f"📭 Aucun équipement trouvé avec les critères spécifiés"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des équipements: {str(e)}"

@tool
async def get_notifications(
    status: str = None,
    priority: str = None,
    equipment_id: str = None,
    functional_location_id: str = None
) -> str:
    """
    Récupère les notifications de maintenance depuis SAP PM.

    Args:
        status: Filtrer par statut
        priority: Filtrer par priorité
        equipment_id: Filtrer par équipement
        functional_location_id: Filtrer par emplacement fonctionnel

    Returns:
        Liste formatée des notifications
    """
    try:
        params = {}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if equipment_id:
            params["equipment_id"] = equipment_id
        if functional_location_id:
            params["functional_location_id"] = functional_location_id

        notifications = await sap_client.get_notifications(**params)
        
        if notifications:
            result = f"📋 {len(notifications)} notification(s) trouvée(s):\n"
            for notification in notifications[:10]:
                result += f"   • ID: {notification.get('id', 'N/A')} - {notification.get('short_text', 'N/A')} " + \
                         f"(Priorité: {notification.get('priority', 'N/A')})\n"
            
            if len(notifications) > 10:
                result += f"   ... et {len(notifications) - 10} autres notifications"
            
            return result
        else:
            return f"📭 Aucune notification trouvée avec les critères spécifiés"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des notifications: {str(e)}"

@tool
async def get_work_centers(
    hierarchy_id: str = None,
    cost_center: str = None
) -> str:
    """
    Récupère les centres de travail depuis SAP PM.

    Args:
        hierarchy_id: Filtrer par hiérarchie
        cost_center: Filtrer par centre de coût

    Returns:
        Liste formatée des centres de travail
    """
    try:
        params = {}
        if hierarchy_id:
            params["hierarchy_id"] = hierarchy_id
        if cost_center:
            params["cost_center"] = cost_center

        work_centers = await sap_client.get_work_centers(**params)
        
        if work_centers:
            result = f"📋 {len(work_centers)} centre(s) de travail trouvé(s):\n"
            for wc in work_centers[:10]:
                result += f"   • {wc.get('id', 'N/A')} - {wc.get('name', 'N/A')} " + \
                         f"(Centre de coût: {wc.get('cost_center', 'N/A')})\n"
            
            if len(work_centers) > 10:
                result += f"   ... et {len(work_centers) - 10} autres centres"
            
            return result
        else:
            return f"📭 Aucun centre de travail trouvé"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des centres de travail: {str(e)}"

@tool
async def get_functional_locations(
    hierarchy_id: str = None,
    equipment_id: str = None
) -> str:
    """
    Récupère les emplacements fonctionnels depuis SAP PM.

    Args:
        hierarchy_id: Filtrer par hiérarchie
        equipment_id: Filtrer par équipement

    Returns:
        Liste formatée des emplacements fonctionnels
    """
    try:
        params = {}
        if hierarchy_id:
            params["hierarchy_id"] = hierarchy_id
        if equipment_id:
            params["equipment_id"] = equipment_id

        locations = await sap_client.get_functional_locations(**params)
        
        if locations:
            result = f"📋 {len(locations)} emplacement(s) fonctionnel(s) trouvé(s):\n"
            for loc in locations[:10]:
                result += f"   • {loc.get('id', 'N/A')} - {loc.get('name', 'N/A')} " + \
                         f"(Hiérarchie: {loc.get('hierarchy_id', 'N/A')})\n"
            
            if len(locations) > 10:
                result += f"   ... et {len(locations) - 10} autres emplacements"
            
            return result
        else:
            return f"📭 Aucun emplacement fonctionnel trouvé"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des emplacements fonctionnels: {str(e)}"

@tool
async def get_materials(
    material_type: str = None,
    status: str = None
) -> str:
    """
    Récupère les matériaux depuis SAP PM.

    Args:
        material_type: Filtrer par type de matériau
        status: Filtrer par statut

    Returns:
        Liste formatée des matériaux
    """
    try:
        params = {}
        if material_type:
            params["material_type"] = material_type
        if status:
            params["status"] = status

        materials = await sap_client.get_materials(**params)
        
        if materials:
            result = f"📋 {len(materials)} matériau(x) trouvé(s):\n"
            for material in materials[:10]:
                result += f"   • {material.get('id', 'N/A')} - {material.get('name', 'N/A')} " + \
                         f"(Type: {material.get('material_type', 'N/A')})\n"
            
            if len(materials) > 10:
                result += f"   ... et {len(materials) - 10} autres matériaux"
            
            return result
        else:
            return f"📭 Aucun matériau trouvé"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des matériaux: {str(e)}"

@tool
async def get_maintenance_strategies(
    equipment_id: str = None,
    strategy_type: str = None
) -> str:
    """
    Récupère les stratégies de maintenance depuis SAP PM.

    Args:
        equipment_id: Filtrer par équipement
        strategy_type: Filtrer par type de stratégie

    Returns:
        Liste formatée des stratégies de maintenance
    """
    try:
        params = {}
        if equipment_id:
            params["equipment_id"] = equipment_id
        if strategy_type:
            params["strategy_type"] = strategy_type

        strategies = await sap_client.get_maintenance_strategies(**params)
        
        if strategies:
            result = f"📋 {len(strategies)} stratégie(s) de maintenance trouvée(s):\n"
            for strategy in strategies[:10]:
                result += f"   • {strategy.get('id', 'N/A')} - {strategy.get('name', 'N/A')} " + \
                         f"(Type: {strategy.get('strategy_type', 'N/A')})\n"
            
            if len(strategies) > 10:
                result += f"   ... et {len(strategies) - 10} autres stratégies"
            
            return result
        else:
            return f"📭 Aucune stratégie de maintenance trouvée"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des stratégies: {str(e)}"

@tool
async def get_catalogs(
    code_group: str = None,
    code: str = None
) -> str:
    """
    Récupère les catalogues depuis SAP PM.

    Args:
        code_group: Filtrer par groupe de codes
        code: Filtrer par code spécifique

    Returns:
        Liste formatée des catalogues
    """
    try:
        params = {}
        if code_group:
            params["code_group"] = code_group
        if code:
            params["code"] = code

        catalogs = await sap_client.get_catalogs(**params)
        
        if catalogs:
            result = f"📋 {len(catalogs)} catalogue(s) trouvé(s):\n"
            for catalog in catalogs[:10]:
                result += f"   • {catalog.get('id', 'N/A')} - {catalog.get('name', 'N/A')} " + \
                         f"(Groupe: {catalog.get('code_group', 'N/A')})\n"
            
            if len(catalogs) > 10:
                result += f"   ... et {len(catalogs) - 10} autres catalogues"
            
            return result
        else:
            return f"📭 Aucun catalogue trouvé"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des catalogues: {str(e)}"

@tool
async def get_characteristics(
    name: str = None,
    unit_of_measurement: str = None
) -> str:
    """
    Récupère les caractéristiques depuis SAP PM.

    Args:
        name: Filtrer par nom
        unit_of_measurement: Filtrer par unité de mesure

    Returns:
        Liste formatée des caractéristiques
    """
    try:
        params = {}
        if name:
            params["name"] = name
        if unit_of_measurement:
            params["unit_of_measurement"] = unit_of_measurement

        characteristics = await sap_client.get_characteristics(**params)
        
        if characteristics:
            result = f"📋 {len(characteristics)} caractéristique(s) trouvée(s):\n"
            for char in characteristics[:10]:
                result += f"   • {char.get('id', 'N/A')} - {char.get('name', 'N/A')} " + \
                         f"(Unité: {char.get('unit_of_measurement', 'N/A')})\n"
            
            if len(characteristics) > 10:
                result += f"   ... et {len(characteristics) - 10} autres caractéristiques"
            
            return result
        else:
            return f"📭 Aucune caractéristique trouvée"
            
    except Exception as e:
        return f"❌ Erreur lors de la récupération des caractéristiques: {str(e)}" 