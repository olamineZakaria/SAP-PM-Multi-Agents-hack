"""
Module de base de données MongoDB pour le simulateur SAP PM
Contient la configuration MongoDB et les fonctions de gestion
"""

from typing import Dict, List, Any, Optional
import uuid
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from schemas import *
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "RAGENNT4SAP")

# Client MongoDB
client: Optional[AsyncIOMotorClient] = None
database = None

async def connect_to_mongo():
    """Établit la connexion à MongoDB"""
    global client, database
    client = AsyncIOMotorClient(MONGO_URL)
    database = client[DATABASE_NAME]
    print(f"Connecté à MongoDB: {MONGO_URL}")
    print(f"Base de données: {DATABASE_NAME}")

async def close_mongo_connection():
    """Ferme la connexion à MongoDB"""
    global client
    if client:
        client.close()
        print("Connexion MongoDB fermée")

def generate_id() -> str:
    """Génère un ID unique pour les nouvelles entrées"""
    return str(uuid.uuid4())

def get_database():
    """Retourne la connexion à la base de données"""
    global database
    if database is None:
        raise RuntimeError("Database connection not established. Please ensure the application has started properly.")
    return database

async def initialize_sample_data():
    """Initialise la base de données avec des données d'exemple complètes"""
    
    # Vérifier si les données existent déjà
    catalog_count = await database.catalogs.count_documents({})
    if catalog_count > 0:
        print("Base de données déjà initialisée")
        return
    
    print("Initialisation des données de simulation pour RAGENNT4SAP...")
    
    # ============================================================================
    # 1. CATALOGUES (Catalogs)
    # ============================================================================
    catalogs = [
        Catalog(id=generate_id(), code_group="DEFAULTS", code="DEFAULT", text="Valeur par défaut"),
        Catalog(id=generate_id(), code_group="MAINTENANCE", code="PREVENTIVE", text="Maintenance préventive"),
        Catalog(id=generate_id(), code_group="MAINTENANCE", code="CORRECTIVE", text="Maintenance corrective"),
        Catalog(id=generate_id(), code_group="MAINTENANCE", code="INSPECTION", text="Inspection"),
        Catalog(id=generate_id(), code_group="MAINTENANCE", code="CALIBRATION", text="Calibration"),
        Catalog(id=generate_id(), code_group="PRIORITY", code="HIGH", text="Priorité haute"),
        Catalog(id=generate_id(), code_group="PRIORITY", code="MEDIUM", text="Priorité moyenne"),
        Catalog(id=generate_id(), code_group="PRIORITY", code="LOW", text="Priorité basse"),
        Catalog(id=generate_id(), code_group="STATUS", code="ACTIVE", text="Actif"),
        Catalog(id=generate_id(), code_group="STATUS", code="INACTIVE", text="Inactif")
    ]
    
    for catalog in catalogs:
        await database.catalogs.insert_one(catalog.dict())
    
    # ============================================================================
    # 2. PERMIS (Permits)
    # ============================================================================
    permits = [
        Permit(id=generate_id(), name="Permis de travail en hauteur", description="Autorisation pour travaux en hauteur"),
        Permit(id=generate_id(), name="Permis de travail électrique", description="Autorisation pour travaux électriques"),
        Permit(id=generate_id(), name="Permis de travail en espace confiné", description="Autorisation pour espaces confinés"),
        Permit(id=generate_id(), name="Permis de travail à chaud", description="Autorisation pour travaux à chaud"),
        Permit(id=generate_id(), name="Permis de travail sous pression", description="Autorisation pour travaux sous pression")
    ]
    
    for permit in permits:
        await database.permits.insert_one(permit.dict())
    
    # ============================================================================
    # 3. CARACTÉRISTIQUES (Characteristics)
    # ============================================================================
    characteristics = [
        Characteristic(id=generate_id(), name="Puissance", description="Puissance en CV", unit_of_measurement=UnitOfMeasurement.KILOGRAMS),
        Characteristic(id=generate_id(), name="Température", description="Température de fonctionnement", unit_of_measurement=UnitOfMeasurement.DEGREES),
        Characteristic(id=generate_id(), name="Pression", description="Pression de fonctionnement", unit_of_measurement=UnitOfMeasurement.KILOGRAMS),
        Characteristic(id=generate_id(), name="Vitesse", description="Vitesse de rotation", unit_of_measurement=UnitOfMeasurement.CYCLES),
        Characteristic(id=generate_id(), name="Niveau", description="Niveau de liquide", unit_of_measurement=UnitOfMeasurement.PERCENT),
        Characteristic(id=generate_id(), name="Débit", description="Débit volumique", unit_of_measurement=UnitOfMeasurement.LITERS),
        Characteristic(id=generate_id(), name="Distance", description="Distance parcourue", unit_of_measurement=UnitOfMeasurement.KILOMETERS),
        Characteristic(id=generate_id(), name="Heures", description="Heures de fonctionnement", unit_of_measurement=UnitOfMeasurement.HOURS)
    ]
    
    for char in characteristics:
        await database.characteristics.insert_one(char.dict())
    
    # ============================================================================
    # 4. CLASSES (Classes)
    # ============================================================================
    classes = [
        Class(id=generate_id(), name="Pompes", description="Classe pour les pompes", characteristics=[characteristics[0].id, characteristics[1].id, characteristics[2].id]),
        Class(id=generate_id(), name="Moteurs", description="Classe pour les moteurs", characteristics=[characteristics[0].id, characteristics[3].id, characteristics[7].id]),
        Class(id=generate_id(), name="Réservoirs", description="Classe pour les réservoirs", characteristics=[characteristics[4].id, characteristics[5].id]),
        Class(id=generate_id(), name="Convoyeurs", description="Classe pour les convoyeurs", characteristics=[characteristics[3].id, characteristics[6].id]),
        Class(id=generate_id(), name="Compresseurs", description="Classe pour les compresseurs", characteristics=[characteristics[0].id, characteristics[2].id, characteristics[3].id])
    ]
    
    for cls in classes:
        await database.classes.insert_one(cls.dict())
    
    # ============================================================================
    # 5. STRATÉGIES DE MAINTENANCE (Maintenance Strategies)
    # ============================================================================
    strategies = [
        MaintenanceStrategy(id=generate_id(), name="Maintenance préventive", description="Stratégie de maintenance préventive basée sur le temps"),
        MaintenanceStrategy(id=generate_id(), name="Maintenance conditionnelle", description="Stratégie basée sur l'état de l'équipement"),
        MaintenanceStrategy(id=generate_id(), name="Maintenance prédictive", description="Stratégie utilisant l'analyse prédictive"),
        MaintenanceStrategy(id=generate_id(), name="Maintenance corrective", description="Stratégie de réparation après panne"),
        MaintenanceStrategy(id=generate_id(), name="Maintenance proactive", description="Stratégie proactive pour éviter les pannes")
    ]
    
    for strategy in strategies:
        await database.maintenance_strategies.insert_one(strategy.dict())
    
    # ============================================================================
    # 6. ENSEMBLES DE CYCLES (Cycle Sets)
    # ============================================================================
    cycle_sets = [
        CycleSet(id=generate_id(), name="Cycle standard", description="Cycle de maintenance standard", cycles=["6 MONTHS", "500 H", "1000 CYCLES"]),
        CycleSet(id=generate_id(), name="Cycle intensif", description="Cycle de maintenance intensif", cycles=["3 MONTHS", "250 H", "500 CYCLES"]),
        CycleSet(id=generate_id(), name="Cycle léger", description="Cycle de maintenance léger", cycles=["12 MONTHS", "1000 H", "2000 CYCLES"]),
        CycleSet(id=generate_id(), name="Cycle critique", description="Cycle pour équipements critiques", cycles=["1 MONTH", "100 H", "200 CYCLES"])
    ]
    
    for cycle_set in cycle_sets:
        await database.cycle_sets.insert_one(cycle_set.dict())
    
    # ============================================================================
    # 7. HIÉRARCHIES DES CENTRES DE TRAVAIL (Work Center Hierarchies)
    # ============================================================================
    hierarchies = [
        WorkCenterHierarchy(id=generate_id(), name="Hiérarchie principale", description="Hiérarchie principale des centres de travail"),
        WorkCenterHierarchy(id=generate_id(), name="Hiérarchie mécanique", description="Hiérarchie pour la maintenance mécanique"),
        WorkCenterHierarchy(id=generate_id(), name="Hiérarchie électrique", description="Hiérarchie pour la maintenance électrique"),
        WorkCenterHierarchy(id=generate_id(), name="Hiérarchie instrumentation", description="Hiérarchie pour l'instrumentation")
    ]
    
    for hierarchy in hierarchies:
        await database.work_center_hierarchies.insert_one(hierarchy.dict())
    
    # ============================================================================
    # 8. CENTRES DE TRAVAIL (Work Centers)
    # ============================================================================
    work_centers = [
        WorkCenter(id=generate_id(), name="Atelier mécanique", cost_center="CC001", employee_id="EMP001", hierarchy_id=hierarchies[1].id),
        WorkCenter(id=generate_id(), name="Atelier électrique", cost_center="CC002", employee_id="EMP002", hierarchy_id=hierarchies[2].id),
        WorkCenter(id=generate_id(), name="Atelier instrumentation", cost_center="CC003", employee_id="EMP003", hierarchy_id=hierarchies[3].id),
        WorkCenter(id=generate_id(), name="Atelier général", cost_center="CC004", employee_id="EMP004", hierarchy_id=hierarchies[0].id),
        WorkCenter(id=generate_id(), name="Équipe mobile", cost_center="CC005", employee_id="EMP005", hierarchy_id=hierarchies[0].id)
    ]
    
    for work_center in work_centers:
        await database.work_centers.insert_one(work_center.dict())
    
    # ============================================================================
    # 9. MATÉRIELS (Materials)
    # ============================================================================
    materials = [
        Material(id=generate_id(), name="Roulement 6205", description="Roulement à billes 6205", cost_center="CC001", profit_center="PC001", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Joint d'étanchéité", description="Joint d'étanchéité standard", cost_center="CC001", profit_center="PC001", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Filtre à air HEPA", description="Filtre à air haute efficacité", cost_center="CC002", profit_center="PC002", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Huile moteur SAE 30", description="Huile moteur SAE 30", cost_center="CC001", profit_center="PC001", uom=UnitOfMeasurement.LITERS),
        Material(id=generate_id(), name="Courroie trapézoïdale", description="Courroie trapézoïdale A-50", cost_center="CC001", profit_center="PC001", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Ampoule LED 100W", description="Ampoule LED 100W", cost_center="CC002", profit_center="PC002", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Capteur de température", description="Capteur PT100", cost_center="CC003", profit_center="PC003", uom=UnitOfMeasurement.KILOGRAMS),
        Material(id=generate_id(), name="Transmetteur de pression", description="Transmetteur 4-20mA", cost_center="CC003", profit_center="PC003", uom=UnitOfMeasurement.KILOGRAMS)
    ]
    
    for material in materials:
        await database.materials.insert_one(material.dict())
    
    # ============================================================================
    # 10. NOMENCLATURES (Bill of Materials)
    # ============================================================================
    boms = [
        BillOfMaterial(id=generate_id(), name="BOM Pompe Centrifuge", material_id=materials[0].id),
        BillOfMaterial(id=generate_id(), name="BOM Moteur Électrique", material_id=materials[1].id),
        BillOfMaterial(id=generate_id(), name="BOM Filtre à Air", material_id=materials[2].id),
        BillOfMaterial(id=generate_id(), name="BOM Système de Lubrification", material_id=materials[3].id)
    ]
    
    for bom in boms:
        await database.bill_of_materials.insert_one(bom.dict())
    
    # ============================================================================
    # 11. POSTES TECHNIQUES (Functional Locations)
    # ============================================================================
    functional_locations = [
        FunctionalLocation(id=generate_id(), name="Zone A - Circuit de refroidissement", description="Zone A du circuit de refroidissement", main_work_center_id=work_centers[0].id, cost_center="CC001", class_id=classes[0].id, characteristics=[characteristics[0].id, characteristics[1].id], asset_id="ASSET001", permits=[permits[0].id]),
        FunctionalLocation(id=generate_id(), name="Zone B - Production", description="Zone B de production", main_work_center_id=work_centers[1].id, cost_center="CC002", class_id=classes[1].id, characteristics=[characteristics[0].id, characteristics[3].id], asset_id="ASSET002", permits=[permits[1].id]),
        FunctionalLocation(id=generate_id(), name="Zone C - Stockage", description="Zone C de stockage", main_work_center_id=work_centers[2].id, cost_center="CC003", class_id=classes[2].id, characteristics=[characteristics[4].id, characteristics[5].id], asset_id="ASSET003", permits=[permits[2].id]),
        FunctionalLocation(id=generate_id(), name="Zone D - Transport", description="Zone D de transport", main_work_center_id=work_centers[3].id, cost_center="CC004", class_id=classes[3].id, characteristics=[characteristics[3].id, characteristics[6].id], asset_id="ASSET004", permits=[permits[3].id])
    ]
    
    for fl in functional_locations:
        await database.functional_locations.insert_one(fl.dict())
    
    # ============================================================================
    # 12. ÉQUIPEMENTS (Equipment)
    # ============================================================================
    equipment = [
        Equipment(id=generate_id(), name="Pompe Centrifuge P-001", description="Pompe principale du circuit de refroidissement", functional_location_id=functional_locations[0].id, main_work_center_id=work_centers[0].id, cost_center="CC001", class_id=classes[0].id, characteristics=[characteristics[0].id, characteristics[1].id], asset_id="ASSET001", permits=[permits[0].id]),
        Equipment(id=generate_id(), name="Moteur Électrique M-001", description="Moteur principal de production", functional_location_id=functional_locations[1].id, main_work_center_id=work_centers[1].id, cost_center="CC002", class_id=classes[1].id, characteristics=[characteristics[0].id, characteristics[3].id], asset_id="ASSET002", permits=[permits[1].id]),
        Equipment(id=generate_id(), name="Réservoir Stockage R-001", description="Réservoir principal de stockage", functional_location_id=functional_locations[2].id, main_work_center_id=work_centers[2].id, cost_center="CC003", class_id=classes[2].id, characteristics=[characteristics[4].id, characteristics[5].id], asset_id="ASSET003", permits=[permits[2].id]),
        Equipment(id=generate_id(), name="Convoyeur Transport C-001", description="Convoyeur principal de transport", functional_location_id=functional_locations[3].id, main_work_center_id=work_centers[3].id, cost_center="CC004", class_id=classes[3].id, characteristics=[characteristics[3].id, characteristics[6].id], asset_id="ASSET004", permits=[permits[3].id]),
        Equipment(id=generate_id(), name="Compresseur Air COMP-001", description="Compresseur d'air principal", functional_location_id=functional_locations[0].id, main_work_center_id=work_centers[0].id, cost_center="CC001", class_id=classes[4].id, characteristics=[characteristics[0].id, characteristics[2].id], asset_id="ASSET005", permits=[permits[4].id])
    ]
    
    for eq in equipment:
        await database.equipment.insert_one(eq.dict())
    
    # ============================================================================
    # 13. POINTS DE MESURE (Measuring Points)
    # ============================================================================
    measuring_points = [
        MeasuringPoint(id=generate_id(), name="MP-001", description="Point de mesure température pompe", target_object_type="EQUIPMENT", target_object_id=equipment[0].id, characteristic_id=characteristics[1].id, catalog_code_groups=["DEFAULTS"]),
        MeasuringPoint(id=generate_id(), name="MP-002", description="Point de mesure pression pompe", target_object_type="EQUIPMENT", target_object_id=equipment[0].id, characteristic_id=characteristics[2].id, catalog_code_groups=["DEFAULTS"]),
        MeasuringPoint(id=generate_id(), name="MP-003", description="Point de mesure vitesse moteur", target_object_type="EQUIPMENT", target_object_id=equipment[1].id, characteristic_id=characteristics[3].id, catalog_code_groups=["DEFAULTS"]),
        MeasuringPoint(id=generate_id(), name="MP-004", description="Point de mesure niveau réservoir", target_object_type="EQUIPMENT", target_object_id=equipment[2].id, characteristic_id=characteristics[4].id, catalog_code_groups=["DEFAULTS"]),
        MeasuringPoint(id=generate_id(), name="MP-005", description="Point de mesure vitesse convoyeur", target_object_type="EQUIPMENT", target_object_id=equipment[3].id, characteristic_id=characteristics[3].id, catalog_code_groups=["DEFAULTS"])
    ]
    
    for mp in measuring_points:
        await database.measuring_points.insert_one(mp.dict())
    
    # ============================================================================
    # 14. COMPTEURS (Counters)
    # ============================================================================
    counters = [
        Counter(id=generate_id(), name="Compteur heures P-001", description="Compteur d'heures de fonctionnement pompe", target_object_type="EQUIPMENT", target_object_id=equipment[0].id, characteristic_id=characteristics[7].id, current_reading=1250.5),
        Counter(id=generate_id(), name="Compteur heures M-001", description="Compteur d'heures de fonctionnement moteur", target_object_type="EQUIPMENT", target_object_id=equipment[1].id, characteristic_id=characteristics[7].id, current_reading=2100.0),
        Counter(id=generate_id(), name="Compteur cycles C-001", description="Compteur de cycles convoyeur", target_object_type="EQUIPMENT", target_object_id=equipment[3].id, characteristic_id=characteristics[3].id, current_reading=50000.0),
        Counter(id=generate_id(), name="Compteur distance C-001", description="Compteur de distance convoyeur", target_object_type="EQUIPMENT", target_object_id=equipment[3].id, characteristic_id=characteristics[6].id, current_reading=150.5)
    ]
    
    for counter in counters:
        await database.counters.insert_one(counter.dict())
    
    # ============================================================================
    # 15. NUMÉROS DE SÉRIE (Serial Numbers)
    # ============================================================================
    serial_numbers = [
        SerialNumber(id=generate_id(), serial_number="SN-P001-2024-001", material_id=materials[0].id, equipment_id=equipment[0].id),
        SerialNumber(id=generate_id(), serial_number="SN-M001-2024-002", material_id=materials[1].id, equipment_id=equipment[1].id),
        SerialNumber(id=generate_id(), serial_number="SN-R001-2024-003", material_id=materials[2].id, equipment_id=equipment[2].id),
        SerialNumber(id=generate_id(), serial_number="SN-C001-2024-004", material_id=materials[3].id, equipment_id=equipment[3].id),
        SerialNumber(id=generate_id(), serial_number="SN-COMP001-2024-005", material_id=materials[4].id, equipment_id=equipment[4].id)
    ]
    
    for sn in serial_numbers:
        await database.serial_numbers.insert_one(sn.dict())
    
    # ============================================================================
    # 16. NOMENCLATURES DE POSTES TECHNIQUES (Functional Location BOMs)
    # ============================================================================
    fl_boms = [
        FunctionalLocationBOM(id=generate_id(), functional_location_id=functional_locations[0].id, material_master_id=materials[0].id),
        FunctionalLocationBOM(id=generate_id(), functional_location_id=functional_locations[1].id, material_master_id=materials[1].id),
        FunctionalLocationBOM(id=generate_id(), functional_location_id=functional_locations[2].id, material_master_id=materials[2].id),
        FunctionalLocationBOM(id=generate_id(), functional_location_id=functional_locations[3].id, material_master_id=materials[3].id)
    ]
    
    for fl_bom in fl_boms:
        await database.functional_location_boms.insert_one(fl_bom.dict())
    
    # ============================================================================
    # 17. NOMENCLATURES D'ÉQUIPEMENTS (Equipment BOMs)
    # ============================================================================
    eq_boms = [
        EquipmentBOM(id=generate_id(), equipment_id=equipment[0].id, material_master_id=materials[0].id),
        EquipmentBOM(id=generate_id(), equipment_id=equipment[1].id, material_master_id=materials[1].id),
        EquipmentBOM(id=generate_id(), equipment_id=equipment[2].id, material_master_id=materials[2].id),
        EquipmentBOM(id=generate_id(), equipment_id=equipment[3].id, material_master_id=materials[3].id),
        EquipmentBOM(id=generate_id(), equipment_id=equipment[4].id, material_master_id=materials[4].id)
    ]
    
    for eq_bom in eq_boms:
        await database.equipment_boms.insert_one(eq_bom.dict())
    
    # ============================================================================
    # 18. GAMMES GÉNÉRALES (General Task Lists)
    # ============================================================================
    general_task_lists = [
        GeneralTaskList(id=generate_id(), name="Gamme générale pompes", main_work_center_id=work_centers[0].id, maintenance_strategy_id=strategies[0].id, material_id=materials[0].id, activity_type=ActivityType.PREVENTIVE),
        GeneralTaskList(id=generate_id(), name="Gamme générale moteurs", main_work_center_id=work_centers[1].id, maintenance_strategy_id=strategies[1].id, material_id=materials[1].id, activity_type=ActivityType.PREVENTIVE),
        GeneralTaskList(id=generate_id(), name="Gamme générale réservoirs", main_work_center_id=work_centers[2].id, maintenance_strategy_id=strategies[2].id, material_id=materials[2].id, activity_type=ActivityType.INSPECTION),
        GeneralTaskList(id=generate_id(), name="Gamme générale convoyeurs", main_work_center_id=work_centers[3].id, maintenance_strategy_id=strategies[3].id, material_id=materials[3].id, activity_type=ActivityType.CORRECTIVE)
    ]
    
    for gtl in general_task_lists:
        await database.general_task_lists.insert_one(gtl.dict())
    
    # ============================================================================
    # 19. GAMMES POUR ÉQUIPEMENTS (Equipment Task Lists)
    # ============================================================================
    equipment_task_lists = [
        EquipmentTaskList(id=generate_id(), name="Gamme P-001", equipment_id=equipment[0].id, main_work_center_id=work_centers[0].id, maintenance_strategy_id=strategies[0].id, material_id=materials[0].id, activity_type=ActivityType.PREVENTIVE),
        EquipmentTaskList(id=generate_id(), name="Gamme M-001", equipment_id=equipment[1].id, main_work_center_id=work_centers[1].id, maintenance_strategy_id=strategies[1].id, material_id=materials[1].id, activity_type=ActivityType.PREVENTIVE),
        EquipmentTaskList(id=generate_id(), name="Gamme R-001", equipment_id=equipment[2].id, main_work_center_id=work_centers[2].id, maintenance_strategy_id=strategies[2].id, material_id=materials[2].id, activity_type=ActivityType.INSPECTION),
        EquipmentTaskList(id=generate_id(), name="Gamme C-001", equipment_id=equipment[3].id, main_work_center_id=work_centers[3].id, maintenance_strategy_id=strategies[3].id, material_id=materials[3].id, activity_type=ActivityType.CORRECTIVE),
        EquipmentTaskList(id=generate_id(), name="Gamme COMP-001", equipment_id=equipment[4].id, main_work_center_id=work_centers[0].id, maintenance_strategy_id=strategies[4].id, material_id=materials[4].id, activity_type=ActivityType.CALIBRATION)
    ]
    
    for etl in equipment_task_lists:
        await database.equipment_task_lists.insert_one(etl.dict())
    
    # ============================================================================
    # 20. GAMMES POUR POSTES TECHNIQUES (Functional Location Task Lists)
    # ============================================================================
    fl_task_lists = [
        FunctionalLocationTaskList(id=generate_id(), name="Gamme Zone A", functional_location_id=functional_locations[0].id, main_work_center_id=work_centers[0].id, maintenance_strategy_id=strategies[0].id, material_id=materials[0].id, activity_type=ActivityType.PREVENTIVE),
        FunctionalLocationTaskList(id=generate_id(), name="Gamme Zone B", functional_location_id=functional_locations[1].id, main_work_center_id=work_centers[1].id, maintenance_strategy_id=strategies[1].id, material_id=materials[1].id, activity_type=ActivityType.PREVENTIVE),
        FunctionalLocationTaskList(id=generate_id(), name="Gamme Zone C", functional_location_id=functional_locations[2].id, main_work_center_id=work_centers[2].id, maintenance_strategy_id=strategies[2].id, material_id=materials[2].id, activity_type=ActivityType.INSPECTION),
        FunctionalLocationTaskList(id=generate_id(), name="Gamme Zone D", functional_location_id=functional_locations[3].id, main_work_center_id=work_centers[3].id, maintenance_strategy_id=strategies[3].id, material_id=materials[3].id, activity_type=ActivityType.CORRECTIVE)
    ]
    
    for fltl in fl_task_lists:
        await database.functional_location_task_lists.insert_one(fltl.dict())
    
    # ============================================================================
    # 21. PLANS À CYCLE SIMPLE (Single Cycle Plans)
    # ============================================================================
    single_cycle_plans = [
        SingleCyclePlan(id=generate_id(), name="Plan maintenance P-001", task_list_id=equipment_task_lists[0].id, equipment_id=equipment[0].id, functional_location_id=functional_locations[0].id, counter_id=counters[0].id),
        SingleCyclePlan(id=generate_id(), name="Plan maintenance M-001", task_list_id=equipment_task_lists[1].id, equipment_id=equipment[1].id, functional_location_id=functional_locations[1].id, counter_id=counters[1].id),
        SingleCyclePlan(id=generate_id(), name="Plan maintenance C-001", task_list_id=equipment_task_lists[3].id, equipment_id=equipment[3].id, functional_location_id=functional_locations[3].id, counter_id=counters[2].id)
    ]
    
    for scp in single_cycle_plans:
        await database.single_cycle_plans.insert_one(scp.dict())
    
    # ============================================================================
    # 22. PLANS DE MAINTENANCE STRATÉGIQUE (Strategy Maintenance Plans)
    # ============================================================================
    strategy_maintenance_plans = [
        StrategyMaintenancePlan(id=generate_id(), name="Plan stratégique P-001", task_list_id=equipment_task_lists[0].id, equipment_id=equipment[0].id, functional_location_id=functional_locations[0].id, counter_id=counters[0].id, maintenance_strategy_id=strategies[0].id),
        StrategyMaintenancePlan(id=generate_id(), name="Plan stratégique M-001", task_list_id=equipment_task_lists[1].id, equipment_id=equipment[1].id, functional_location_id=functional_locations[1].id, counter_id=counters[1].id, maintenance_strategy_id=strategies[1].id),
        StrategyMaintenancePlan(id=generate_id(), name="Plan stratégique COMP-001", task_list_id=equipment_task_lists[4].id, equipment_id=equipment[4].id, functional_location_id=functional_locations[0].id, counter_id=counters[0].id, maintenance_strategy_id=strategies[4].id)
    ]
    
    for smp in strategy_maintenance_plans:
        await database.strategy_maintenance_plans.insert_one(smp.dict())
    
    # ============================================================================
    # 23. PLANS À PLUSIEURS COMPTEURS (Multiple Counter Plans)
    # ============================================================================
    multiple_counter_plans = [
        MultipleCounterPlan(id=generate_id(), name="Plan multi-compteurs C-001", task_list_id=equipment_task_lists[3].id, equipment_id=equipment[3].id, functional_location_id=functional_locations[3].id, counter_id=counters[2].id, cycle_set_id=cycle_sets[0].id),
        MultipleCounterPlan(id=generate_id(), name="Plan multi-compteurs P-001", task_list_id=equipment_task_lists[0].id, equipment_id=equipment[0].id, functional_location_id=functional_locations[0].id, counter_id=counters[0].id, cycle_set_id=cycle_sets[1].id)
    ]
    
    for mcp in multiple_counter_plans:
        await database.multiple_counter_plans.insert_one(mcp.dict())
    
    # ============================================================================
    # 24. VALEURS CARACTÉRISTIQUES (Characteristic Values)
    # ============================================================================
    characteristic_values = [
        CharacteristicValues(id=generate_id(), class_id=classes[0].id, characteristic_id=characteristics[0].id, value="7.5", master_data_object_id=equipment[0].id, master_data_object_type="EQUIPMENT"),
        CharacteristicValues(id=generate_id(), class_id=classes[0].id, characteristic_id=characteristics[1].id, value="65.0", master_data_object_id=equipment[0].id, master_data_object_type="EQUIPMENT"),
        CharacteristicValues(id=generate_id(), class_id=classes[1].id, characteristic_id=characteristics[0].id, value="15.0", master_data_object_id=equipment[1].id, master_data_object_type="EQUIPMENT"),
        CharacteristicValues(id=generate_id(), class_id=classes[1].id, characteristic_id=characteristics[3].id, value="1750", master_data_object_id=equipment[1].id, master_data_object_type="EQUIPMENT"),
        CharacteristicValues(id=generate_id(), class_id=classes[2].id, characteristic_id=characteristics[4].id, value="85.0", master_data_object_id=equipment[2].id, master_data_object_type="EQUIPMENT")
    ]
    
    for cv in characteristic_values:
        await database.characteristic_values.insert_one(cv.dict())
    
    # ============================================================================
    # 25. NOTIFICATIONS (Notifications)
    # ============================================================================
    from datetime import datetime, timedelta
    
    notifications = [
        Notification(
            id=generate_id(),
            title="Panne moteur pompe P-001",
            description="Le moteur de la pompe P-001 présente des vibrations anormales et nécessite une intervention urgente",
            status=NotificationStatus.CREATED,
            priority=NotificationPriority.HIGH,
            notification_type=NotificationType.BREAKDOWN,
            created_date=datetime.now() - timedelta(hours=2),
            created_by="OPERATEUR_001",
            equipment_id=equipment[0].id,
            work_center_id=work_centers[0].id,
            assigned_to="TECHNICIEN_001",
            estimated_duration=4.0
        ),
        Notification(
            id=generate_id(),
            title="Maintenance préventive compresseur M-001",
            description="Maintenance préventive programmée pour le compresseur M-001 selon le planning",
            status=NotificationStatus.IN_PROGRESS,
            priority=NotificationPriority.MEDIUM,
            notification_type=NotificationType.PREVENTIVE,
            created_date=datetime.now() - timedelta(days=1),
            created_by="PLANIFICATEUR_001",
            equipment_id=equipment[1].id,
            work_center_id=work_centers[1].id,
            assigned_to="TECHNICIEN_002",
            estimated_duration=8.0,
            actual_duration=6.5,
            completion_date=datetime.now() - timedelta(hours=2)
        ),
        Notification(
            id=generate_id(),
            title="Inspection sécurité zone A",
            description="Inspection de sécurité requise pour la zone A du poste technique FL-001",
            status=NotificationStatus.COMPLETED,
            priority=NotificationPriority.CRITICAL,
            notification_type=NotificationType.SAFETY,
            created_date=datetime.now() - timedelta(days=2),
            created_by="SECURITE_001",
            functional_location_id=functional_locations[0].id,
            work_center_id=work_centers[0].id,
            assigned_to="INSPECTEUR_001",
            estimated_duration=2.0,
            actual_duration=1.5,
            completion_date=datetime.now() - timedelta(days=1)
        ),
        Notification(
            id=generate_id(),
            title="Calibration capteur température",
            description="Calibration du capteur de température sur l'équipement C-001",
            status=NotificationStatus.CREATED,
            priority=NotificationPriority.LOW,
            notification_type=NotificationType.CALIBRATION,
            created_date=datetime.now() - timedelta(hours=1),
            created_by="QUALITE_001",
            equipment_id=equipment[2].id,
            work_center_id=work_centers[2].id,
            estimated_duration=1.0
        )
    ]
    
    for notification in notifications:
        await database.notifications.insert_one(notification.dict())
    
    # ============================================================================
    # 26. ORDRES (Orders)
    # ============================================================================
    orders = [
        Order(
            id=generate_id(),
            order_number="WO-2024-001",
            title="Réparation moteur pompe P-001",
            description="Réparation complète du moteur de la pompe P-001 suite à la panne signalée",
            status=OrderStatus.IN_PROGRESS,
            order_type=OrderType.CORRECTIVE,
            created_date=datetime.now() - timedelta(hours=1),
            created_by="TECHNICIEN_001",
            equipment_id=equipment[0].id,
            work_center_id=work_centers[0].id,
            assigned_to="TECHNICIEN_001",
            planned_start_date=datetime.now() - timedelta(hours=1),
            planned_end_date=datetime.now() + timedelta(hours=3),
            actual_start_date=datetime.now() - timedelta(hours=1),
            estimated_duration=4.0,
            actual_duration=2.5,
            priority=NotificationPriority.HIGH,
            cost_center="CC-MAINT-001",
            materials_required=[materials[0].id, materials[1].id],
            related_notifications=[notifications[0].id]
        ),
        Order(
            id=generate_id(),
            order_number="WO-2024-002",
            title="Maintenance préventive compresseur M-001",
            description="Maintenance préventive programmée pour le compresseur M-001",
            status=OrderStatus.COMPLETED,
            order_type=OrderType.PREVENTIVE,
            created_date=datetime.now() - timedelta(days=1),
            created_by="PLANIFICATEUR_001",
            equipment_id=equipment[1].id,
            work_center_id=work_centers[1].id,
            assigned_to="TECHNICIEN_002",
            planned_start_date=datetime.now() - timedelta(days=1),
            planned_end_date=datetime.now() - timedelta(hours=2),
            actual_start_date=datetime.now() - timedelta(days=1),
            actual_end_date=datetime.now() - timedelta(hours=2),
            estimated_duration=8.0,
            actual_duration=6.5,
            priority=NotificationPriority.MEDIUM,
            cost_center="CC-MAINT-002",
            materials_required=[materials[2].id],
            related_notifications=[notifications[1].id],
            task_list_id=equipment_task_lists[1].id
        ),
        Order(
            id=generate_id(),
            order_number="WO-2024-003",
            title="Inspection sécurité zone A",
            description="Inspection de sécurité complète de la zone A",
            status=OrderStatus.COMPLETED,
            order_type=OrderType.INSPECTION,
            created_date=datetime.now() - timedelta(days=2),
            created_by="SECURITE_001",
            functional_location_id=functional_locations[0].id,
            work_center_id=work_centers[0].id,
            assigned_to="INSPECTEUR_001",
            planned_start_date=datetime.now() - timedelta(days=2),
            planned_end_date=datetime.now() - timedelta(days=1),
            actual_start_date=datetime.now() - timedelta(days=2),
            actual_end_date=datetime.now() - timedelta(days=1),
            estimated_duration=2.0,
            actual_duration=1.5,
            priority=NotificationPriority.CRITICAL,
            cost_center="CC-SECU-001",
            related_notifications=[notifications[2].id]
        ),
        Order(
            id=generate_id(),
            order_number="WO-2024-004",
            title="Calibration capteur température C-001",
            description="Calibration du capteur de température sur l'équipement C-001",
            status=OrderStatus.CREATED,
            order_type=OrderType.CALIBRATION,
            created_date=datetime.now() - timedelta(hours=1),
            created_by="QUALITE_001",
            equipment_id=equipment[2].id,
            work_center_id=work_centers[2].id,
            assigned_to="TECHNICIEN_003",
            planned_start_date=datetime.now() + timedelta(hours=2),
            planned_end_date=datetime.now() + timedelta(hours=3),
            estimated_duration=1.0,
            priority=NotificationPriority.LOW,
            cost_center="CC-QUAL-001",
            related_notifications=[notifications[3].id]
        )
    ]
    
    for order in orders:
        await database.orders.insert_one(order.dict())
    
    print("✅ Données de simulation RAGENNT4SAP initialisées avec succès!")
    print(f"📊 Collections créées: {len(database.list_collection_names())}")
    print("🎯 Base de données prête pour les tests!")

async def get_all_data() -> Dict[str, Any]:
    """Retourne toutes les données de la base"""
    return {
        "catalogs": await database.catalogs.find().to_list(length=None),
        "permits": await database.permits.find().to_list(length=None),
        "characteristics": await database.characteristics.find().to_list(length=None),
        "classes": await database.classes.find().to_list(length=None),
        "maintenance_strategies": await database.maintenance_strategies.find().to_list(length=None),
        "cycle_sets": await database.cycle_sets.find().to_list(length=None),
        "work_center_hierarchies": await database.work_center_hierarchies.find().to_list(length=None),
        "work_centers": await database.work_centers.find().to_list(length=None),
        "materials": await database.materials.find().to_list(length=None),
        "bill_of_materials": await database.bill_of_materials.find().to_list(length=None),
        "functional_locations": await database.functional_locations.find().to_list(length=None),
        "equipment": await database.equipment.find().to_list(length=None),
        "measuring_points": await database.measuring_points.find().to_list(length=None),
        "counters": await database.counters.find().to_list(length=None),
        "serial_numbers": await database.serial_numbers.find().to_list(length=None),
        "functional_location_boms": await database.functional_location_boms.find().to_list(length=None),
        "equipment_boms": await database.equipment_boms.find().to_list(length=None),
        "general_task_lists": await database.general_task_lists.find().to_list(length=None),
        "equipment_task_lists": await database.equipment_task_lists.find().to_list(length=None),
        "functional_location_task_lists": await database.functional_location_task_lists.find().to_list(length=None),
        "single_cycle_plans": await database.single_cycle_plans.find().to_list(length=None),
        "strategy_maintenance_plans": await database.strategy_maintenance_plans.find().to_list(length=None),
        "multiple_counter_plans": await database.multiple_counter_plans.find().to_list(length=None),
        "characteristic_values": await database.characteristic_values.find().to_list(length=None),
        "notifications": await database.notifications.find().to_list(length=None),
        "orders": await database.orders.find().to_list(length=None)
    }
