"""
API FastAPI pour le simulateur SAP PM
Contient tous les endpoints pour gérer les données SAP PM
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Dict, Any
import uvicorn

from database import connect_to_mongo, close_mongo_connection, initialize_sample_data
from crud import *
from schemas import *

# Configuration de l'application FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage
    await connect_to_mongo()
    await initialize_sample_data()
    yield
    # Arrêt
    await close_mongo_connection()

app = FastAPI(
    title="SAP PM Simulator API",
    description="API pour simuler les données SAP Plant Maintenance",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENDPOINTS POUR CATALOGUES
# ============================================================================

@app.post("/catalogs/", response_model=Catalog)
async def create_catalog_endpoint(catalog: Catalog):
    """Crée un nouveau catalogue"""
    return await create_catalog(catalog)

@app.get("/catalogs/", response_model=List[Catalog])
async def get_all_catalogs_endpoint():
    """Récupère tous les catalogues"""
    return await get_all_catalogs()

@app.get("/catalogs/{catalog_id}", response_model=Catalog)
async def get_catalog_endpoint(catalog_id: str):
    """Récupère un catalogue par ID"""
    catalog = await get_catalog(catalog_id)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catalogue non trouvé")
    return catalog

@app.put("/catalogs/{catalog_id}", response_model=Catalog)
async def update_catalog_endpoint(catalog_id: str, catalog: Catalog):
    """Met à jour un catalogue"""
    return await update_catalog(catalog_id, catalog)

@app.delete("/catalogs/{catalog_id}")
async def delete_catalog_endpoint(catalog_id: str):
    """Supprime un catalogue"""
    success = await delete_catalog(catalog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Catalogue non trouvé")
    return {"message": "Catalogue supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR PERMIS
# ============================================================================

@app.post("/permits/", response_model=Permit)
async def create_permit_endpoint(permit: Permit):
    """Crée un nouveau permis"""
    return await create_permit(permit)

@app.get("/permits/", response_model=List[Permit])
async def get_all_permits_endpoint():
    """Récupère tous les permis"""
    return await get_all_permits()

@app.get("/permits/{permit_id}", response_model=Permit)
async def get_permit_endpoint(permit_id: str):
    """Récupère un permis par ID"""
    permit = await get_permit(permit_id)
    if not permit:
        raise HTTPException(status_code=404, detail="Permis non trouvé")
    return permit

@app.put("/permits/{permit_id}", response_model=Permit)
async def update_permit_endpoint(permit_id: str, permit: Permit):
    """Met à jour un permis"""
    return await update_permit(permit_id, permit)

@app.delete("/permits/{permit_id}")
async def delete_permit_endpoint(permit_id: str):
    """Supprime un permis"""
    success = await delete_permit(permit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permis non trouvé")
    return {"message": "Permis supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR CARACTÉRISTIQUES
# ============================================================================

@app.post("/characteristics/", response_model=Characteristic)
async def create_characteristic_endpoint(characteristic: Characteristic):
    """Crée une nouvelle caractéristique"""
    return await create_characteristic(characteristic)

@app.get("/characteristics/", response_model=List[Characteristic])
async def get_all_characteristics_endpoint():
    """Récupère toutes les caractéristiques"""
    return await get_all_characteristics()

@app.get("/characteristics/{characteristic_id}", response_model=Characteristic)
async def get_characteristic_endpoint(characteristic_id: str):
    """Récupère une caractéristique par ID"""
    characteristic = await get_characteristic(characteristic_id)
    if not characteristic:
        raise HTTPException(status_code=404, detail="Caractéristique non trouvée")
    return characteristic

@app.put("/characteristics/{characteristic_id}", response_model=Characteristic)
async def update_characteristic_endpoint(characteristic_id: str, characteristic: Characteristic):
    """Met à jour une caractéristique"""
    return await update_characteristic(characteristic_id, characteristic)

@app.delete("/characteristics/{characteristic_id}")
async def delete_characteristic_endpoint(characteristic_id: str):
    """Supprime une caractéristique"""
    success = await delete_characteristic(characteristic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Caractéristique non trouvée")
    return {"message": "Caractéristique supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR CLASSES
# ============================================================================

@app.post("/classes/", response_model=Class)
async def create_class_endpoint(cls: Class):
    """Crée une nouvelle classe"""
    return await create_class(cls)

@app.get("/classes/", response_model=List[Class])
async def get_all_classes_endpoint():
    """Récupère toutes les classes"""
    return await get_all_classes()

@app.get("/classes/{class_id}", response_model=Class)
async def get_class_endpoint(class_id: str):
    """Récupère une classe par ID"""
    cls = await get_class(class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return cls

@app.put("/classes/{class_id}", response_model=Class)
async def update_class_endpoint(class_id: str, cls: Class):
    """Met à jour une classe"""
    return await update_class(class_id, cls)

@app.delete("/classes/{class_id}")
async def delete_class_endpoint(class_id: str):
    """Supprime une classe"""
    success = await delete_class(class_id)
    if not success:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return {"message": "Classe supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR STRATÉGIES DE MAINTENANCE
# ============================================================================

@app.post("/maintenance-strategies/", response_model=MaintenanceStrategy)
async def create_maintenance_strategy_endpoint(strategy: MaintenanceStrategy):
    """Crée une nouvelle stratégie de maintenance"""
    return await create_maintenance_strategy(strategy)

@app.get("/maintenance-strategies/", response_model=List[MaintenanceStrategy])
async def get_all_maintenance_strategies_endpoint():
    """Récupère toutes les stratégies de maintenance"""
    return await get_all_maintenance_strategies()

@app.get("/maintenance-strategies/{strategy_id}", response_model=MaintenanceStrategy)
async def get_maintenance_strategy_endpoint(strategy_id: str):
    """Récupère une stratégie de maintenance par ID"""
    strategy = await get_maintenance_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Stratégie de maintenance non trouvée")
    return strategy

@app.put("/maintenance-strategies/{strategy_id}", response_model=MaintenanceStrategy)
async def update_maintenance_strategy_endpoint(strategy_id: str, strategy: MaintenanceStrategy):
    """Met à jour une stratégie de maintenance"""
    return await update_maintenance_strategy(strategy_id, strategy)

@app.delete("/maintenance-strategies/{strategy_id}")
async def delete_maintenance_strategy_endpoint(strategy_id: str):
    """Supprime une stratégie de maintenance"""
    success = await delete_maintenance_strategy(strategy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stratégie de maintenance non trouvée")
    return {"message": "Stratégie de maintenance supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR ENSEMBLES DE CYCLES
# ============================================================================

@app.post("/cycle-sets/", response_model=CycleSet)
async def create_cycle_set_endpoint(cycle_set: CycleSet):
    """Crée un nouvel ensemble de cycles"""
    return await create_cycle_set(cycle_set)

@app.get("/cycle-sets/", response_model=List[CycleSet])
async def get_all_cycle_sets_endpoint():
    """Récupère tous les ensembles de cycles"""
    return await get_all_cycle_sets()

@app.get("/cycle-sets/{cycle_set_id}", response_model=CycleSet)
async def get_cycle_set_endpoint(cycle_set_id: str):
    """Récupère un ensemble de cycles par ID"""
    cycle_set = await get_cycle_set(cycle_set_id)
    if not cycle_set:
        raise HTTPException(status_code=404, detail="Ensemble de cycles non trouvé")
    return cycle_set

@app.put("/cycle-sets/{cycle_set_id}", response_model=CycleSet)
async def update_cycle_set_endpoint(cycle_set_id: str, cycle_set: CycleSet):
    """Met à jour un ensemble de cycles"""
    return await update_cycle_set(cycle_set_id, cycle_set)

@app.delete("/cycle-sets/{cycle_set_id}")
async def delete_cycle_set_endpoint(cycle_set_id: str):
    """Supprime un ensemble de cycles"""
    success = await delete_cycle_set(cycle_set_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ensemble de cycles non trouvé")
    return {"message": "Ensemble de cycles supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR HIÉRARCHIES DE CENTRES DE TRAVAIL
# ============================================================================

@app.post("/work-center-hierarchies/", response_model=WorkCenterHierarchy)
async def create_work_center_hierarchy_endpoint(hierarchy: WorkCenterHierarchy):
    """Crée une nouvelle hiérarchie de centre de travail"""
    return await create_work_center_hierarchy(hierarchy)

@app.get("/work-center-hierarchies/", response_model=List[WorkCenterHierarchy])
async def get_all_work_center_hierarchies_endpoint():
    """Récupère toutes les hiérarchies de centres de travail"""
    return await get_all_work_center_hierarchies()

@app.get("/work-center-hierarchies/{hierarchy_id}", response_model=WorkCenterHierarchy)
async def get_work_center_hierarchy_endpoint(hierarchy_id: str):
    """Récupère une hiérarchie de centre de travail par ID"""
    hierarchy = await get_work_center_hierarchy(hierarchy_id)
    if not hierarchy:
        raise HTTPException(status_code=404, detail="Hiérarchie de centre de travail non trouvée")
    return hierarchy

@app.put("/work-center-hierarchies/{hierarchy_id}", response_model=WorkCenterHierarchy)
async def update_work_center_hierarchy_endpoint(hierarchy_id: str, hierarchy: WorkCenterHierarchy):
    """Met à jour une hiérarchie de centre de travail"""
    return await update_work_center_hierarchy(hierarchy_id, hierarchy)

@app.delete("/work-center-hierarchies/{hierarchy_id}")
async def delete_work_center_hierarchy_endpoint(hierarchy_id: str):
    """Supprime une hiérarchie de centre de travail"""
    success = await delete_work_center_hierarchy(hierarchy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hiérarchie de centre de travail non trouvée")
    return {"message": "Hiérarchie de centre de travail supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR CENTRES DE TRAVAIL
# ============================================================================

@app.post("/work-centers/", response_model=WorkCenter)
async def create_work_center_endpoint(work_center: WorkCenter):
    """Crée un nouveau centre de travail"""
    return await create_work_center(work_center)

@app.get("/work-centers/", response_model=List[WorkCenter])
async def get_all_work_centers_endpoint():
    """Récupère tous les centres de travail"""
    return await get_all_work_centers()

@app.get("/work-centers/{work_center_id}", response_model=WorkCenter)
async def get_work_center_endpoint(work_center_id: str):
    """Récupère un centre de travail par ID"""
    work_center = await get_work_center(work_center_id)
    if not work_center:
        raise HTTPException(status_code=404, detail="Centre de travail non trouvé")
    return work_center

@app.put("/work-centers/{work_center_id}", response_model=WorkCenter)
async def update_work_center_endpoint(work_center_id: str, work_center: WorkCenter):
    """Met à jour un centre de travail"""
    return await update_work_center(work_center_id, work_center)

@app.delete("/work-centers/{work_center_id}")
async def delete_work_center_endpoint(work_center_id: str):
    """Supprime un centre de travail"""
    success = await delete_work_center(work_center_id)
    if not success:
        raise HTTPException(status_code=404, detail="Centre de travail non trouvé")
    return {"message": "Centre de travail supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR MATÉRIELS
# ============================================================================

@app.post("/materials/", response_model=Material)
async def create_material_endpoint(material: Material):
    """Crée un nouveau matériel"""
    return await create_material(material)

@app.get("/materials/", response_model=List[Material])
async def get_all_materials_endpoint():
    """Récupère tous les matériels"""
    return await get_all_materials()

@app.get("/materials/{material_id}", response_model=Material)
async def get_material_endpoint(material_id: str):
    """Récupère un matériel par ID"""
    material = await get_material(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Matériel non trouvé")
    return material

@app.put("/materials/{material_id}", response_model=Material)
async def update_material_endpoint(material_id: str, material: Material):
    """Met à jour un matériel"""
    return await update_material(material_id, material)

@app.delete("/materials/{material_id}")
async def delete_material_endpoint(material_id: str):
    """Supprime un matériel"""
    success = await delete_material(material_id)
    if not success:
        raise HTTPException(status_code=404, detail="Matériel non trouvé")
    return {"message": "Matériel supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR NOMENCLATURES
# ============================================================================

@app.post("/bill-of-materials/", response_model=BillOfMaterial)
async def create_bill_of_material_endpoint(bom: BillOfMaterial):
    """Crée une nouvelle nomenclature"""
    return await create_bill_of_material(bom)

@app.get("/bill-of-materials/", response_model=List[BillOfMaterial])
async def get_all_bill_of_materials_endpoint():
    """Récupère toutes les nomenclatures"""
    return await get_all_bill_of_materials()

@app.get("/bill-of-materials/{bom_id}", response_model=BillOfMaterial)
async def get_bill_of_material_endpoint(bom_id: str):
    """Récupère une nomenclature par ID"""
    bom = await get_bill_of_material(bom_id)
    if not bom:
        raise HTTPException(status_code=404, detail="Nomenclature non trouvée")
    return bom

@app.put("/bill-of-materials/{bom_id}", response_model=BillOfMaterial)
async def update_bill_of_material_endpoint(bom_id: str, bom: BillOfMaterial):
    """Met à jour une nomenclature"""
    return await update_bill_of_material(bom_id, bom)

@app.delete("/bill-of-materials/{bom_id}")
async def delete_bill_of_material_endpoint(bom_id: str):
    """Supprime une nomenclature"""
    success = await delete_bill_of_material(bom_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nomenclature non trouvée")
    return {"message": "Nomenclature supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR POSTES TECHNIQUES
# ============================================================================

@app.post("/functional-locations/", response_model=FunctionalLocation)
async def create_functional_location_endpoint(fl: FunctionalLocation):
    """Crée un nouveau poste technique"""
    return await create_functional_location(fl)

@app.get("/functional-locations/", response_model=List[FunctionalLocation])
async def get_all_functional_locations_endpoint():
    """Récupère tous les postes techniques"""
    return await get_all_functional_locations()

@app.get("/functional-locations/{fl_id}", response_model=FunctionalLocation)
async def get_functional_location_endpoint(fl_id: str):
    """Récupère un poste technique par ID"""
    fl = await get_functional_location(fl_id)
    if not fl:
        raise HTTPException(status_code=404, detail="Poste technique non trouvé")
    return fl

@app.put("/functional-locations/{fl_id}", response_model=FunctionalLocation)
async def update_functional_location_endpoint(fl_id: str, fl: FunctionalLocation):
    """Met à jour un poste technique"""
    return await update_functional_location(fl_id, fl)

@app.delete("/functional-locations/{fl_id}")
async def delete_functional_location_endpoint(fl_id: str):
    """Supprime un poste technique"""
    success = await delete_functional_location(fl_id)
    if not success:
        raise HTTPException(status_code=404, detail="Poste technique non trouvé")
    return {"message": "Poste technique supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR ÉQUIPEMENTS
# ============================================================================

@app.post("/equipment/", response_model=Equipment)
async def create_equipment_endpoint(equipment: Equipment):
    """Crée un nouvel équipement"""
    return await create_equipment(equipment)

@app.get("/equipment/", response_model=List[Equipment])
async def get_all_equipment_endpoint():
    """Récupère tous les équipements"""
    return await get_all_equipment()

@app.get("/equipment/{equipment_id}", response_model=Equipment)
async def get_equipment_endpoint(equipment_id: str):
    """Récupère un équipement par ID"""
    equipment = await get_equipment(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return equipment

@app.put("/equipment/{equipment_id}", response_model=Equipment)
async def update_equipment_endpoint(equipment_id: str, equipment: Equipment):
    """Met à jour un équipement"""
    return await update_equipment(equipment_id, equipment)

@app.delete("/equipment/{equipment_id}")
async def delete_equipment_endpoint(equipment_id: str):
    """Supprime un équipement"""
    success = await delete_equipment(equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return {"message": "Équipement supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR POINTS DE MESURE
# ============================================================================

@app.post("/measuring-points/", response_model=MeasuringPoint)
async def create_measuring_point_endpoint(mp: MeasuringPoint):
    """Crée un nouveau point de mesure"""
    return await create_measuring_point(mp)

@app.get("/measuring-points/", response_model=List[MeasuringPoint])
async def get_all_measuring_points_endpoint():
    """Récupère tous les points de mesure"""
    return await get_all_measuring_points()

@app.get("/measuring-points/{mp_id}", response_model=MeasuringPoint)
async def get_measuring_point_endpoint(mp_id: str):
    """Récupère un point de mesure par ID"""
    mp = await get_measuring_point(mp_id)
    if not mp:
        raise HTTPException(status_code=404, detail="Point de mesure non trouvé")
    return mp

@app.put("/measuring-points/{mp_id}", response_model=MeasuringPoint)
async def update_measuring_point_endpoint(mp_id: str, mp: MeasuringPoint):
    """Met à jour un point de mesure"""
    return await update_measuring_point(mp_id, mp)

@app.delete("/measuring-points/{mp_id}")
async def delete_measuring_point_endpoint(mp_id: str):
    """Supprime un point de mesure"""
    success = await delete_measuring_point(mp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point de mesure non trouvé")
    return {"message": "Point de mesure supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR COMPTEURS
# ============================================================================

@app.post("/counters/", response_model=Counter)
async def create_counter_endpoint(counter: Counter):
    """Crée un nouveau compteur"""
    return await create_counter(counter)

@app.get("/counters/", response_model=List[Counter])
async def get_all_counters_endpoint():
    """Récupère tous les compteurs"""
    return await get_all_counters()

@app.get("/counters/{counter_id}", response_model=Counter)
async def get_counter_endpoint(counter_id: str):
    """Récupère un compteur par ID"""
    counter = await get_counter(counter_id)
    if not counter:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    return counter

@app.put("/counters/{counter_id}", response_model=Counter)
async def update_counter_endpoint(counter_id: str, counter: Counter):
    """Met à jour un compteur"""
    return await update_counter(counter_id, counter)

@app.delete("/counters/{counter_id}")
async def delete_counter_endpoint(counter_id: str):
    """Supprime un compteur"""
    success = await delete_counter(counter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    return {"message": "Compteur supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR NUMÉROS DE SÉRIE
# ============================================================================

@app.post("/serial-numbers/", response_model=SerialNumber)
async def create_serial_number_endpoint(sn: SerialNumber):
    """Crée un nouveau numéro de série"""
    return await create_serial_number(sn)

@app.get("/serial-numbers/", response_model=List[SerialNumber])
async def get_all_serial_numbers_endpoint():
    """Récupère tous les numéros de série"""
    return await get_all_serial_numbers()

@app.get("/serial-numbers/{sn_id}", response_model=SerialNumber)
async def get_serial_number_endpoint(sn_id: str):
    """Récupère un numéro de série par ID"""
    sn = await get_serial_number(sn_id)
    if not sn:
        raise HTTPException(status_code=404, detail="Numéro de série non trouvé")
    return sn

@app.put("/serial-numbers/{sn_id}", response_model=SerialNumber)
async def update_serial_number_endpoint(sn_id: str, sn: SerialNumber):
    """Met à jour un numéro de série"""
    return await update_serial_number(sn_id, sn)

@app.delete("/serial-numbers/{sn_id}")
async def delete_serial_number_endpoint(sn_id: str):
    """Supprime un numéro de série"""
    success = await delete_serial_number(sn_id)
    if not success:
        raise HTTPException(status_code=404, detail="Numéro de série non trouvé")
    return {"message": "Numéro de série supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR NOMENCLATURES DE POSTES TECHNIQUES
# ============================================================================

@app.post("/functional-location-boms/", response_model=FunctionalLocationBOM)
async def create_functional_location_bom_endpoint(fl_bom: FunctionalLocationBOM):
    """Crée une nouvelle nomenclature de poste technique"""
    return await create_functional_location_bom(fl_bom)

@app.get("/functional-location-boms/", response_model=List[FunctionalLocationBOM])
async def get_all_functional_location_boms_endpoint():
    """Récupère toutes les nomenclatures de postes techniques"""
    return await get_all_functional_location_boms()

@app.get("/functional-location-boms/{fl_bom_id}", response_model=FunctionalLocationBOM)
async def get_functional_location_bom_endpoint(fl_bom_id: str):
    """Récupère une nomenclature de poste technique par ID"""
    fl_bom = await get_functional_location_bom(fl_bom_id)
    if not fl_bom:
        raise HTTPException(status_code=404, detail="Nomenclature de poste technique non trouvée")
    return fl_bom

@app.put("/functional-location-boms/{fl_bom_id}", response_model=FunctionalLocationBOM)
async def update_functional_location_bom_endpoint(fl_bom_id: str, fl_bom: FunctionalLocationBOM):
    """Met à jour une nomenclature de poste technique"""
    return await update_functional_location_bom(fl_bom_id, fl_bom)

@app.delete("/functional-location-boms/{fl_bom_id}")
async def delete_functional_location_bom_endpoint(fl_bom_id: str):
    """Supprime une nomenclature de poste technique"""
    success = await delete_functional_location_bom(fl_bom_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nomenclature de poste technique non trouvée")
    return {"message": "Nomenclature de poste technique supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR NOMENCLATURES D'ÉQUIPEMENTS
# ============================================================================

@app.post("/equipment-boms/", response_model=EquipmentBOM)
async def create_equipment_bom_endpoint(eq_bom: EquipmentBOM):
    """Crée une nouvelle nomenclature d'équipement"""
    return await create_equipment_bom(eq_bom)

@app.get("/equipment-boms/", response_model=List[EquipmentBOM])
async def get_all_equipment_boms_endpoint():
    """Récupère toutes les nomenclatures d'équipements"""
    return await get_all_equipment_boms()

@app.get("/equipment-boms/{eq_bom_id}", response_model=EquipmentBOM)
async def get_equipment_bom_endpoint(eq_bom_id: str):
    """Récupère une nomenclature d'équipement par ID"""
    eq_bom = await get_equipment_bom(eq_bom_id)
    if not eq_bom:
        raise HTTPException(status_code=404, detail="Nomenclature d'équipement non trouvée")
    return eq_bom

@app.put("/equipment-boms/{eq_bom_id}", response_model=EquipmentBOM)
async def update_equipment_bom_endpoint(eq_bom_id: str, eq_bom: EquipmentBOM):
    """Met à jour une nomenclature d'équipement"""
    return await update_equipment_bom(eq_bom_id, eq_bom)

@app.delete("/equipment-boms/{eq_bom_id}")
async def delete_equipment_bom_endpoint(eq_bom_id: str):
    """Supprime une nomenclature d'équipement"""
    success = await delete_equipment_bom(eq_bom_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nomenclature d'équipement non trouvée")
    return {"message": "Nomenclature d'équipement supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR GAMMES GÉNÉRALES
# ============================================================================

@app.post("/general-task-lists/", response_model=GeneralTaskList)
async def create_general_task_list_endpoint(gtl: GeneralTaskList):
    """Crée une nouvelle gamme générale"""
    return await create_general_task_list(gtl)

@app.get("/general-task-lists/", response_model=List[GeneralTaskList])
async def get_all_general_task_lists_endpoint():
    """Récupère toutes les gammes générales"""
    return await get_all_general_task_lists()

@app.get("/general-task-lists/{gtl_id}", response_model=GeneralTaskList)
async def get_general_task_list_endpoint(gtl_id: str):
    """Récupère une gamme générale par ID"""
    gtl = await get_general_task_list(gtl_id)
    if not gtl:
        raise HTTPException(status_code=404, detail="Gamme générale non trouvée")
    return gtl

@app.put("/general-task-lists/{gtl_id}", response_model=GeneralTaskList)
async def update_general_task_list_endpoint(gtl_id: str, gtl: GeneralTaskList):
    """Met à jour une gamme générale"""
    return await update_general_task_list(gtl_id, gtl)

@app.delete("/general-task-lists/{gtl_id}")
async def delete_general_task_list_endpoint(gtl_id: str):
    """Supprime une gamme générale"""
    success = await delete_general_task_list(gtl_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gamme générale non trouvée")
    return {"message": "Gamme générale supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR GAMMES POUR ÉQUIPEMENTS
# ============================================================================

@app.post("/equipment-task-lists/", response_model=EquipmentTaskList)
async def create_equipment_task_list_endpoint(etl: EquipmentTaskList):
    """Crée une nouvelle gamme pour équipement"""
    return await create_equipment_task_list(etl)

@app.get("/equipment-task-lists/", response_model=List[EquipmentTaskList])
async def get_all_equipment_task_lists_endpoint():
    """Récupère toutes les gammes pour équipements"""
    return await get_all_equipment_task_lists()

@app.get("/equipment-task-lists/{etl_id}", response_model=EquipmentTaskList)
async def get_equipment_task_list_endpoint(etl_id: str):
    """Récupère une gamme pour équipement par ID"""
    etl = await get_equipment_task_list(etl_id)
    if not etl:
        raise HTTPException(status_code=404, detail="Gamme pour équipement non trouvée")
    return etl

@app.put("/equipment-task-lists/{etl_id}", response_model=EquipmentTaskList)
async def update_equipment_task_list_endpoint(etl_id: str, etl: EquipmentTaskList):
    """Met à jour une gamme pour équipement"""
    return await update_equipment_task_list(etl_id, etl)

@app.delete("/equipment-task-lists/{etl_id}")
async def delete_equipment_task_list_endpoint(etl_id: str):
    """Supprime une gamme pour équipement"""
    success = await delete_equipment_task_list(etl_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gamme pour équipement non trouvée")
    return {"message": "Gamme pour équipement supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR GAMMES POUR POSTES TECHNIQUES
# ============================================================================

@app.post("/functional-location-task-lists/", response_model=FunctionalLocationTaskList)
async def create_functional_location_task_list_endpoint(fltl: FunctionalLocationTaskList):
    """Crée une nouvelle gamme pour poste technique"""
    return await create_functional_location_task_list(fltl)

@app.get("/functional-location-task-lists/", response_model=List[FunctionalLocationTaskList])
async def get_all_functional_location_task_lists_endpoint():
    """Récupère toutes les gammes pour postes techniques"""
    return await get_all_functional_location_task_lists()

@app.get("/functional-location-task-lists/{fltl_id}", response_model=FunctionalLocationTaskList)
async def get_functional_location_task_list_endpoint(fltl_id: str):
    """Récupère une gamme pour poste technique par ID"""
    fltl = await get_functional_location_task_list(fltl_id)
    if not fltl:
        raise HTTPException(status_code=404, detail="Gamme pour poste technique non trouvée")
    return fltl

@app.put("/functional-location-task-lists/{fltl_id}", response_model=FunctionalLocationTaskList)
async def update_functional_location_task_list_endpoint(fltl_id: str, fltl: FunctionalLocationTaskList):
    """Met à jour une gamme pour poste technique"""
    return await update_functional_location_task_list(fltl_id, fltl)

@app.delete("/functional-location-task-lists/{fltl_id}")
async def delete_functional_location_task_list_endpoint(fltl_id: str):
    """Supprime une gamme pour poste technique"""
    success = await delete_functional_location_task_list(fltl_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gamme pour poste technique non trouvée")
    return {"message": "Gamme pour poste technique supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR PLANS À CYCLE SIMPLE
# ============================================================================

@app.post("/single-cycle-plans/", response_model=SingleCyclePlan)
async def create_single_cycle_plan_endpoint(scp: SingleCyclePlan):
    """Crée un nouveau plan à cycle simple"""
    return await create_single_cycle_plan(scp)

@app.get("/single-cycle-plans/", response_model=List[SingleCyclePlan])
async def get_all_single_cycle_plans_endpoint():
    """Récupère tous les plans à cycle simple"""
    return await get_all_single_cycle_plans()

@app.get("/single-cycle-plans/{scp_id}", response_model=SingleCyclePlan)
async def get_single_cycle_plan_endpoint(scp_id: str):
    """Récupère un plan à cycle simple par ID"""
    scp = await get_single_cycle_plan(scp_id)
    if not scp:
        raise HTTPException(status_code=404, detail="Plan à cycle simple non trouvé")
    return scp

@app.put("/single-cycle-plans/{scp_id}", response_model=SingleCyclePlan)
async def update_single_cycle_plan_endpoint(scp_id: str, scp: SingleCyclePlan):
    """Met à jour un plan à cycle simple"""
    return await update_single_cycle_plan(scp_id, scp)

@app.delete("/single-cycle-plans/{scp_id}")
async def delete_single_cycle_plan_endpoint(scp_id: str):
    """Supprime un plan à cycle simple"""
    success = await delete_single_cycle_plan(scp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan à cycle simple non trouvé")
    return {"message": "Plan à cycle simple supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR PLANS DE MAINTENANCE STRATÉGIQUE
# ============================================================================

@app.post("/strategy-maintenance-plans/", response_model=StrategyMaintenancePlan)
async def create_strategy_maintenance_plan_endpoint(smp: StrategyMaintenancePlan):
    """Crée un nouveau plan de maintenance stratégique"""
    return await create_strategy_maintenance_plan(smp)

@app.get("/strategy-maintenance-plans/", response_model=List[StrategyMaintenancePlan])
async def get_all_strategy_maintenance_plans_endpoint():
    """Récupère tous les plans de maintenance stratégique"""
    return await get_all_strategy_maintenance_plans()

@app.get("/strategy-maintenance-plans/{smp_id}", response_model=StrategyMaintenancePlan)
async def get_strategy_maintenance_plan_endpoint(smp_id: str):
    """Récupère un plan de maintenance stratégique par ID"""
    smp = await get_strategy_maintenance_plan(smp_id)
    if not smp:
        raise HTTPException(status_code=404, detail="Plan de maintenance stratégique non trouvé")
    return smp

@app.put("/strategy-maintenance-plans/{smp_id}", response_model=StrategyMaintenancePlan)
async def update_strategy_maintenance_plan_endpoint(smp_id: str, smp: StrategyMaintenancePlan):
    """Met à jour un plan de maintenance stratégique"""
    return await update_strategy_maintenance_plan(smp_id, smp)

@app.delete("/strategy-maintenance-plans/{smp_id}")
async def delete_strategy_maintenance_plan_endpoint(smp_id: str):
    """Supprime un plan de maintenance stratégique"""
    success = await delete_strategy_maintenance_plan(smp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan de maintenance stratégique non trouvé")
    return {"message": "Plan de maintenance stratégique supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR PLANS À PLUSIEURS COMPTEURS
# ============================================================================

@app.post("/multiple-counter-plans/", response_model=MultipleCounterPlan)
async def create_multiple_counter_plan_endpoint(mcp: MultipleCounterPlan):
    """Crée un nouveau plan à plusieurs compteurs"""
    return await create_multiple_counter_plan(mcp)

@app.get("/multiple-counter-plans/", response_model=List[MultipleCounterPlan])
async def get_all_multiple_counter_plans_endpoint():
    """Récupère tous les plans à plusieurs compteurs"""
    return await get_all_multiple_counter_plans()

@app.get("/multiple-counter-plans/{mcp_id}", response_model=MultipleCounterPlan)
async def get_multiple_counter_plan_endpoint(mcp_id: str):
    """Récupère un plan à plusieurs compteurs par ID"""
    mcp = await get_multiple_counter_plan(mcp_id)
    if not mcp:
        raise HTTPException(status_code=404, detail="Plan à plusieurs compteurs non trouvé")
    return mcp

@app.put("/multiple-counter-plans/{mcp_id}", response_model=MultipleCounterPlan)
async def update_multiple_counter_plan_endpoint(mcp_id: str, mcp: MultipleCounterPlan):
    """Met à jour un plan à plusieurs compteurs"""
    return await update_multiple_counter_plan(mcp_id, mcp)

@app.delete("/multiple-counter-plans/{mcp_id}")
async def delete_multiple_counter_plan_endpoint(mcp_id: str):
    """Supprime un plan à plusieurs compteurs"""
    success = await delete_multiple_counter_plan(mcp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan à plusieurs compteurs non trouvé")
    return {"message": "Plan à plusieurs compteurs supprimé avec succès"}

# ============================================================================
# ENDPOINTS POUR VALEURS CARACTÉRISTIQUES
# ============================================================================

@app.post("/characteristic-values/", response_model=CharacteristicValues)
async def create_characteristic_values_endpoint(cv: CharacteristicValues):
    """Crée une nouvelle valeur caractéristique"""
    return await create_characteristic_values(cv)

@app.get("/characteristic-values/", response_model=List[CharacteristicValues])
async def get_all_characteristic_values_endpoint():
    """Récupère toutes les valeurs caractéristiques"""
    return await get_all_characteristic_values()

@app.get("/characteristic-values/{cv_id}", response_model=CharacteristicValues)
async def get_characteristic_values_endpoint(cv_id: str):
    """Récupère une valeur caractéristique par ID"""
    cv = await get_characteristic_values(cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="Valeur caractéristique non trouvée")
    return cv

@app.put("/characteristic-values/{cv_id}", response_model=CharacteristicValues)
async def update_characteristic_values_endpoint(cv_id: str, cv: CharacteristicValues):
    """Met à jour une valeur caractéristique"""
    return await update_characteristic_values(cv_id, cv)

@app.delete("/characteristic-values/{cv_id}")
async def delete_characteristic_values_endpoint(cv_id: str):
    """Supprime une valeur caractéristique"""
    success = await delete_characteristic_values(cv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Valeur caractéristique non trouvée")
    return {"message": "Valeur caractéristique supprimée avec succès"}

# ============================================================================
# ENDPOINTS POUR NOTIFICATIONS
# ============================================================================

@app.post("/notifications/", response_model=Notification)
async def create_notification_endpoint(notification: Notification):
    """Crée une nouvelle notification"""
    return await create_notification(notification)

@app.get("/notifications/", response_model=List[Notification])
async def get_all_notifications_endpoint():
    """Récupère toutes les notifications"""
    return await get_all_notifications()

@app.get("/notifications/{notification_id}", response_model=Notification)
async def get_notification_endpoint(notification_id: str):
    """Récupère une notification par ID"""
    notification = await get_notification(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notification

@app.put("/notifications/{notification_id}", response_model=Notification)
async def update_notification_endpoint(notification_id: str, notification: Notification):
    """Met à jour une notification"""
    return await update_notification(notification_id, notification)

@app.delete("/notifications/{notification_id}")
async def delete_notification_endpoint(notification_id: str):
    """Supprime une notification"""
    success = await delete_notification(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return {"message": "Notification supprimée avec succès"}

@app.get("/notifications/equipment/{equipment_id}", response_model=List[Notification])
async def get_notifications_by_equipment_endpoint(equipment_id: str):
    """Récupère toutes les notifications pour un équipement"""
    return await get_notifications_by_equipment(equipment_id)

@app.get("/notifications/status/{status}", response_model=List[Notification])
async def get_notifications_by_status_endpoint(status: str):
    """Récupère toutes les notifications par statut"""
    return await get_notifications_by_status(status)

@app.get("/notifications/priority/{priority}", response_model=List[Notification])
async def get_notifications_by_priority_endpoint(priority: str):
    """Récupère toutes les notifications par priorité"""
    return await get_notifications_by_priority(priority)

# ============================================================================
# ENDPOINTS POUR ORDRES
# ============================================================================

@app.post("/orders/", response_model=Order)
async def create_order_endpoint(order: Order):
    """Crée un nouvel ordre"""
    return await create_order(order)

@app.get("/orders/", response_model=List[Order])
async def get_all_orders_endpoint():
    """Récupère tous les ordres"""
    return await get_all_orders()

@app.get("/orders/{order_id}", response_model=Order)
async def get_order_endpoint(order_id: str):
    """Récupère un ordre par ID"""
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Ordre non trouvé")
    return order

@app.put("/orders/{order_id}", response_model=Order)
async def update_order_endpoint(order_id: str, order: Order):
    """Met à jour un ordre"""
    return await update_order(order_id, order)

@app.delete("/orders/{order_id}")
async def delete_order_endpoint(order_id: str):
    """Supprime un ordre"""
    success = await delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ordre non trouvé")
    return {"message": "Ordre supprimé avec succès"}

@app.get("/orders/equipment/{equipment_id}", response_model=List[Order])
async def get_orders_by_equipment_endpoint(equipment_id: str):
    """Récupère tous les ordres pour un équipement"""
    return await get_orders_by_equipment(equipment_id)

@app.get("/orders/status/{status}", response_model=List[Order])
async def get_orders_by_status_endpoint(status: str):
    """Récupère tous les ordres par statut"""
    return await get_orders_by_status(status)

@app.get("/orders/type/{order_type}", response_model=List[Order])
async def get_orders_by_type_endpoint(order_type: str):
    """Récupère tous les ordres par type"""
    return await get_orders_by_type(order_type)

@app.get("/orders/work-center/{work_center_id}", response_model=List[Order])
async def get_orders_by_work_center_endpoint(work_center_id: str):
    """Récupère tous les ordres pour un centre de travail"""
    return await get_orders_by_work_center(work_center_id)

# ============================================================================
# ENDPOINTS GÉNÉRAUX
# ============================================================================

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "SAP PM Simulator API",
        "version": "1.0.0",
        "database": "RAGENNT4SAP",
        "status": "running"
    }

@app.get("/all-data")
async def get_all_data():
    """Récupère toutes les données de la base"""
    from database import get_all_data
    return await get_all_data()

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "database": "RAGENNT4SAP",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 