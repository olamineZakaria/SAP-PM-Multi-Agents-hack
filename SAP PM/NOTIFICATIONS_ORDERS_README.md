# Endpoints Notifications et Ordres - SAP PM API

## Vue d'ensemble

Ce document décrit les nouveaux endpoints ajoutés à l'API SAP PM pour gérer les **notifications** et les **ordres** de maintenance.

## Notifications

### Modèle de données

```python
class Notification:
    id: str                    # Identifiant unique
    title: str                 # Titre de la notification
    description: str           # Description détaillée
    status: NotificationStatus # CREATED, IN_PROGRESS, COMPLETED, CANCELLED
    priority: NotificationPriority # LOW, MEDIUM, HIGH, CRITICAL
    notification_type: NotificationType # BREAKDOWN, PREVENTIVE, INSPECTION, CALIBRATION, SAFETY, QUALITY
    created_date: datetime     # Date de création
    created_by: str           # Utilisateur créateur
    equipment_id: Optional[str] # ID de l'équipement concerné
    functional_location_id: Optional[str] # ID du poste technique
    work_center_id: Optional[str] # ID du centre de travail
    assigned_to: Optional[str] # Utilisateur assigné
    estimated_duration: Optional[float] # Durée estimée en heures
    actual_duration: Optional[float] # Durée réelle en heures
    completion_date: Optional[datetime] # Date de completion
    related_orders: List[str] # IDs des ordres liés
```

### Endpoints disponibles

#### 1. Créer une notification
```http
POST /notifications/
```

#### 2. Récupérer toutes les notifications
```http
GET /notifications/
```

#### 3. Récupérer une notification par ID
```http
GET /notifications/{notification_id}
```

#### 4. Mettre à jour une notification
```http
PUT /notifications/{notification_id}
```

#### 5. Supprimer une notification
```http
DELETE /notifications/{notification_id}
```

#### 6. Récupérer les notifications par équipement
```http
GET /notifications/equipment/{equipment_id}
```

#### 7. Récupérer les notifications par statut
```http
GET /notifications/status/{status}
```

#### 8. Récupérer les notifications par priorité
```http
GET /notifications/priority/{priority}
```

### Exemple d'utilisation

```python
import httpx

# Créer une nouvelle notification
notification_data = {
    "title": "Panne moteur pompe P-001",
    "description": "Le moteur présente des vibrations anormales",
    "status": "CREATED",
    "priority": "HIGH",
    "notification_type": "BREAKDOWN",
    "created_date": "2024-01-15T10:30:00Z",
    "created_by": "OPERATEUR_001",
    "equipment_id": "EQ-001",
    "work_center_id": "WC-001",
    "assigned_to": "TECHNICIEN_001",
    "estimated_duration": 4.0
}

async with httpx.AsyncClient() as client:
    response = await client.post("http://localhost:8000/notifications/", json=notification_data)
    notification = response.json()
    print(f"Notification créée: {notification['id']}")
```

## Ordres

### Modèle de données

```python
class Order:
    id: str                    # Identifiant unique
    order_number: str          # Numéro d'ordre
    title: str                 # Titre de l'ordre
    description: str           # Description détaillée
    status: OrderStatus        # CREATED, RELEASED, IN_PROGRESS, COMPLETED, CANCELLED
    order_type: OrderType      # PREVENTIVE, CORRECTIVE, INSPECTION, CALIBRATION, EMERGENCY
    created_date: datetime     # Date de création
    created_by: str           # Utilisateur créateur
    equipment_id: Optional[str] # ID de l'équipement concerné
    functional_location_id: Optional[str] # ID du poste technique
    work_center_id: Optional[str] # ID du centre de travail
    assigned_to: Optional[str] # Utilisateur assigné
    planned_start_date: Optional[datetime] # Date de début planifiée
    planned_end_date: Optional[datetime] # Date de fin planifiée
    actual_start_date: Optional[datetime] # Date de début réelle
    actual_end_date: Optional[datetime] # Date de fin réelle
    estimated_duration: Optional[float] # Durée estimée en heures
    actual_duration: Optional[float] # Durée réelle en heures
    priority: NotificationPriority # Priorité
    cost_center: str          # Centre de coûts
    materials_required: List[str] # IDs des matériaux requis
    related_notifications: List[str] # IDs des notifications liées
    task_list_id: Optional[str] # ID de la gamme associée
```

### Endpoints disponibles

#### 1. Créer un ordre
```http
POST /orders/
```

#### 2. Récupérer tous les ordres
```http
GET /orders/
```

#### 3. Récupérer un ordre par ID
```http
GET /orders/{order_id}
```

#### 4. Mettre à jour un ordre
```http
PUT /orders/{order_id}
```

#### 5. Supprimer un ordre
```http
DELETE /orders/{order_id}
```

#### 6. Récupérer les ordres par équipement
```http
GET /orders/equipment/{equipment_id}
```

#### 7. Récupérer les ordres par statut
```http
GET /orders/status/{status}
```

#### 8. Récupérer les ordres par type
```http
GET /orders/type/{order_type}
```

#### 9. Récupérer les ordres par centre de travail
```http
GET /orders/work-center/{work_center_id}
```

### Exemple d'utilisation

```python
import httpx
from datetime import datetime, timedelta

# Créer un nouvel ordre
order_data = {
    "order_number": "WO-2024-001",
    "title": "Réparation moteur pompe P-001",
    "description": "Réparation complète du moteur suite à la panne",
    "status": "CREATED",
    "order_type": "CORRECTIVE",
    "created_date": datetime.now().isoformat(),
    "created_by": "TECHNICIEN_001",
    "equipment_id": "EQ-001",
    "work_center_id": "WC-001",
    "assigned_to": "TECHNICIEN_001",
    "planned_start_date": (datetime.now() + timedelta(hours=1)).isoformat(),
    "planned_end_date": (datetime.now() + timedelta(hours=5)).isoformat(),
    "estimated_duration": 4.0,
    "priority": "HIGH",
    "cost_center": "CC-MAINT-001",
    "materials_required": ["MAT-001", "MAT-002"],
    "related_notifications": ["NOTIF-001"]
}

async with httpx.AsyncClient() as client:
    response = await client.post("http://localhost:8000/orders/", json=order_data)
    order = response.json()
    print(f"Ordre créé: {order['id']}")
```

## Tests

### Exécuter les tests

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API
python main.py

# Dans un autre terminal, exécuter les tests
python test_notifications_orders.py
```

### Données de test

L'API inclut des données de test pour les notifications et les ordres :

- **4 notifications** avec différents statuts et priorités
- **4 ordres** avec différents types et statuts
- Relations entre notifications et ordres

## Statuts et types

### Statuts de notification
- `CREATED` : Créée
- `IN_PROGRESS` : En cours
- `COMPLETED` : Terminée
- `CANCELLED` : Annulée

### Priorités
- `LOW` : Basse
- `MEDIUM` : Moyenne
- `HIGH` : Haute
- `CRITICAL` : Critique

### Types de notification
- `BREAKDOWN` : Panne
- `PREVENTIVE` : Préventive
- `INSPECTION` : Inspection
- `CALIBRATION` : Calibration
- `SAFETY` : Sécurité
- `QUALITY` : Qualité

### Statuts d'ordre
- `CREATED` : Créé
- `RELEASED` : Libéré
- `IN_PROGRESS` : En cours
- `COMPLETED` : Terminé
- `CANCELLED` : Annulé

### Types d'ordre
- `PREVENTIVE` : Préventif
- `CORRECTIVE` : Correctif
- `INSPECTION` : Inspection
- `CALIBRATION` : Calibration
- `EMERGENCY` : Urgence

## Intégration avec l'API existante

Les nouveaux endpoints s'intègrent parfaitement avec l'API existante :

- Utilisent les mêmes modèles de données (équipements, postes techniques, centres de travail)
- Respectent la même structure de réponse
- Incluent la gestion d'erreurs standard
- Supportent les opérations CRUD complètes

## Base de données

Les collections MongoDB créées :
- `notifications` : Stockage des notifications
- `orders` : Stockage des ordres

Les données sont automatiquement initialisées au démarrage de l'API avec des exemples réalistes. 