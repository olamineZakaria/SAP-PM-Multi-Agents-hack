# Simulateur SAP PM (Plant Maintenance)

Un simulateur complet du module SAP Plant Maintenance (PM) développé avec FastAPI et Python. Ce projet reproduit les fonctionnalités de base de SAP PM pour la gestion de la maintenance des équipements et installations industrielles.

## 🚀 Fonctionnalités

### Données de Base (Master Data) SAP PM
Le simulateur inclut les 24 données de base principales de SAP PM :

1. **Catalog** - Catalogue de codes et textes
2. **Permit** - Permis de travail
3. **Characteristic** - Caractéristiques techniques
4. **Class** - Classes d'équipements
5. **MaintenanceStrategy** - Stratégies de maintenance
6. **CycleSet** - Ensembles de cycles
7. **WorkCenterHierarchy** - Hiérarchies des centres de travail
8. **WorkCenter** - Centres de travail
9. **Material** - Matériels et pièces
10. **BillOfMaterial** - Nomenclatures
11. **FunctionalLocation** - Postes techniques
12. **Equipment** - Équipements
13. **MeasuringPoint** - Points de mesure
14. **Counter** - Compteurs
15. **SerialNumber** - Numéros de série
16. **FunctionalLocationBOM** - Nomenclatures de postes techniques
17. **EquipmentBOM** - Nomenclatures d'équipements
18. **GeneralTaskList** - Gammes générales
19. **EquipmentTaskList** - Gammes pour équipements
20. **FunctionalLocationTaskList** - Gammes pour postes techniques
21. **SingleCyclePlan** - Plans à cycle simple
22. **StrategyMaintenancePlan** - Plans de maintenance stratégique
23. **MultipleCounterPlan** - Plans à plusieurs compteurs
24. **CharacteristicValues** - Valeurs caractéristiques

### API RESTful Complète
- **CRUD Operations** : Création, Lecture, Mise à jour, Suppression pour chaque entité
- **Validation des Dépendances** : Vérification automatique des relations entre entités
- **Documentation Interactive** : Interface Swagger/OpenAPI intégrée
- **Gestion d'Erreurs** : Messages d'erreur détaillés et codes HTTP appropriés

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🛠️ Installation

1. **Cloner ou télécharger le projet**
   ```bash
   # Si vous avez git
   git clone <url-du-repo>
   cd simulateur-sap-pm
   
   # Ou téléchargez et extrayez le projet
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   
   # Sur Windows
   venv\Scripts\activate
   
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Démarrage

### Lancer le serveur de développement
```bash
# Méthode 1 : Directement avec Python
python main.py

# Méthode 2 : Avec uvicorn (recommandé pour le développement)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Méthode 3 : Avec uvicorn en mode production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Accéder à l'application
- **API Documentation** : http://localhost:8000/docs
- **ReDoc Documentation** : http://localhost:8000/redoc
- **API Racine** : http://localhost:8000/

## 📚 Utilisation

### 1. Documentation Interactive
Accédez à http://localhost:8000/docs pour utiliser l'interface Swagger qui permet de :
- Tester tous les endpoints directement
- Voir les modèles de données
- Comprendre les paramètres requis

### 2. Exemples d'Utilisation

#### Créer une caractéristique
```bash
curl -X POST "http://localhost:8000/characteristics" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "CHAR001",
       "name": "Puissance",
       "description": "Puissance en CV",
       "unit_of_measurement": "KILOGRAMS"
     }'
```

#### Créer un équipement
```bash
curl -X POST "http://localhost:8000/equipment" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "EQ001",
       "name": "Pompe Centrifuge",
       "description": "Pompe principale du circuit de refroidissement",
       "functional_location_id": "FL001",
       "cost_center": "CC001",
       "characteristics": ["CHAR001"],
       "permits": []
     }'
```

#### Récupérer tous les équipements
```bash
curl -X GET "http://localhost:8000/equipment"
```

### 3. Ordre de Création Recommandé
Pour respecter les dépendances SAP PM, créez les entités dans cet ordre :

1. **Données de base sans dépendances** :
   - Catalog, Permit, Characteristic, MaintenanceStrategy, CycleSet
   - WorkCenterHierarchy, Material

2. **Données avec dépendances simples** :
   - Class (dépend de Characteristic)
   - WorkCenter (dépend de WorkCenterHierarchy)
   - BillOfMaterial (dépend de Material)

3. **Données techniques principales** :
   - FunctionalLocation (dépend de WorkCenter, Class, Characteristic, Permit)
   - Equipment (dépend de FunctionalLocation, WorkCenter, Class, Characteristic, Permit)

4. **Données de mesure et suivi** :
   - MeasuringPoint, Counter (dépendent de Equipment/FunctionalLocation, Characteristic)
   - SerialNumber (dépend de Material, Equipment)

5. **Nomenclatures spécialisées** :
   - FunctionalLocationBOM, EquipmentBOM (dépendent de FunctionalLocation/Equipment, Material)

6. **Gammes de maintenance** :
   - GeneralTaskList, EquipmentTaskList, FunctionalLocationTaskList
   - (dépendent de WorkCenter, MaintenanceStrategy, Material, Equipment/FunctionalLocation)

7. **Plans de maintenance** :
   - SingleCyclePlan, StrategyMaintenancePlan, MultipleCounterPlan
   - (dépendent des gammes, équipements, compteurs, stratégies)

8. **Valeurs caractéristiques** :
   - CharacteristicValues (dépend de Class, Characteristic, objets maîtres)

## 🏗️ Architecture du Projet

```
simulateur-sap-pm/
├── main.py              # Application FastAPI principale
├── schemas.py           # Modèles Pydantic pour la validation
├── crud.py             # Fonctions de logique métier et CRUD
├── database.py         # Base de données en mémoire et initialisation
├── requirements.txt    # Dépendances Python
└── README.md          # Documentation
```

### Structure des Fichiers

#### `main.py`
- Application FastAPI avec tous les endpoints REST
- Configuration CORS et documentation
- Gestion des erreurs HTTP

#### `schemas.py`
- Modèles Pydantic pour les 24 entités SAP PM
- Validation automatique des données
- Enums pour les types d'activité et unités de mesure

#### `crud.py`
- Fonctions CRUD pour chaque entité
- Validation des dépendances entre entités
- Gestion des erreurs métier

#### `database.py`
- Base de données en mémoire (dictionnaires Python)
- Données d'exemple pour le démarrage
- Fonctions utilitaires

## 🔧 Configuration

### Variables d'Environnement
Le simulateur utilise des valeurs par défaut, mais vous pouvez configurer :

```bash
# Port du serveur (défaut: 8000)
export PORT=8080

# Host (défaut: 0.0.0.0)
export HOST=127.0.0.1
```

### Personnalisation
- Modifiez `database.py` pour ajouter vos propres données d'exemple
- Ajustez les validations dans `crud.py` selon vos besoins métier
- Étendez les modèles dans `schemas.py` pour ajouter de nouveaux champs

## 🧪 Tests

### Test Manuel avec curl
```bash
# Test de l'endpoint racine
curl http://localhost:8000/

# Test de récupération de toutes les données
curl http://localhost:8000/all-data

# Test de création d'une caractéristique
curl -X POST "http://localhost:8000/characteristics" \
     -H "Content-Type: application/json" \
     -d '{"id":"TEST001","name":"Test","description":"Test"}'
```

### Test avec l'Interface Web
1. Ouvrez http://localhost:8000/docs
2. Cliquez sur un endpoint
3. Cliquez sur "Try it out"
4. Remplissez les paramètres
5. Cliquez sur "Execute"

## 🐛 Dépannage

### Problèmes Courants

#### Port déjà utilisé
```bash
# Changer le port
uvicorn main:app --port 8080
```

#### Erreur de dépendances
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

#### Erreur de validation
- Vérifiez que les IDs référencés existent
- Respectez l'ordre de création recommandé
- Consultez les messages d'erreur détaillés dans l'API

### Logs et Debug
```bash
# Mode debug avec logs détaillés
uvicorn main:app --reload --log-level debug
```

## 📖 API Reference

### Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations sur l'API |
| GET | `/all-data` | Toutes les données SAP PM |
| GET | `/docs` | Documentation interactive |

### Endpoints par Entité
Chaque entité a 5 endpoints :
- `POST /{entity}` - Créer
- `GET /{entity}/{id}` - Lire par ID
- `GET /{entity}` - Lire tous
- `PUT /{entity}/{id}` - Mettre à jour
- `DELETE /{entity}/{id}` - Supprimer

### Codes de Réponse
- `200` - Succès
- `201` - Créé avec succès
- `400` - Erreur de validation
- `404` - Ressource non trouvée
- `422` - Erreur de validation des données

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 🆘 Support

Pour toute question ou problème :
1. Consultez la documentation interactive à `/docs`
2. Vérifiez les logs du serveur
3. Testez avec l'interface Swagger

---

**Note** : Ce simulateur reproduit les concepts de SAP PM mais n'est pas un produit SAP officiel. Il est destiné à l'apprentissage et à la démonstration des concepts de maintenance industrielle. 