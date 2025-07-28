"""
Module CRUD pour le simulateur SAP PM
Contient toutes les opérations CRUD pour les entités SAP PM
"""

from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from database import get_database, generate_id
from schemas import *

# ============================================================================
# CRUD OPERATIONS FOR CATALOG
# ============================================================================

async def create_catalog(catalog: Catalog) -> Catalog:
    """Crée un nouveau catalogue"""
    catalog.id = generate_id()
    db = get_database()
    await db.catalogs.insert_one(catalog.dict())
    return catalog

async def get_catalog(catalog_id: str) -> Optional[Catalog]:
    """Récupère un catalogue par ID"""
    db = get_database()
    result = await db.catalogs.find_one({"id": catalog_id})
    return Catalog(**result) if result else None

async def get_all_catalogs() -> List[Catalog]:
    """Récupère tous les catalogues"""
    db = get_database()
    results = await db.catalogs.find().to_list(length=None)
    return [Catalog(**result) for result in results]

async def update_catalog(catalog_id: str, catalog: Catalog) -> Catalog:
    """Met à jour un catalogue"""
    catalog.id = catalog_id
    db = get_database()
    result = await db.catalogs.replace_one({"id": catalog_id}, catalog.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Catalogue non trouvé")
    return catalog

async def delete_catalog(catalog_id: str) -> bool:
    """Supprime un catalogue"""
    db = get_database()
    result = await db.catalogs.delete_one({"id": catalog_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR PERMIT
# ============================================================================

async def create_permit(permit: Permit) -> Permit:
    """Crée un nouveau permis"""
    permit.id = generate_id()
    db = get_database()
    await db.permits.insert_one(permit.dict())
    return permit

async def get_permit(permit_id: str) -> Optional[Permit]:
    """Récupère un permis par ID"""
    db = get_database()
    result = await db.permits.find_one({"id": permit_id})
    return Permit(**result) if result else None

async def get_all_permits() -> List[Permit]:
    """Récupère tous les permis"""
    db = get_database()
    results = await db.permits.find().to_list(length=None)
    return [Permit(**result) for result in results]

async def update_permit(permit_id: str, permit: Permit) -> Permit:
    """Met à jour un permis"""
    permit.id = permit_id
    db = get_database()
    result = await db.permits.replace_one({"id": permit_id}, permit.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Permis non trouvé")
    return permit

async def delete_permit(permit_id: str) -> bool:
    """Supprime un permis"""
    db = get_database()
    result = await db.permits.delete_one({"id": permit_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR CHARACTERISTIC
# ============================================================================

async def create_characteristic(characteristic: Characteristic) -> Characteristic:
    """Crée une nouvelle caractéristique"""
    characteristic.id = generate_id()
    await get_database().characteristics.insert_one(characteristic.dict())
    return characteristic

async def get_characteristic(characteristic_id: str) -> Optional[Characteristic]:
    """Récupère une caractéristique par ID"""
    result = await get_database().characteristics.find_one({"id": characteristic_id})
    return Characteristic(**result) if result else None

async def get_all_characteristics() -> List[Characteristic]:
    """Récupère toutes les caractéristiques"""
    results = await get_database().characteristics.find().to_list(length=None)
    return [Characteristic(**result) for result in results]

async def update_characteristic(characteristic_id: str, characteristic: Characteristic) -> Characteristic:
    """Met à jour une caractéristique"""
    characteristic.id = characteristic_id
    result = await get_database().characteristics.replace_one({"id": characteristic_id}, characteristic.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Caractéristique non trouvée")
    return characteristic

async def delete_characteristic(characteristic_id: str) -> bool:
    """Supprime une caractéristique"""
    result = await get_database().characteristics.delete_one({"id": characteristic_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR CLASS
# ============================================================================

async def create_class(cls: Class) -> Class:
    """Crée une nouvelle classe"""
    cls.id = generate_id()
    await get_database().classes.insert_one(cls.dict())
    return cls

async def get_class(class_id: str) -> Optional[Class]:
    """Récupère une classe par ID"""
    result = await get_database().classes.find_one({"id": class_id})
    return Class(**result) if result else None

async def get_all_classes() -> List[Class]:
    """Récupère toutes les classes"""
    results = await get_database().classes.find().to_list(length=None)
    return [Class(**result) for result in results]

async def update_class(class_id: str, cls: Class) -> Class:
    """Met à jour une classe"""
    cls.id = class_id
    result = await get_database().classes.replace_one({"id": class_id}, cls.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return cls

async def delete_class(class_id: str) -> bool:
    """Supprime une classe"""
    result = await get_database().classes.delete_one({"id": class_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR MAINTENANCE STRATEGY
# ============================================================================

async def create_maintenance_strategy(strategy: MaintenanceStrategy) -> MaintenanceStrategy:
    """Crée une nouvelle stratégie de maintenance"""
    strategy.id = generate_id()
    await get_database().maintenance_strategies.insert_one(strategy.dict())
    return strategy

async def get_maintenance_strategy(strategy_id: str) -> Optional[MaintenanceStrategy]:
    """Récupère une stratégie de maintenance par ID"""
    result = await get_database().maintenance_strategies.find_one({"id": strategy_id})
    return MaintenanceStrategy(**result) if result else None

async def get_all_maintenance_strategies() -> List[MaintenanceStrategy]:
    """Récupère toutes les stratégies de maintenance"""
    results = await get_database().maintenance_strategies.find().to_list(length=None)
    return [MaintenanceStrategy(**result) for result in results]

async def update_maintenance_strategy(strategy_id: str, strategy: MaintenanceStrategy) -> MaintenanceStrategy:
    """Met à jour une stratégie de maintenance"""
    strategy.id = strategy_id
    result = await get_database().maintenance_strategies.replace_one({"id": strategy_id}, strategy.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Stratégie de maintenance non trouvée")
    return strategy

async def delete_maintenance_strategy(strategy_id: str) -> bool:
    """Supprime une stratégie de maintenance"""
    result = await get_database().maintenance_strategies.delete_one({"id": strategy_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR CYCLE SET
# ============================================================================

async def create_cycle_set(cycle_set: CycleSet) -> CycleSet:
    """Crée un nouvel ensemble de cycles"""
    cycle_set.id = generate_id()
    await get_database().cycle_sets.insert_one(cycle_set.dict())
    return cycle_set

async def get_cycle_set(cycle_set_id: str) -> Optional[CycleSet]:
    """Récupère un ensemble de cycles par ID"""
    result = await get_database().cycle_sets.find_one({"id": cycle_set_id})
    return CycleSet(**result) if result else None

async def get_all_cycle_sets() -> List[CycleSet]:
    """Récupère tous les ensembles de cycles"""
    results = await get_database().cycle_sets.find().to_list(length=None)
    return [CycleSet(**result) for result in results]

async def update_cycle_set(cycle_set_id: str, cycle_set: CycleSet) -> CycleSet:
    """Met à jour un ensemble de cycles"""
    cycle_set.id = cycle_set_id
    result = await get_database().cycle_sets.replace_one({"id": cycle_set_id}, cycle_set.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Ensemble de cycles non trouvé")
    return cycle_set

async def delete_cycle_set(cycle_set_id: str) -> bool:
    """Supprime un ensemble de cycles"""
    result = await get_database().cycle_sets.delete_one({"id": cycle_set_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR WORK CENTER HIERARCHY
# ============================================================================

async def create_work_center_hierarchy(hierarchy: WorkCenterHierarchy) -> WorkCenterHierarchy:
    """Crée une nouvelle hiérarchie de centre de travail"""
    hierarchy.id = generate_id()
    await get_database().work_center_hierarchies.insert_one(hierarchy.dict())
    return hierarchy

async def get_work_center_hierarchy(hierarchy_id: str) -> Optional[WorkCenterHierarchy]:
    """Récupère une hiérarchie de centre de travail par ID"""
    result = await get_database().work_center_hierarchies.find_one({"id": hierarchy_id})
    return WorkCenterHierarchy(**result) if result else None

async def get_all_work_center_hierarchies() -> List[WorkCenterHierarchy]:
    """Récupère toutes les hiérarchies de centres de travail"""
    results = await get_database().work_center_hierarchies.find().to_list(length=None)
    return [WorkCenterHierarchy(**result) for result in results]

async def update_work_center_hierarchy(hierarchy_id: str, hierarchy: WorkCenterHierarchy) -> WorkCenterHierarchy:
    """Met à jour une hiérarchie de centre de travail"""
    hierarchy.id = hierarchy_id
    result = await get_database().work_center_hierarchies.replace_one({"id": hierarchy_id}, hierarchy.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Hiérarchie de centre de travail non trouvée")
    return hierarchy

async def delete_work_center_hierarchy(hierarchy_id: str) -> bool:
    """Supprime une hiérarchie de centre de travail"""
    result = await get_database().work_center_hierarchies.delete_one({"id": hierarchy_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR WORK CENTER
# ============================================================================

async def create_work_center(work_center: WorkCenter) -> WorkCenter:
    """Crée un nouveau centre de travail"""
    work_center.id = generate_id()
    await get_database().work_centers.insert_one(work_center.dict())
    return work_center

async def get_work_center(work_center_id: str) -> Optional[WorkCenter]:
    """Récupère un centre de travail par ID"""
    result = await get_database().work_centers.find_one({"id": work_center_id})
    return WorkCenter(**result) if result else None

async def get_all_work_centers() -> List[WorkCenter]:
    """Récupère tous les centres de travail"""
    results = await get_database().work_centers.find().to_list(length=None)
    return [WorkCenter(**result) for result in results]

async def update_work_center(work_center_id: str, work_center: WorkCenter) -> WorkCenter:
    """Met à jour un centre de travail"""
    work_center.id = work_center_id
    result = await get_database().work_centers.replace_one({"id": work_center_id}, work_center.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Centre de travail non trouvé")
    return work_center

async def delete_work_center(work_center_id: str) -> bool:
    """Supprime un centre de travail"""
    result = await get_database().work_centers.delete_one({"id": work_center_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR MATERIAL
# ============================================================================

async def create_material(material: Material) -> Material:
    """Crée un nouveau matériel"""
    material.id = generate_id()
    await get_database().materials.insert_one(material.dict())
    return material

async def get_material(material_id: str) -> Optional[Material]:
    """Récupère un matériel par ID"""
    result = await get_database().materials.find_one({"id": material_id})
    return Material(**result) if result else None

async def get_all_materials() -> List[Material]:
    """Récupère tous les matériels"""
    results = await get_database().materials.find().to_list(length=None)
    return [Material(**result) for result in results]

async def update_material(material_id: str, material: Material) -> Material:
    """Met à jour un matériel"""
    material.id = material_id
    result = await get_database().materials.replace_one({"id": material_id}, material.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Matériel non trouvé")
    return material

async def delete_material(material_id: str) -> bool:
    """Supprime un matériel"""
    result = await get_database().materials.delete_one({"id": material_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR BILL OF MATERIAL
# ============================================================================

async def create_bill_of_material(bom: BillOfMaterial) -> BillOfMaterial:
    """Crée une nouvelle nomenclature"""
    bom.id = generate_id()
    await get_database().bill_of_materials.insert_one(bom.dict())
    return bom

async def get_bill_of_material(bom_id: str) -> Optional[BillOfMaterial]:
    """Récupère une nomenclature par ID"""
    result = await get_database().bill_of_materials.find_one({"id": bom_id})
    return BillOfMaterial(**result) if result else None

async def get_all_bill_of_materials() -> List[BillOfMaterial]:
    """Récupère toutes les nomenclatures"""
    results = await get_database().bill_of_materials.find().to_list(length=None)
    return [BillOfMaterial(**result) for result in results]

async def update_bill_of_material(bom_id: str, bom: BillOfMaterial) -> BillOfMaterial:
    """Met à jour une nomenclature"""
    bom.id = bom_id
    result = await get_database().bill_of_materials.replace_one({"id": bom_id}, bom.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Nomenclature non trouvée")
    return bom

async def delete_bill_of_material(bom_id: str) -> bool:
    """Supprime une nomenclature"""
    result = await get_database().bill_of_materials.delete_one({"id": bom_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR FUNCTIONAL LOCATION
# ============================================================================

async def create_functional_location(fl: FunctionalLocation) -> FunctionalLocation:
    """Crée un nouveau poste technique"""
    fl.id = generate_id()
    await get_database().functional_locations.insert_one(fl.dict())
    return fl

async def get_functional_location(fl_id: str) -> Optional[FunctionalLocation]:
    """Récupère un poste technique par ID"""
    result = await get_database().functional_locations.find_one({"id": fl_id})
    return FunctionalLocation(**result) if result else None

async def get_all_functional_locations() -> List[FunctionalLocation]:
    """Récupère tous les postes techniques"""
    results = await get_database().functional_locations.find().to_list(length=None)
    return [FunctionalLocation(**result) for result in results]

async def update_functional_location(fl_id: str, fl: FunctionalLocation) -> FunctionalLocation:
    """Met à jour un poste technique"""
    fl.id = fl_id
    result = await get_database().functional_locations.replace_one({"id": fl_id}, fl.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Poste technique non trouvé")
    return fl

async def delete_functional_location(fl_id: str) -> bool:
    """Supprime un poste technique"""
    result = await get_database().functional_locations.delete_one({"id": fl_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR EQUIPMENT
# ============================================================================

async def create_equipment(equipment: Equipment) -> Equipment:
    """Crée un nouvel équipement"""
    equipment.id = generate_id()
    await get_database().equipment.insert_one(equipment.dict())
    return equipment

async def get_equipment(equipment_id: str) -> Optional[Equipment]:
    """Récupère un équipement par ID"""
    result = await get_database().equipment.find_one({"id": equipment_id})
    return Equipment(**result) if result else None

async def get_all_equipment() -> List[Equipment]:
    """Récupère tous les équipements"""
    results = await get_database().equipment.find().to_list(length=None)
    return [Equipment(**result) for result in results]

async def update_equipment(equipment_id: str, equipment: Equipment) -> Equipment:
    """Met à jour un équipement"""
    equipment.id = equipment_id
    result = await get_database().equipment.replace_one({"id": equipment_id}, equipment.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return equipment

async def delete_equipment(equipment_id: str) -> bool:
    """Supprime un équipement"""
    result = await get_database().equipment.delete_one({"id": equipment_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR MEASURING POINT
# ============================================================================

async def create_measuring_point(mp: MeasuringPoint) -> MeasuringPoint:
    """Crée un nouveau point de mesure"""
    mp.id = generate_id()
    await get_database().measuring_points.insert_one(mp.dict())
    return mp

async def get_measuring_point(mp_id: str) -> Optional[MeasuringPoint]:
    """Récupère un point de mesure par ID"""
    result = await get_database().measuring_points.find_one({"id": mp_id})
    return MeasuringPoint(**result) if result else None

async def get_all_measuring_points() -> List[MeasuringPoint]:
    """Récupère tous les points de mesure"""
    results = await get_database().measuring_points.find().to_list(length=None)
    return [MeasuringPoint(**result) for result in results]

async def update_measuring_point(mp_id: str, mp: MeasuringPoint) -> MeasuringPoint:
    """Met à jour un point de mesure"""
    mp.id = mp_id
    result = await get_database().measuring_points.replace_one({"id": mp_id}, mp.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Point de mesure non trouvé")
    return mp

async def delete_measuring_point(mp_id: str) -> bool:
    """Supprime un point de mesure"""
    result = await get_database().measuring_points.delete_one({"id": mp_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR COUNTER
# ============================================================================

async def create_counter(counter: Counter) -> Counter:
    """Crée un nouveau compteur"""
    counter.id = generate_id()
    await get_database().counters.insert_one(counter.dict())
    return counter

async def get_counter(counter_id: str) -> Optional[Counter]:
    """Récupère un compteur par ID"""
    result = await get_database().counters.find_one({"id": counter_id})
    return Counter(**result) if result else None

async def get_all_counters() -> List[Counter]:
    """Récupère tous les compteurs"""
    results = await get_database().counters.find().to_list(length=None)
    return [Counter(**result) for result in results]

async def update_counter(counter_id: str, counter: Counter) -> Counter:
    """Met à jour un compteur"""
    counter.id = counter_id
    result = await get_database().counters.replace_one({"id": counter_id}, counter.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    return counter

async def delete_counter(counter_id: str) -> bool:
    """Supprime un compteur"""
    result = await get_database().counters.delete_one({"id": counter_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR SERIAL NUMBER
# ============================================================================

async def create_serial_number(sn: SerialNumber) -> SerialNumber:
    """Crée un nouveau numéro de série"""
    sn.id = generate_id()
    await get_database().serial_numbers.insert_one(sn.dict())
    return sn

async def get_serial_number(sn_id: str) -> Optional[SerialNumber]:
    """Récupère un numéro de série par ID"""
    result = await get_database().serial_numbers.find_one({"id": sn_id})
    return SerialNumber(**result) if result else None

async def get_all_serial_numbers() -> List[SerialNumber]:
    """Récupère tous les numéros de série"""
    results = await get_database().serial_numbers.find().to_list(length=None)
    return [SerialNumber(**result) for result in results]

async def update_serial_number(sn_id: str, sn: SerialNumber) -> SerialNumber:
    """Met à jour un numéro de série"""
    sn.id = sn_id
    result = await get_database().serial_numbers.replace_one({"id": sn_id}, sn.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Numéro de série non trouvé")
    return sn

async def delete_serial_number(sn_id: str) -> bool:
    """Supprime un numéro de série"""
    result = await get_database().serial_numbers.delete_one({"id": sn_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR FUNCTIONAL LOCATION BOM
# ============================================================================

async def create_functional_location_bom(fl_bom: FunctionalLocationBOM) -> FunctionalLocationBOM:
    """Crée une nouvelle nomenclature de poste technique"""
    fl_bom.id = generate_id()
    await get_database().functional_location_boms.insert_one(fl_bom.dict())
    return fl_bom

async def get_functional_location_bom(fl_bom_id: str) -> Optional[FunctionalLocationBOM]:
    """Récupère une nomenclature de poste technique par ID"""
    result = await get_database().functional_location_boms.find_one({"id": fl_bom_id})
    return FunctionalLocationBOM(**result) if result else None

async def get_all_functional_location_boms() -> List[FunctionalLocationBOM]:
    """Récupère toutes les nomenclatures de postes techniques"""
    results = await get_database().functional_location_boms.find().to_list(length=None)
    return [FunctionalLocationBOM(**result) for result in results]

async def update_functional_location_bom(fl_bom_id: str, fl_bom: FunctionalLocationBOM) -> FunctionalLocationBOM:
    """Met à jour une nomenclature de poste technique"""
    fl_bom.id = fl_bom_id
    result = await get_database().functional_location_boms.replace_one({"id": fl_bom_id}, fl_bom.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Nomenclature de poste technique non trouvée")
    return fl_bom

async def delete_functional_location_bom(fl_bom_id: str) -> bool:
    """Supprime une nomenclature de poste technique"""
    result = await get_database().functional_location_boms.delete_one({"id": fl_bom_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR EQUIPMENT BOM
# ============================================================================

async def create_equipment_bom(eq_bom: EquipmentBOM) -> EquipmentBOM:
    """Crée une nouvelle nomenclature d'équipement"""
    eq_bom.id = generate_id()
    await get_database().equipment_boms.insert_one(eq_bom.dict())
    return eq_bom

async def get_equipment_bom(eq_bom_id: str) -> Optional[EquipmentBOM]:
    """Récupère une nomenclature d'équipement par ID"""
    result = await get_database().equipment_boms.find_one({"id": eq_bom_id})
    return EquipmentBOM(**result) if result else None

async def get_all_equipment_boms() -> List[EquipmentBOM]:
    """Récupère toutes les nomenclatures d'équipements"""
    results = await get_database().equipment_boms.find().to_list(length=None)
    return [EquipmentBOM(**result) for result in results]

async def update_equipment_bom(eq_bom_id: str, eq_bom: EquipmentBOM) -> EquipmentBOM:
    """Met à jour une nomenclature d'équipement"""
    eq_bom.id = eq_bom_id
    result = await get_database().equipment_boms.replace_one({"id": eq_bom_id}, eq_bom.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Nomenclature d'équipement non trouvée")
    return eq_bom

async def delete_equipment_bom(eq_bom_id: str) -> bool:
    """Supprime une nomenclature d'équipement"""
    result = await get_database().equipment_boms.delete_one({"id": eq_bom_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR GENERAL TASK LIST
# ============================================================================

async def create_general_task_list(gtl: GeneralTaskList) -> GeneralTaskList:
    """Crée une nouvelle gamme générale"""
    gtl.id = generate_id()
    await get_database().general_task_lists.insert_one(gtl.dict())
    return gtl

async def get_general_task_list(gtl_id: str) -> Optional[GeneralTaskList]:
    """Récupère une gamme générale par ID"""
    result = await get_database().general_task_lists.find_one({"id": gtl_id})
    return GeneralTaskList(**result) if result else None

async def get_all_general_task_lists() -> List[GeneralTaskList]:
    """Récupère toutes les gammes générales"""
    results = await get_database().general_task_lists.find().to_list(length=None)
    return [GeneralTaskList(**result) for result in results]

async def update_general_task_list(gtl_id: str, gtl: GeneralTaskList) -> GeneralTaskList:
    """Met à jour une gamme générale"""
    gtl.id = gtl_id
    result = await get_database().general_task_lists.replace_one({"id": gtl_id}, gtl.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Gamme générale non trouvée")
    return gtl

async def delete_general_task_list(gtl_id: str) -> bool:
    """Supprime une gamme générale"""
    result = await get_database().general_task_lists.delete_one({"id": gtl_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR EQUIPMENT TASK LIST
# ============================================================================

async def create_equipment_task_list(etl: EquipmentTaskList) -> EquipmentTaskList:
    """Crée une nouvelle gamme pour équipement"""
    etl.id = generate_id()
    await get_database().equipment_task_lists.insert_one(etl.dict())
    return etl

async def get_equipment_task_list(etl_id: str) -> Optional[EquipmentTaskList]:
    """Récupère une gamme pour équipement par ID"""
    result = await get_database().equipment_task_lists.find_one({"id": etl_id})
    return EquipmentTaskList(**result) if result else None

async def get_all_equipment_task_lists() -> List[EquipmentTaskList]:
    """Récupère toutes les gammes pour équipements"""
    results = await get_database().equipment_task_lists.find().to_list(length=None)
    return [EquipmentTaskList(**result) for result in results]

async def update_equipment_task_list(etl_id: str, etl: EquipmentTaskList) -> EquipmentTaskList:
    """Met à jour une gamme pour équipement"""
    etl.id = etl_id
    result = await get_database().equipment_task_lists.replace_one({"id": etl_id}, etl.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Gamme pour équipement non trouvée")
    return etl

async def delete_equipment_task_list(etl_id: str) -> bool:
    """Supprime une gamme pour équipement"""
    result = await get_database().equipment_task_lists.delete_one({"id": etl_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR FUNCTIONAL LOCATION TASK LIST
# ============================================================================

async def create_functional_location_task_list(fltl: FunctionalLocationTaskList) -> FunctionalLocationTaskList:
    """Crée une nouvelle gamme pour poste technique"""
    fltl.id = generate_id()
    await get_database().functional_location_task_lists.insert_one(fltl.dict())
    return fltl

async def get_functional_location_task_list(fltl_id: str) -> Optional[FunctionalLocationTaskList]:
    """Récupère une gamme pour poste technique par ID"""
    result = await get_database().functional_location_task_lists.find_one({"id": fltl_id})
    return FunctionalLocationTaskList(**result) if result else None

async def get_all_functional_location_task_lists() -> List[FunctionalLocationTaskList]:
    """Récupère toutes les gammes pour postes techniques"""
    results = await get_database().functional_location_task_lists.find().to_list(length=None)
    return [FunctionalLocationTaskList(**result) for result in results]

async def update_functional_location_task_list(fltl_id: str, fltl: FunctionalLocationTaskList) -> FunctionalLocationTaskList:
    """Met à jour une gamme pour poste technique"""
    fltl.id = fltl_id
    result = await get_database().functional_location_task_lists.replace_one({"id": fltl_id}, fltl.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Gamme pour poste technique non trouvée")
    return fltl

async def delete_functional_location_task_list(fltl_id: str) -> bool:
    """Supprime une gamme pour poste technique"""
    result = await get_database().functional_location_task_lists.delete_one({"id": fltl_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR SINGLE CYCLE PLAN
# ============================================================================

async def create_single_cycle_plan(scp: SingleCyclePlan) -> SingleCyclePlan:
    """Crée un nouveau plan à cycle simple"""
    scp.id = generate_id()
    await get_database().single_cycle_plans.insert_one(scp.dict())
    return scp

async def get_single_cycle_plan(scp_id: str) -> Optional[SingleCyclePlan]:
    """Récupère un plan à cycle simple par ID"""
    result = await get_database().single_cycle_plans.find_one({"id": scp_id})
    return SingleCyclePlan(**result) if result else None

async def get_all_single_cycle_plans() -> List[SingleCyclePlan]:
    """Récupère tous les plans à cycle simple"""
    results = await get_database().single_cycle_plans.find().to_list(length=None)
    return [SingleCyclePlan(**result) for result in results]

async def update_single_cycle_plan(scp_id: str, scp: SingleCyclePlan) -> SingleCyclePlan:
    """Met à jour un plan à cycle simple"""
    scp.id = scp_id
    result = await get_database().single_cycle_plans.replace_one({"id": scp_id}, scp.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Plan à cycle simple non trouvé")
    return scp

async def delete_single_cycle_plan(scp_id: str) -> bool:
    """Supprime un plan à cycle simple"""
    result = await get_database().single_cycle_plans.delete_one({"id": scp_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR STRATEGY MAINTENANCE PLAN
# ============================================================================

async def create_strategy_maintenance_plan(smp: StrategyMaintenancePlan) -> StrategyMaintenancePlan:
    """Crée un nouveau plan de maintenance stratégique"""
    smp.id = generate_id()
    await get_database().strategy_maintenance_plans.insert_one(smp.dict())
    return smp

async def get_strategy_maintenance_plan(smp_id: str) -> Optional[StrategyMaintenancePlan]:
    """Récupère un plan de maintenance stratégique par ID"""
    result = await get_database().strategy_maintenance_plans.find_one({"id": smp_id})
    return StrategyMaintenancePlan(**result) if result else None

async def get_all_strategy_maintenance_plans() -> List[StrategyMaintenancePlan]:
    """Récupère tous les plans de maintenance stratégique"""
    results = await get_database().strategy_maintenance_plans.find().to_list(length=None)
    return [StrategyMaintenancePlan(**result) for result in results]

async def update_strategy_maintenance_plan(smp_id: str, smp: StrategyMaintenancePlan) -> StrategyMaintenancePlan:
    """Met à jour un plan de maintenance stratégique"""
    smp.id = smp_id
    result = await get_database().strategy_maintenance_plans.replace_one({"id": smp_id}, smp.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Plan de maintenance stratégique non trouvé")
    return smp

async def delete_strategy_maintenance_plan(smp_id: str) -> bool:
    """Supprime un plan de maintenance stratégique"""
    result = await get_database().strategy_maintenance_plans.delete_one({"id": smp_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR MULTIPLE COUNTER PLAN
# ============================================================================

async def create_multiple_counter_plan(mcp: MultipleCounterPlan) -> MultipleCounterPlan:
    """Crée un nouveau plan à plusieurs compteurs"""
    mcp.id = generate_id()
    await get_database().multiple_counter_plans.insert_one(mcp.dict())
    return mcp

async def get_multiple_counter_plan(mcp_id: str) -> Optional[MultipleCounterPlan]:
    """Récupère un plan à plusieurs compteurs par ID"""
    result = await get_database().multiple_counter_plans.find_one({"id": mcp_id})
    return MultipleCounterPlan(**result) if result else None

async def get_all_multiple_counter_plans() -> List[MultipleCounterPlan]:
    """Récupère tous les plans à plusieurs compteurs"""
    results = await get_database().multiple_counter_plans.find().to_list(length=None)
    return [MultipleCounterPlan(**result) for result in results]

async def update_multiple_counter_plan(mcp_id: str, mcp: MultipleCounterPlan) -> MultipleCounterPlan:
    """Met à jour un plan à plusieurs compteurs"""
    mcp.id = mcp_id
    result = await get_database().multiple_counter_plans.replace_one({"id": mcp_id}, mcp.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Plan à plusieurs compteurs non trouvé")
    return mcp

async def delete_multiple_counter_plan(mcp_id: str) -> bool:
    """Supprime un plan à plusieurs compteurs"""
    result = await get_database().multiple_counter_plans.delete_one({"id": mcp_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR CHARACTERISTIC VALUES
# ============================================================================

async def create_characteristic_values(cv: CharacteristicValues) -> CharacteristicValues:
    """Crée une nouvelle valeur caractéristique"""
    cv.id = generate_id()
    await get_database().characteristic_values.insert_one(cv.dict())
    return cv

async def get_characteristic_values(cv_id: str) -> Optional[CharacteristicValues]:
    """Récupère une valeur caractéristique par ID"""
    result = await get_database().characteristic_values.find_one({"id": cv_id})
    return CharacteristicValues(**result) if result else None

async def get_all_characteristic_values() -> List[CharacteristicValues]:
    """Récupère toutes les valeurs caractéristiques"""
    results = await get_database().characteristic_values.find().to_list(length=None)
    return [CharacteristicValues(**result) for result in results]

async def update_characteristic_values(cv_id: str, cv: CharacteristicValues) -> CharacteristicValues:
    """Met à jour une valeur caractéristique"""
    cv.id = cv_id
    result = await get_database().characteristic_values.replace_one({"id": cv_id}, cv.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Valeur caractéristique non trouvée")
    return cv

async def delete_characteristic_values(cv_id: str) -> bool:
    """Supprime une valeur caractéristique"""
    result = await get_database().characteristic_values.delete_one({"id": cv_id})
    return result.deleted_count > 0

# ============================================================================
# CRUD OPERATIONS FOR NOTIFICATIONS
# ============================================================================

async def create_notification(notification: Notification) -> Notification:
    """Crée une nouvelle notification"""
    if not notification.id:
        notification.id = generate_id()
    await get_database().notifications.insert_one(notification.dict())
    return notification

async def get_notification(notification_id: str) -> Optional[Notification]:
    """Récupère une notification par ID"""
    result = await get_database().notifications.find_one({"id": notification_id})
    return Notification(**result) if result else None

async def get_all_notifications() -> List[Notification]:
    """Récupère toutes les notifications"""
    results = await get_database().notifications.find().to_list(length=None)
    return [Notification(**result) for result in results]

async def update_notification(notification_id: str, notification: Notification) -> Notification:
    """Met à jour une notification"""
    notification.id = notification_id
    result = await get_database().notifications.replace_one({"id": notification_id}, notification.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notification

async def delete_notification(notification_id: str) -> bool:
    """Supprime une notification"""
    result = await get_database().notifications.delete_one({"id": notification_id})
    return result.deleted_count > 0

async def get_notifications_by_equipment(equipment_id: str) -> List[Notification]:
    """Récupère toutes les notifications pour un équipement"""
    results = await get_database().notifications.find({"equipment_id": equipment_id}).to_list(length=None)
    return [Notification(**result) for result in results]

async def get_notifications_by_status(status: str) -> List[Notification]:
    """Récupère toutes les notifications par statut"""
    results = await get_database().notifications.find({"status": status}).to_list(length=None)
    return [Notification(**result) for result in results]

async def get_notifications_by_priority(priority: str) -> List[Notification]:
    """Récupère toutes les notifications par priorité"""
    results = await get_database().notifications.find({"priority": priority}).to_list(length=None)
    return [Notification(**result) for result in results]

# ============================================================================
# CRUD OPERATIONS FOR ORDERS
# ============================================================================

async def create_order(order: Order) -> Order:
    """Crée un nouvel ordre"""
    if not order.id:
        order.id = generate_id()
    await get_database().orders.insert_one(order.dict())
    return order

async def get_order(order_id: str) -> Optional[Order]:
    """Récupère un ordre par ID"""
    result = await get_database().orders.find_one({"id": order_id})
    return Order(**result) if result else None

async def get_all_orders() -> List[Order]:
    """Récupère tous les ordres"""
    results = await get_database().orders.find().to_list(length=None)
    return [Order(**result) for result in results]

async def update_order(order_id: str, order: Order) -> Order:
    """Met à jour un ordre"""
    order.id = order_id
    result = await get_database().orders.replace_one({"id": order_id}, order.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Ordre non trouvé")
    return order

async def delete_order(order_id: str) -> bool:
    """Supprime un ordre"""
    result = await get_database().orders.delete_one({"id": order_id})
    return result.deleted_count > 0

async def get_orders_by_equipment(equipment_id: str) -> List[Order]:
    """Récupère tous les ordres pour un équipement"""
    results = await get_database().orders.find({"equipment_id": equipment_id}).to_list(length=None)
    return [Order(**result) for result in results]

async def get_orders_by_status(status: str) -> List[Order]:
    """Récupère tous les ordres par statut"""
    results = await get_database().orders.find({"status": status}).to_list(length=None)
    return [Order(**result) for result in results]

async def get_orders_by_type(order_type: str) -> List[Order]:
    """Récupère tous les ordres par type"""
    results = await get_database().orders.find({"order_type": order_type}).to_list(length=None)
    return [Order(**result) for result in results]

async def get_orders_by_work_center(work_center_id: str) -> List[Order]:
    """Récupère tous les ordres pour un centre de travail"""
    results = await get_database().orders.find({"work_center_id": work_center_id}).to_list(length=None)
    return [Order(**result) for result in results] 
