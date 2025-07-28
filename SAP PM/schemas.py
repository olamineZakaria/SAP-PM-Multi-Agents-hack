from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Enums pour les types d'activité et unités de mesure
class ActivityType(str, Enum):
    PREVENTIVE = "PREVENTIVE"
    CORRECTIVE = "CORRECTIVE"
    INSPECTION = "INSPECTION"
    CALIBRATION = "CALIBRATION"

class UnitOfMeasurement(str, Enum):
    HOURS = "HOURS"
    DAYS = "DAYS"
    MONTHS = "MONTHS"
    YEARS = "YEARS"
    KILOMETERS = "KM"
    CYCLES = "CYCLES"
    LITERS = "L"
    KILOGRAMS = "KG"
    DEGREES = "°C"
    PERCENT = "%"

# Modèles de base
class Catalog(BaseModel):
    id: str = Field(..., description="Identifiant unique du catalogue")
    code_group: str = Field(..., description="Groupe de codes")
    code: str = Field(..., description="Code spécifique")
    text: str = Field(..., description="Description textuelle")

class Permit(BaseModel):
    id: str = Field(..., description="Identifiant unique du permis")
    name: str = Field(..., description="Nom du permis")
    description: str = Field(..., description="Description du permis")

class Characteristic(BaseModel):
    id: str = Field(..., description="Identifiant unique de la caractéristique")
    name: str = Field(..., description="Nom de la caractéristique")
    description: str = Field(..., description="Description de la caractéristique")
    unit_of_measurement: Optional[UnitOfMeasurement] = Field(None, description="Unité de mesure")

class Class(BaseModel):
    id: str = Field(..., description="Identifiant unique de la classe")
    name: str = Field(..., description="Nom de la classe")
    description: str = Field(..., description="Description de la classe")
    characteristics: List[str] = Field(default=[], description="Liste des IDs des caractéristiques")

class MaintenanceStrategy(BaseModel):
    id: str = Field(..., description="Identifiant unique de la stratégie de maintenance")
    name: str = Field(..., description="Nom de la stratégie")
    description: str = Field(..., description="Description de la stratégie")

class CycleSet(BaseModel):
    id: str = Field(..., description="Identifiant unique de l'ensemble de cycles")
    name: str = Field(..., description="Nom de l'ensemble de cycles")
    description: str = Field(..., description="Description de l'ensemble de cycles")
    cycles: List[str] = Field(..., description="Liste des cycles (ex: '6 MONTHS', '500 H')")

class WorkCenterHierarchy(BaseModel):
    id: str = Field(..., description="Identifiant unique de la hiérarchie des centres de travail")
    name: str = Field(..., description="Nom de la hiérarchie")
    description: str = Field(..., description="Description de la hiérarchie")

class WorkCenter(BaseModel):
    id: str = Field(..., description="Identifiant unique du centre de travail")
    name: str = Field(..., description="Nom du centre de travail")
    cost_center: str = Field(..., description="Centre de coûts")
    employee_id: Optional[str] = Field(None, description="ID de l'employé responsable")
    hierarchy_id: Optional[str] = Field(None, description="ID de la hiérarchie des centres de travail")

class Material(BaseModel):
    id: str = Field(..., description="Identifiant unique du matériel")
    name: str = Field(..., description="Nom du matériel")
    description: str = Field(..., description="Description du matériel")
    cost_center: str = Field(..., description="Centre de coûts")
    profit_center: str = Field(..., description="Centre de profit")
    uom: UnitOfMeasurement = Field(..., description="Unité de mesure")

class BillOfMaterial(BaseModel):
    id: str = Field(..., description="Identifiant unique de la nomenclature")
    name: str = Field(..., description="Nom de la nomenclature")
    material_id: str = Field(..., description="ID du matériel principal")

class FunctionalLocation(BaseModel):
    id: str = Field(..., description="Identifiant unique du poste technique")
    name: str = Field(..., description="Nom du poste technique")
    description: str = Field(..., description="Description du poste technique")
    main_work_center_id: Optional[str] = Field(None, description="ID du centre de travail principal")
    cost_center: str = Field(..., description="Centre de coûts")
    class_id: Optional[str] = Field(None, description="ID de la classe")
    characteristics: List[str] = Field(default=[], description="Liste des IDs des caractéristiques")
    asset_id: Optional[str] = Field(None, description="ID de l'actif")
    permits: List[str] = Field(default=[], description="Liste des IDs des permis")

class Equipment(BaseModel):
    id: str = Field(..., description="Identifiant unique de l'équipement")
    name: str = Field(..., description="Nom de l'équipement")
    description: str = Field(..., description="Description de l'équipement")
    functional_location_id: str = Field(..., description="ID du poste technique")
    main_work_center_id: Optional[str] = Field(None, description="ID du centre de travail principal")
    cost_center: str = Field(..., description="Centre de coûts")
    class_id: Optional[str] = Field(None, description="ID de la classe")
    characteristics: List[str] = Field(default=[], description="Liste des IDs des caractéristiques")
    asset_id: Optional[str] = Field(None, description="ID de l'actif")
    permits: List[str] = Field(default=[], description="Liste des IDs des permis")

class MeasuringPoint(BaseModel):
    id: str = Field(..., description="Identifiant unique du point de mesure")
    name: str = Field(..., description="Nom du point de mesure")
    description: str = Field(..., description="Description du point de mesure")
    target_object_type: str = Field(..., description="Type d'objet cible: 'EQUIPMENT' ou 'FUNCTIONAL_LOCATION'")
    target_object_id: str = Field(..., description="ID de l'objet cible")
    characteristic_id: str = Field(..., description="ID de la caractéristique")
    catalog_code_groups: List[str] = Field(default=[], description="Groupes de codes de catalogue")

class Counter(BaseModel):
    id: str = Field(..., description="Identifiant unique du compteur")
    name: str = Field(..., description="Nom du compteur")
    description: str = Field(..., description="Description du compteur")
    target_object_type: str = Field(..., description="Type d'objet cible: 'EQUIPMENT' ou 'FUNCTIONAL_LOCATION'")
    target_object_id: str = Field(..., description="ID de l'objet cible")
    characteristic_id: str = Field(..., description="ID de la caractéristique")
    current_reading: float = Field(..., description="Lecture actuelle du compteur")

class SerialNumber(BaseModel):
    id: str = Field(..., description="Identifiant unique du numéro de série")
    serial_number: str = Field(..., description="Numéro de série")
    material_id: str = Field(..., description="ID du matériel")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement")

class FunctionalLocationBOM(BaseModel):
    id: str = Field(..., description="Identifiant unique de la nomenclature du poste technique")
    functional_location_id: str = Field(..., description="ID du poste technique")
    material_master_id: str = Field(..., description="ID du matériel maître")

class EquipmentBOM(BaseModel):
    id: str = Field(..., description="Identifiant unique de la nomenclature de l'équipement")
    equipment_id: str = Field(..., description="ID de l'équipement")
    material_master_id: str = Field(..., description="ID du matériel maître")

class GeneralTaskList(BaseModel):
    id: str = Field(..., description="Identifiant unique de la gamme générale")
    name: str = Field(..., description="Nom de la gamme")
    main_work_center_id: Optional[str] = Field(None, description="ID du centre de travail principal")
    maintenance_strategy_id: Optional[str] = Field(None, description="ID de la stratégie de maintenance")
    material_id: Optional[str] = Field(None, description="ID du matériel")
    activity_type: ActivityType = Field(..., description="Type d'activité")

class EquipmentTaskList(BaseModel):
    id: str = Field(..., description="Identifiant unique de la gamme pour équipement")
    name: str = Field(..., description="Nom de la gamme")
    equipment_id: str = Field(..., description="ID de l'équipement")
    main_work_center_id: Optional[str] = Field(None, description="ID du centre de travail principal")
    maintenance_strategy_id: Optional[str] = Field(None, description="ID de la stratégie de maintenance")
    material_id: Optional[str] = Field(None, description="ID du matériel")
    activity_type: ActivityType = Field(..., description="Type d'activité")

class FunctionalLocationTaskList(BaseModel):
    id: str = Field(..., description="Identifiant unique de la gamme pour poste technique")
    name: str = Field(..., description="Nom de la gamme")
    functional_location_id: str = Field(..., description="ID du poste technique")
    main_work_center_id: Optional[str] = Field(None, description="ID du centre de travail principal")
    maintenance_strategy_id: Optional[str] = Field(None, description="ID de la stratégie de maintenance")
    material_id: Optional[str] = Field(None, description="ID du matériel")
    activity_type: ActivityType = Field(..., description="Type d'activité")

class SingleCyclePlan(BaseModel):
    id: str = Field(..., description="Identifiant unique du plan à cycle simple")
    name: str = Field(..., description="Nom du plan")
    task_list_id: str = Field(..., description="ID de la gamme")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement")
    functional_location_id: Optional[str] = Field(None, description="ID du poste technique")
    counter_id: Optional[str] = Field(None, description="ID du compteur")

class StrategyMaintenancePlan(BaseModel):
    id: str = Field(..., description="Identifiant unique du plan de maintenance stratégique")
    name: str = Field(..., description="Nom du plan")
    task_list_id: str = Field(..., description="ID de la gamme")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement")
    functional_location_id: Optional[str] = Field(None, description="ID du poste technique")
    counter_id: Optional[str] = Field(None, description="ID du compteur")
    maintenance_strategy_id: str = Field(..., description="ID de la stratégie de maintenance")

class MultipleCounterPlan(BaseModel):
    id: str = Field(..., description="Identifiant unique du plan à plusieurs compteurs")
    name: str = Field(..., description="Nom du plan")
    task_list_id: str = Field(..., description="ID de la gamme")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement")
    functional_location_id: Optional[str] = Field(None, description="ID du poste technique")
    counter_id: Optional[str] = Field(None, description="ID du compteur")
    cycle_set_id: str = Field(..., description="ID de l'ensemble de cycles")

class CharacteristicValues(BaseModel):
    id: str = Field(..., description="Identifiant unique de la valeur caractéristique")
    class_id: str = Field(..., description="ID de la classe")
    characteristic_id: str = Field(..., description="ID de la caractéristique")
    value: str = Field(..., description="Valeur de la caractéristique")
    master_data_object_id: str = Field(..., description="ID de l'objet de données maître")
    master_data_object_type: str = Field(..., description="Type d'objet: 'EQUIPMENT', 'FUNCTIONAL_LOCATION', etc.")

# ============================================================================
# SCHÉMAS POUR NOTIFICATIONS ET ORDRES
# ============================================================================

class NotificationStatus(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class NotificationPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class NotificationType(str, Enum):
    BREAKDOWN = "BREAKDOWN"
    PREVENTIVE = "PREVENTIVE"
    INSPECTION = "INSPECTION"
    CALIBRATION = "CALIBRATION"
    SAFETY = "SAFETY"
    QUALITY = "QUALITY"

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    RELEASED = "RELEASED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderType(str, Enum):
    PREVENTIVE = "PREVENTIVE"
    CORRECTIVE = "CORRECTIVE"
    INSPECTION = "INSPECTION"
    CALIBRATION = "CALIBRATION"
    EMERGENCY = "EMERGENCY"

class Notification(BaseModel):
    id: Optional[str] = Field(None, description="Identifiant unique de la notification")
    title: str = Field(..., description="Titre de la notification")
    description: str = Field(..., description="Description détaillée de la notification")
    status: NotificationStatus = Field(..., description="Statut de la notification")
    priority: NotificationPriority = Field(..., description="Priorité de la notification")
    notification_type: NotificationType = Field(..., description="Type de notification")
    created_date: datetime = Field(..., description="Date de création")
    created_by: str = Field(..., description="Utilisateur qui a créé la notification")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement concerné")
    functional_location_id: Optional[str] = Field(None, description="ID du poste technique concerné")
    work_center_id: Optional[str] = Field(None, description="ID du centre de travail responsable")
    assigned_to: Optional[str] = Field(None, description="Utilisateur assigné à la notification")
    estimated_duration: Optional[float] = Field(None, description="Durée estimée en heures")
    actual_duration: Optional[float] = Field(None, description="Durée réelle en heures")
    completion_date: Optional[datetime] = Field(None, description="Date de completion")
    related_orders: List[str] = Field(default=[], description="Liste des IDs des ordres liés")

class Order(BaseModel):
    id: Optional[str] = Field(None, description="Identifiant unique de l'ordre")
    order_number: str = Field(..., description="Numéro d'ordre")
    title: str = Field(..., description="Titre de l'ordre")
    description: str = Field(..., description="Description détaillée de l'ordre")
    status: OrderStatus = Field(..., description="Statut de l'ordre")
    order_type: OrderType = Field(..., description="Type d'ordre")
    created_date: datetime = Field(..., description="Date de création")
    created_by: str = Field(..., description="Utilisateur qui a créé l'ordre")
    equipment_id: Optional[str] = Field(None, description="ID de l'équipement concerné")
    functional_location_id: Optional[str] = Field(None, description="ID du poste technique concerné")
    work_center_id: Optional[str] = Field(None, description="ID du centre de travail responsable")
    assigned_to: Optional[str] = Field(None, description="Utilisateur assigné à l'ordre")
    planned_start_date: Optional[datetime] = Field(None, description="Date de début planifiée")
    planned_end_date: Optional[datetime] = Field(None, description="Date de fin planifiée")
    actual_start_date: Optional[datetime] = Field(None, description="Date de début réelle")
    actual_end_date: Optional[datetime] = Field(None, description="Date de fin réelle")
    estimated_duration: Optional[float] = Field(None, description="Durée estimée en heures")
    actual_duration: Optional[float] = Field(None, description="Durée réelle en heures")
    priority: NotificationPriority = Field(..., description="Priorité de l'ordre")
    cost_center: str = Field(..., description="Centre de coûts")
    materials_required: List[str] = Field(default=[], description="Liste des IDs des matériaux requis")
    related_notifications: List[str] = Field(default=[], description="Liste des IDs des notifications liées")
    task_list_id: Optional[str] = Field(None, description="ID de la gamme associée")

# Modèles de réponse pour les listes
class CatalogList(BaseModel):
    catalogs: List[Catalog]

class PermitList(BaseModel):
    permits: List[Permit]

class CharacteristicList(BaseModel):
    characteristics: List[Characteristic]

class ClassList(BaseModel):
    classes: List[Class]

class MaintenanceStrategyList(BaseModel):
    strategies: List[MaintenanceStrategy]

class CycleSetList(BaseModel):
    cycle_sets: List[CycleSet]

class WorkCenterHierarchyList(BaseModel):
    hierarchies: List[WorkCenterHierarchy]

class WorkCenterList(BaseModel):
    work_centers: List[WorkCenter]

class MaterialList(BaseModel):
    materials: List[Material]

class BillOfMaterialList(BaseModel):
    boms: List[BillOfMaterial]

class FunctionalLocationList(BaseModel):
    functional_locations: List[FunctionalLocation]

class EquipmentList(BaseModel):
    equipment: List[Equipment]

class MeasuringPointList(BaseModel):
    measuring_points: List[MeasuringPoint]

class CounterList(BaseModel):
    counters: List[Counter]

class SerialNumberList(BaseModel):
    serial_numbers: List[SerialNumber]

class FunctionalLocationBOMList(BaseModel):
    fl_boms: List[FunctionalLocationBOM]

class EquipmentBOMList(BaseModel):
    eq_boms: List[EquipmentBOM]

class GeneralTaskListList(BaseModel):
    general_task_lists: List[GeneralTaskList]

class EquipmentTaskListList(BaseModel):
    equipment_task_lists: List[EquipmentTaskList]

class FunctionalLocationTaskListList(BaseModel):
    fl_task_lists: List[FunctionalLocationTaskList]

class SingleCyclePlanList(BaseModel):
    single_cycle_plans: List[SingleCyclePlan]

class StrategyMaintenancePlanList(BaseModel):
    strategy_plans: List[StrategyMaintenancePlan]

class MultipleCounterPlanList(BaseModel):
    multiple_counter_plans: List[MultipleCounterPlan]

class CharacteristicValuesList(BaseModel):
    characteristic_values: List[CharacteristicValues]

class NotificationList(BaseModel):
    notifications: List[Notification]

class OrderList(BaseModel):
    orders: List[Order] 