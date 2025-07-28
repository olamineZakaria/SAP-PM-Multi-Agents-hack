# 🤖 Agent de Maintenance Intelligente avec MCP + ChatGPT-4

Un agent conversationnel intelligent combinant **MCP (Model Context Protocol)** et **ChatGPT-4** pour la gestion de maintenance industrielle via une interface web moderne.

## 🚀 **Fonctionnalités**

- **🤖 ChatGPT-4 Intégré** : Conversation naturelle et explications détaillées
- **📊 Serveur MCP** : Requêtes techniques précises vers l'API SAP PM
- **🏭 API SAP PM** : Accès complet aux données de maintenance industrielle
- **💬 Interface Chat Hybride** : Détection automatique du type de demande
- **📊 Formatage Intelligent** : Réponses formatées en tableaux et listes
- **🔄 Historique** : Conservation du contexte de conversation
- **⚡ Temps Réel** : Réponses instantanées

## 🏗️ **Architecture Hybride**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   Application   │    │   Serveur       │    │   Serveur       │
│   Web Flask     │◄──►│   Hybride       │◄──►│   MCP           │◄──►│   SAP PM API    │
│   (Port 5000)   │    │   ChatGPT-4     │    │   (Port 8001)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **🎯 Logique de Routage**

- **Demandes Techniques** → MCP → SAP PM API
- **Conversations Générales** → ChatGPT-4 (réponse directe)

## 📋 **Prérequis**

- Python 3.8+
- Clé API OpenAI (ChatGPT-4)
- Serveur MCP (inclus dans le projet)
- Serveur SAP PM (inclus dans le projet)

## 🔧 **Installation**

### 1. **Cloner le projet**
```bash
git clone <repository-url>
cd "Teal hack"
```

### 2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 3. **Configuration**
Créez un fichier `.env` basé sur `env_example.txt` :
```bash
cp env_example.txt .env
```

Éditez le fichier `.env` et ajoutez votre clé API OpenAI :
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
MCP_SERVER_URL=http://localhost:8001
SAP_PM_URL=http://localhost:8000
```

### 4. **Démarrer l'application**
```bash
python start_app.py
```

## 🎯 **Utilisation**

### **Démarrage Automatique**
```bash
python start_app.py
```
Le script va :
- ✅ Vérifier la configuration OpenAI
- ✅ Démarrer le serveur SAP PM
- ✅ Démarrer le serveur MCP
- ✅ Lancer l'application Flask
- ✅ Ouvrir l'interface sur http://localhost:5000

### **Démarrage Manuel**
```bash
# Terminal 1 - Serveur SAP PM
cd "SAP PM"
python main.py

# Terminal 2 - Serveur MCP
python main_mcp.py

# Terminal 3 - Application Flask
python app.py
```

## 💬 **Exemples d'Utilisation**

### **Conversations Générales (ChatGPT-4)**
- "Salut, comment ça va ?"
- "Explique-moi la maintenance préventive"
- "Quels sont les avantages de la maintenance prédictive ?"
- "Comment fonctionne un système de maintenance ?"

### **Demandes Techniques (MCP)**
- "Donne-moi tous les équipements dans un tableau"
- "Montre-moi les ordres de maintenance ouverts"
- "Liste toutes les notifications"
- "Crée une notification de maintenance pour l'équipement EQ-001"

### **Conversation Mixte**
- "Salut ! Peux-tu me donner un aperçu de l'état de nos équipements ?"
- "J'ai besoin de créer un ordre de maintenance urgent"
- "Quels sont les équipements qui nécessitent une attention immédiate ?"

## 🔍 **APIs Disponibles**

### **Endpoints MCP**
- `POST /ask` - Questions en langage naturel
- `POST /session` - Gestion des sessions
- `GET /health` - État du serveur MCP

### **Endpoints SAP PM**
- `GET /equipments` - Liste des équipements
- `GET /orders` - Ordres de maintenance
- `GET /notifications` - Notifications
- `GET /work-centers` - Centres de travail
- `GET /functional-locations` - Emplacements fonctionnels
- `GET /materials` - Matériaux
- `POST /notifications` - Créer une notification
- `POST /orders` - Créer un ordre

### **Endpoints Flask**
- `GET /` - Interface web
- `POST /api/chat` - Chat hybride
- `GET /api/health` - État du système
- `GET /api/examples` - Exemples de questions

## 🛠️ **Configuration Avancée**

### **Variables d'Environnement**
```env
# OpenAI (OBLIGATOIRE)
OPENAI_API_KEY=your-openai-api-key

# MCP Server
MCP_SERVER_URL=http://localhost:8001
MCP_HOST=0.0.0.0
MCP_PORT=8001

# SAP PM
SAP_PM_URL=http://localhost:8000
SAP_PM_HOST=0.0.0.0
SAP_PM_PORT=8000

# Flask
FLASK_SECRET_KEY=your-secret-key
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Debug
DEBUG=True
```

### **Personnalisation du Routage**
Modifiez les mots-clés techniques dans `app.py` :
```python
technical_keywords = [
    "équipement", "equipment", "équipements", "ordre", "order", "notification", 
    "maintenance", "centre de travail", "work center", "matériau", "material",
    "donne-moi", "montre-moi", "liste", "récupérer", "obtenir"
]
```

## 🔧 **Dépannage**

### **Erreur OpenAI**
```
❌ OPENAI_API_KEY non configurée
```
**Solution** : Ajoutez votre clé API dans le fichier `.env`

### **Serveur MCP Inaccessible**
```
❌ Serveur MCP non accessible
```
**Solution** : Vérifiez que le serveur MCP est démarré sur le port 8001

### **Serveur SAP PM Inaccessible**
```
❌ Serveur SAP PM non accessible
```
**Solution** : Vérifiez que le serveur SAP PM est démarré sur le port 8000

### **Erreur de Connexion**
```
❌ Erreur de connexion au serveur MCP/SAP PM
```
**Solution** : Vérifiez que tous les serveurs sont en cours d'exécution

## 📊 **Monitoring**

### **Vérification de l'État**
```bash
curl http://localhost:5000/api/health
```

### **Logs**
- **Flask** : Logs dans la console
- **MCP** : Logs dans le terminal du serveur MCP
- **SAP PM** : Logs dans le terminal du serveur SAP PM
- **ChatGPT-4** : Réponses dans l'interface web

## 🚀 **Développement**

### **Structure du Projet**
```
Teal hack/
├── app.py                 # Application Flask hybride
├── main_mcp.py           # Serveur MCP
├── start_app.py          # Script de démarrage
├── requirements.txt      # Dépendances Python
├── env_example.txt      # Exemple de configuration
├── templates/           # Templates HTML
│   └── index.html      # Interface web
└── SAP PM/             # Serveur SAP PM
    ├── main.py         # API SAP PM
    └── database.py     # Base de données
```

### **Ajout de Nouvelles Fonctionnalités**
1. **Nouvelle API SAP PM** : Ajoutez l'endpoint dans `SAP PM/main.py`
2. **Nouveau Formatage** : Modifiez les méthodes `_format_*` dans `app.py`
3. **Nouveau Contexte** : Mettez à jour `get_context_for_gpt()` dans `app.py`
4. **Nouveaux Mots-clés** : Ajoutez des mots-clés techniques dans `process_user_request()`

## 🤝 **Contribution**

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 **Licence**

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 **Support**

Pour toute question ou problème :
1. Vérifiez la section **Dépannage**
2. Consultez les logs de l'application
3. Vérifiez la configuration dans `.env`
4. Ouvrez une issue sur GitHub

---

**🎉 Prêt à utiliser votre Agent de Maintenance Intelligente avec MCP + ChatGPT-4 !** 