#!/usr/bin/env python3
"""
Application Flask - Agent Conversationnel Intelligent avec MCP + ChatGPT-4
Intégration hybride : MCP pour les requêtes techniques + ChatGPT-4 pour l'interaction
"""

from flask import Flask, render_template, request, jsonify, session
import requests
import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'teal-hack-secret-key-2024')

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8001')
SAP_PM_URL = os.getenv('SAP_PM_URL', 'http://localhost:8000')

# Initialiser le client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

class HybridMaintenanceAgent:
    """Agent hybride combinant MCP et ChatGPT-4"""
    
    def __init__(self):
        self.conversation_history = []
        self.session_id = None
        self.mcp_session_id = None
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'mcp_requests': 0,
            'gpt_requests': 0,
            'avg_response_time': 0,
            'last_activity': None
        }
    
    def create_mcp_session(self):
        """Crée une session MCP"""
        try:
            response = requests.post(f"{MCP_SERVER_URL}/session", 
                                  json={"user_id": "flask_app"})
            if response.status_code == 200:
                data = response.json()
                self.mcp_session_id = data.get('session_id')
                return True, data
            else:
                return False, {"error": "Impossible de créer la session MCP"}
        except Exception as e:
            return False, {"error": f"Erreur de connexion MCP: {str(e)}"}
    
    def ask_mcp(self, query):
        """Pose une question au serveur MCP"""
        if not self.mcp_session_id:
            success, session_data = self.create_mcp_session()
            if not success:
                return {"error": "Impossible de créer une session MCP"}
        
        try:
            payload = {
                "query": query,
                "session_id": self.mcp_session_id
            }
            
            response = requests.post(f"{MCP_SERVER_URL}/ask", 
                                  json=payload,
                                  timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Erreur API MCP: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Erreur de connexion au serveur MCP: {str(e)}"}
        except Exception as e:
            return {"error": f"Erreur inattendue: {str(e)}"}
    
    def get_context_for_gpt(self):
        """Prépare le contexte pour ChatGPT avec les données MCP"""
        context = """
Tu es un assistant conversationnel intelligent spécialisé dans la gestion de maintenance industrielle.
Tu interagis avec un utilisateur et tu peux utiliser un serveur MCP (Model Context Protocol) pour obtenir des données techniques.

TON RÔLE:
1. Comprendre les demandes de l'utilisateur en français
2. Détecter si la demande nécessite des données techniques
3. Si oui, demander au serveur MCP de récupérer les données
4. Formater et présenter les résultats de manière claire et professionnelle

EXEMPLES DE DEMANDES TECHNIQUES:
- "Donne-moi tous les équipements" → Demande des données via MCP
- "Montre-moi les ordres de maintenance" → Demande des données via MCP
- "Liste les notifications" → Demande des données via MCP

EXEMPLES DE CONVERSATION GÉNÉRALE:
- "Salut, comment ça va ?" → Réponse conversationnelle directe
- "Explique-moi la maintenance préventive" → Explication sans données
- "Quels sont les avantages de la maintenance prédictive ?" → Explication

FORMAT DE RÉPONSE:
- Utilise des emojis et du markdown pour formater
- Sois précis et professionnel
- Si tu as besoin de données techniques, indique-le clairement

HISTORIQUE DE CONVERSATION:
"""
        # Ajouter l'historique récent
        for entry in self.conversation_history[-5:]:  # Derniers 5 échanges
            context += f"Utilisateur: {entry['user']}\nAssistant: {entry['assistant']}\n\n"
        
        return context
    
    def process_user_request(self, user_message):
        """Traite la demande utilisateur avec ChatGPT-4 et MCP"""
        start_time = datetime.now()
        
        try:
            # Détecter si c'est une demande technique
            technical_keywords = [
                "équipement", "equipment", "équipements", "ordre", "order", "notification", 
                "maintenance", "centre de travail", "work center", "matériau", "material",
                "donne-moi", "montre-moi", "liste", "récupérer", "obtenir", "fournir", "tableau"
            ]
            
            is_technical_request = any(keyword in user_message.lower() for keyword in technical_keywords)
            
            if is_technical_request:
                # ÉTAPE 1: Demander les données via MCP
                mcp_response = self.ask_mcp(user_message)
                
                if mcp_response.get("success"):
                    # ÉTAPE 2: Préparer le contexte pour GPT avec les données MCP
                    context = self.get_context_for_gpt_with_data(mcp_response, user_message)
                    
                    # ÉTAPE 3: Demander à ChatGPT-4 d'organiser les données
                    system_message = f"""
Tu es un assistant spécialisé dans l'organisation et la présentation de données techniques de maintenance industrielle.

TON RÔLE:
1. Analyser les données brutes reçues du serveur MCP
2. Les organiser et les présenter de manière claire et professionnelle
3. Créer des tableaux, listes ou résumés selon la demande de l'utilisateur
4. Utiliser des emojis et du markdown pour améliorer la présentation

DONNÉES BRUTES RECUES:
{context}

DEMANDE UTILISATEUR: {user_message}

INSTRUCTIONS DE FORMATAGE MARKDOWN:
- Utilise des titres avec ## pour les sections principales
- Crée des tableaux avec | pour séparer les colonnes
- Utilise des listes à puces avec - pour les points
- Ajoute des emojis appropriés au début des sections
- Utilise **texte** pour le gras et *texte* pour l'italique
- Crée des blocs de code avec ``` pour les données techniques
- Utilise des badges avec des couleurs pour les statuts

EXEMPLES DE FORMATAGE:
```markdown
## 🏭 Liste des Équipements

Voici la liste complète des équipements disponibles :

| ID | Nom | Description | Asset ID | Centre de Coût |
|----|-----|-------------|----------|----------------|
| EQ-001 | Pompe Centrifuge | Pompe principale... | ASSET001 | CC001 |

📊 **Résumé :**
- **Total d'équipements :** 5
- **Centres de coût actifs :** CC001, CC002
- **Types d'équipements :** Pompes, Moteurs

✅ Données récupérées avec succès via le serveur MCP.
```

FORMAT DE RÉPONSE ATTENDU:
1. **Titre principal** avec emoji
2. **Introduction** courte et claire
3. **Tableau** bien formaté si applicable
4. **Résumé** avec points clés
5. **Confirmation** de la source des données

IMPORTANT:
- Sois précis et professionnel
- Utilise des emojis appropriés
- Formate les tableaux correctement
- Ajoute des informations contextuelles utiles
- Si les données sont vides, indique-le clairement
- Respecte la demande spécifique de l'utilisateur
"""

                    # Appeler ChatGPT-4 pour organiser les données
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": f"Organise ces données selon ma demande: {user_message}"}
                        ],
                        max_tokens=2000,
                        temperature=0.7
                    )
                    
                    final_response = response.choices[0].message.content
                    self.stats['mcp_requests'] += 1
                    
                else:
                    # En cas d'erreur MCP, utiliser ChatGPT-4 pour expliquer l'erreur
                    error_context = f"""
L'utilisateur a demandé: {user_message}
Mais le serveur MCP a retourné une erreur: {mcp_response.get('error', 'Erreur inconnue')}

Explique poliment l'erreur et suggère des alternatives.
"""
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Tu es un assistant de maintenance. Explique les erreurs de manière claire et suggère des solutions."},
                            {"role": "user", "content": error_context}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )
                    
                    final_response = response.choices[0].message.content
                    
            else:
                # ÉTAPE 1: Demande conversationnelle directe à ChatGPT-4
                context = self.get_context_for_gpt()
                
                system_message = f"""
{context}

Tu es un assistant conversationnel intelligent spécialisé dans la gestion de maintenance industrielle.
Réponds de manière naturelle et utile aux questions générales.
Utilise des emojis et du markdown pour améliorer la présentation.
"""

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": f"Question utilisateur: {user_message}"}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                
                final_response = response.choices[0].message.content
                self.stats['gpt_requests'] += 1
            
            # Calculer le temps de réponse
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Mettre à jour les statistiques
            self.stats['total_requests'] += 1
            self.stats['successful_requests'] += 1
            self.stats['last_activity'] = datetime.now().isoformat()
            
            # Calculer le temps de réponse moyen
            if self.stats['total_requests'] > 1:
                self.stats['avg_response_time'] = (
                    (self.stats['avg_response_time'] * (self.stats['total_requests'] - 1) + response_time) 
                    / self.stats['total_requests']
                )
            else:
                self.stats['avg_response_time'] = response_time
            
            # Ajouter à l'historique
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_message,
                "assistant": final_response,
                "is_technical": is_technical_request,
                "response_time": response_time
            })
            
            return {
                "success": True,
                "message": final_response,
                "is_technical_request": is_technical_request,
                "mcp_used": is_technical_request,
                "response_time": response_time,
                "agents_used": ["MCP", "ChatGPT-4"] if is_technical_request else ["ChatGPT-4"]
            }
            
        except Exception as e:
            self.stats['total_requests'] += 1
            return {
                "success": False,
                "error": f"Erreur lors du traitement: {str(e)}"
            }
    
    def format_mcp_response(self, mcp_data):
        """Formate la réponse MCP de manière lisible"""
        if not mcp_data.get("success"):
            return f"❌ **Erreur MCP**: {mcp_data.get('error', 'Erreur inconnue')}"
        
        intent = mcp_data.get("intent", "unknown")
        response_data = mcp_data.get("response", {})
        result = response_data.get("result", {})
        
        # Formatage selon l'intention
        if intent == "get_equipment_list":
            return self._format_equipment_list(result)
        elif intent == "get_open_orders":
            return self._format_orders_list(result)
        elif intent == "get_notifications":
            return self._format_notifications_list(result)
        elif intent == "create_notification":
            return self._format_creation_response(result, "notification")
        elif intent == "create_order":
            return self._format_creation_response(result, "ordre")
        elif intent == "get_equipment_by_id":
            return self._format_equipment_details(result)
        elif intent == "get_work_centers":
            return self._format_work_centers_list(result)
        elif intent == "get_functional_locations":
            return self._format_functional_locations_list(result)
        elif intent == "get_materials":
            return self._format_materials_list(result)
        else:
            return self._format_generic_response(mcp_data)
    
    def _format_equipment_list(self, result):
        """Formate la liste des équipements"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucun équipement trouvé**"
        
        formatted = "🏭 **Liste des Équipements**\n\n"
        formatted += "| ID | Nom | Description | Asset ID | Centre de Coût |\n"
        formatted += "|----|-----|-------------|----------|----------------|\n"
        
        for equipment in data:
            name = equipment.get('name', 'N/A')
            description = equipment.get('description', 'N/A')
            desc_short = description[:40] + "..." if len(description) > 40 else description
            
            formatted += f"| {equipment.get('id', 'N/A')} | {name} | {desc_short} | {equipment.get('asset_id', 'N/A')} | {equipment.get('cost_center', 'N/A')} |\n"
        
        return formatted
    
    def _format_orders_list(self, result):
        """Formate la liste des ordres"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucun ordre trouvé**"
        
        formatted = "🔧 **Liste des Ordres de Maintenance**\n\n"
        formatted += "| ID | Titre | Statut | Priorité | Type |\n"
        formatted += "|----|-------|--------|----------|------|\n"
        
        for order in data:
            formatted += f"| {order.get('id', 'N/A')} | {order.get('title', 'N/A')} | {order.get('status', 'N/A')} | {order.get('priority', 'N/A')} | {order.get('order_type', 'N/A')} |\n"
        
        return formatted
    
    def _format_notifications_list(self, result):
        """Formate la liste des notifications"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucune notification trouvée**"
        
        formatted = "🔔 **Liste des Notifications**\n\n"
        formatted += "| ID | Titre | Statut | Priorité | Type |\n"
        formatted += "|----|-------|--------|----------|------|\n"
        
        for notification in data:
            formatted += f"| {notification.get('id', 'N/A')} | {notification.get('title', 'N/A')} | {notification.get('status', 'N/A')} | {notification.get('priority', 'N/A')} | {notification.get('notification_type', 'N/A')} |\n"
        
        return formatted
    
    def _format_creation_response(self, result, item_type):
        """Formate la réponse de création"""
        if result.get("data"):
            return f"✅ **{item_type.capitalize()} créé(e) avec succès**\n\nID: {result['data'].get('id', 'N/A')}\nMessage: {result.get('message', 'Création réussie')}"
        else:
            return f"❌ **Erreur lors de la création de la {item_type}**\n\nMessage: {result.get('message', 'Erreur inconnue')}"
    
    def _format_equipment_details(self, result):
        """Formate les détails d'un équipement"""
        data = result.get("data")
        if not data:
            return "❌ **Équipement non trouvé**"
        
        formatted = "🏭 **Détails de l'Équipement**\n\n"
        formatted += f"**ID**: {data.get('id', 'N/A')}\n"
        formatted += f"**Nom**: {data.get('name', 'N/A')}\n"
        formatted += f"**Description**: {data.get('description', 'N/A')}\n"
        formatted += f"**Asset ID**: {data.get('asset_id', 'N/A')}\n"
        formatted += f"**Centre de Coût**: {data.get('cost_center', 'N/A')}\n"
        
        return formatted
    
    def _format_work_centers_list(self, result):
        """Formate la liste des centres de travail"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucun centre de travail trouvé**"
        
        formatted = "🏢 **Liste des Centres de Travail**\n\n"
        formatted += "| ID | Nom | Description |\n"
        formatted += "|----|-----|-------------|\n"
        
        for wc in data:
            formatted += f"| {wc.get('id', 'N/A')} | {wc.get('name', 'N/A')} | {wc.get('description', 'N/A')[:30]}... |\n"
        
        return formatted
    
    def _format_functional_locations_list(self, result):
        """Formate la liste des emplacements fonctionnels"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucun emplacement fonctionnel trouvé**"
        
        formatted = "📍 **Liste des Emplacements Fonctionnels**\n\n"
        formatted += "| ID | Nom | Description |\n"
        formatted += "|----|-----|-------------|\n"
        
        for fl in data:
            formatted += f"| {fl.get('id', 'N/A')} | {fl.get('name', 'N/A')} | {fl.get('description', 'N/A')[:30]}... |\n"
        
        return formatted
    
    def _format_materials_list(self, result):
        """Formate la liste des matériaux"""
        data = result.get("data", [])
        if not data:
            return "📋 **Aucun matériau trouvé**"
        
        formatted = "📦 **Liste des Matériaux**\n\n"
        formatted += "| ID | Nom | Description | Type |\n"
        formatted += "|----|-----|-------------|------|\n"
        
        for material in data:
            formatted += f"| {material.get('id', 'N/A')} | {material.get('name', 'N/A')} | {material.get('description', 'N/A')[:30]}... | {material.get('material_type', 'N/A')} |\n"
        
        return formatted
    
    def _format_generic_response(self, data):
        """Formate une réponse générique"""
        intent = data.get("intent", "unknown")
        confidence = data.get("confidence", 0.0)
        result = data.get("response", {}).get("result", {})
        
        formatted = f"🤖 **Réponse du Système**\n\n"
        formatted += f"**Intention détectée**: {intent}\n"
        formatted += f"**Confiance**: {confidence:.2f}\n\n"
        
        if result.get("message"):
            formatted += f"**Message**: {result['message']}\n"
        
        if result.get("data"):
            formatted += f"**Données**: {len(result['data'])} élément(s) trouvé(s)\n"
        
        return formatted

    def get_context_for_gpt_with_data(self, mcp_data, user_message):
        """Prépare le contexte pour ChatGPT avec les données MCP brutes"""
        context = f"""
DONNÉES BRUTES DU SERVEUR MCP:

Intent détecté: {mcp_data.get('intent', 'unknown')}
Confiance: {mcp_data.get('confidence', 0.0)}

RÉPONSE MCP:
{json.dumps(mcp_data.get('response', {}), indent=2, ensure_ascii=False)}

RÉSULTAT DÉTAILLÉ:
{json.dumps(mcp_data.get('response', {}).get('result', {}), indent=2, ensure_ascii=False)}

DEMANDE UTILISATEUR: {user_message}

INSTRUCTIONS:
- Analyse ces données brutes
- Organise-les selon la demande de l'utilisateur
- Crée des tableaux clairs et lisibles
- Utilise des emojis appropriés
- Sois précis et professionnel
"""
        return context

# Instance globale de l'agent
agent = HybridMaintenanceAgent()

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint pour le chat avec l'agent hybride"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message vide"}), 400
        
        # Traiter la demande avec l'agent hybride
        response = agent.process_user_request(user_message)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@app.route('/api/health')
def health_check():
    """Vérification de l'état du serveur"""
    try:
        # Vérifier la connexion au serveur MCP
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        mcp_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        mcp_status = "unreachable"
    
    try:
        # Vérifier la connexion au serveur SAP PM
        response = requests.get(f"{SAP_PM_URL}/health", timeout=5)
        sap_pm_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        sap_pm_status = "unreachable"
    
    # Vérifier OpenAI
    openai_status = "configured" if OPENAI_API_KEY else "not_configured"
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mcp_server": mcp_status,
        "sap_pm_server": sap_pm_status,
        "openai": openai_status,
        "conversation_history_length": len(agent.conversation_history)
    })

@app.route('/api/dashboard')
def dashboard():
    """Endpoint pour les données du dashboard"""
    try:
        # Calculer le taux de succès
        success_rate = 0
        if agent.stats['total_requests'] > 0:
            success_rate = (agent.stats['successful_requests'] / agent.stats['total_requests']) * 100
        
        return jsonify({
            "metrics": {
                "total_requests": agent.stats['total_requests'],
                "avg_response_time": round(agent.stats['avg_response_time'], 2),
                "success_rate": round(success_rate, 1),
                "active_agents": 3  # MCP, ChatGPT-4, SAP PM
            },
            "recent_activity": agent.conversation_history[-5:] if agent.conversation_history else [],
            "system_status": {
                "mcp_server": "healthy",
                "sap_pm_server": "healthy",
                "openai": "configured" if OPENAI_API_KEY else "not_configured"
            }
        })
    except Exception as e:
        return jsonify({"error": f"Erreur dashboard: {str(e)}"}), 500

@app.route('/api/agents')
def agents():
    """Endpoint pour les informations des agents"""
    return jsonify({
        "agents": [
            {
                "id": "mcp",
                "name": "Agent MCP",
                "description": "Requêtes techniques SAP PM",
                "category": "SAP",
                "icon": "fas fa-robot",
                "color": "blue",
                "usage_count": agent.stats['mcp_requests'],
                "status": "active"
            },
            {
                "id": "gpt4",
                "name": "ChatGPT-4",
                "description": "Conversation naturelle",
                "category": "Avancé",
                "icon": "fas fa-comments",
                "color": "green",
                "usage_count": agent.stats['gpt_requests'],
                "status": "active"
            },
            {
                "id": "analytics",
                "name": "Agent Analytics",
                "description": "Analyse de données",
                "category": "Avancé",
                "icon": "fas fa-chart-line",
                "color": "purple",
                "usage_count": 67,
                "status": "active"
            }
        ]
    })

@app.route('/api/stats')
def stats():
    """Endpoint pour les statistiques détaillées"""
    return jsonify({
        "performance": {
            "cpu_usage": 45,
            "memory_usage": 62,
            "network_usage": 28
        },
        "requests": {
            "total": agent.stats['total_requests'],
            "successful": agent.stats['successful_requests'],
            "failed": agent.stats['total_requests'] - agent.stats['successful_requests'],
            "avg_response_time": round(agent.stats['avg_response_time'], 2)
        },
        "agents": {
            "mcp_requests": agent.stats['mcp_requests'],
            "gpt_requests": agent.stats['gpt_requests'],
            "total_agents": 3
        }
    })

@app.route('/api/examples')
def get_examples():
    """Retourne des exemples de questions"""
    examples = [
        "Salut, comment ça va ?",
        "Donne-moi tous les équipements dans un tableau",
        "Montre-moi les ordres de maintenance ouverts",
        "Liste toutes les notifications",
        "Explique-moi la maintenance préventive",
        "Crée une notification de maintenance pour l'équipement EQ-001",
        "Quels sont les avantages de la maintenance prédictive ?"
    ]
    
    return jsonify({
        "examples": examples
    })

if __name__ == '__main__':
    print("🚀 Démarrage de l'application Flask avec MCP + ChatGPT-4...")
    print(f"📊 Serveur MCP: {MCP_SERVER_URL}")
    print(f"🏭 Serveur SAP PM: {SAP_PM_URL}")
    print(f"🤖 OpenAI GPT-4: {'Configuré' if OPENAI_API_KEY else 'Non configuré'}")
    print("🌐 Application disponible sur: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 