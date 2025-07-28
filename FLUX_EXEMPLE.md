# 🔄 Flux MCP → ChatGPT-4 - Exemple Concret

## 📋 **Scénario d'Exemple**

**Question utilisateur :** *"Pourrais-tu me fournir la liste des équipements sous forme de tableau ?"*

---

## 🔄 **Étape 1: Détection de la Demande Technique**

```python
# Le système détecte que c'est une demande technique
technical_keywords = ["équipement", "tableau", "fournir", "liste"]
is_technical_request = True  # ✅ Détecté comme technique
```

---

## 🔄 **Étape 2: Appel au Serveur MCP**

```python
# Appel à l'API MCP
mcp_response = requests.post("http://localhost:8001/ask", {
    "query": "Pourrais-tu me fournir la liste des équipements sous forme de tableau ?",
    "session_id": "session_123"
})
```

**Réponse MCP (données brutes) :**
```json
{
  "success": true,
  "intent": "get_equipment_list",
  "confidence": 0.95,
  "response": {
    "result": {
      "action": "get_equipment_list",
      "count": 5,
      "data": [
        {
          "id": "df261fe9-66a5-4ab3-b580-de0177d34e33",
          "name": "Pompe Centrifuge P-001",
          "description": "Pompe principale du circuit de refroidissement",
          "asset_id": "ASSET001",
          "cost_center": "CC001",
          "functional_location_id": "d5bb83b3-fe50-4962-8bc4-f930ead11ff7"
        },
        {
          "id": "fef85973-f19d-4001-923d-cf1b71882c91",
          "name": "Moteur Électrique M-001",
          "description": "Moteur principal de production",
          "asset_id": "ASSET002",
          "cost_center": "CC002",
          "functional_location_id": "4c0e4202-92ad-4657-b9d8-da23e0a74c81"
        }
      ],
      "message": "Récupération de 5 équipements"
    }
  }
}
```

---

## 🔄 **Étape 3: Transfert vers ChatGPT-4**

```python
# Préparation du contexte pour ChatGPT-4
context = f"""
DONNÉES BRUTES DU SERVEUR MCP:

Intent détecté: get_equipment_list
Confiance: 0.95

RÉPONSE MCP:
{json.dumps(mcp_response, indent=2)}

DEMANDE UTILISATEUR: Pourrais-tu me fournir la liste des équipements sous forme de tableau ?

INSTRUCTIONS:
- Analyse ces données brutes
- Organise-les selon la demande de l'utilisateur
- Crée des tableaux clairs et lisibles
- Utilise des emojis appropriés
- Sois précis et professionnel
"""

# Appel à ChatGPT-4
gpt_response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un assistant spécialisé dans l'organisation de données..."},
        {"role": "user", "content": f"Organise ces données selon ma demande: {user_message}"}
    ]
)
```

---

## 🔄 **Étape 4: Réponse Organisée par ChatGPT-4**

**Réponse finale (organisée par ChatGPT-4) :**

```
🏭 **Liste des Équipements**

Voici la liste complète des équipements disponibles dans le système :

| ID | Nom | Description | Asset ID | Centre de Coût |
|----|-----|-------------|----------|----------------|
| df261fe9-66a5-4ab3-b580-de0177d34e33 | Pompe Centrifuge P-001 | Pompe principale du circuit de refroidissement | ASSET001 | CC001 |
| fef85973-f19d-4001-923d-cf1b71882c91 | Moteur Électrique M-001 | Moteur principal de production | ASSET002 | CC002 |
| edfb427d-7981-423c-8b98-fcabe84eb21f | Réservoir Stockage R-001 | Réservoir principal de stockage | ASSET003 | CC003 |
| 5bf222d7-c173-4e48-8424-39caabc108e3 | Convoyeur Transport C-001 | Convoyeur principal de transport | ASSET004 | CC004 |
| 07a34d8d-fd27-45b0-a222-d599874c3ef1 | Compresseur Air COMP-001 | Compresseur d'air principal | ASSET005 | CC001 |

📊 **Résumé :**
- **Total d'équipements :** 5
- **Centres de coût actifs :** CC001, CC002, CC003, CC004
- **Types d'équipements :** Pompes, Moteurs, Réservoirs, Convoyeurs, Compresseurs

✅ Les données ont été récupérées avec succès via le serveur MCP et organisées selon votre demande.
```

---

## 🎯 **Avantages de ce Flux**

### **1. Séparation des Responsabilités**
- **MCP** : Récupération des données brutes
- **ChatGPT-4** : Organisation et présentation

### **2. Flexibilité**
- ChatGPT-4 peut adapter la présentation selon la demande
- Tableaux, listes, résumés selon les besoins

### **3. Qualité de Présentation**
- Emojis appropriés
- Formatage markdown professionnel
- Informations contextuelles ajoutées

### **4. Gestion d'Erreurs**
- Si MCP échoue, ChatGPT-4 explique l'erreur
- Suggestions d'alternatives

---

## 🔧 **Exemples d'Autres Demandes**

### **Demande :** "Montre-moi les ordres de maintenance ouverts"
**Flux :** MCP → ChatGPT-4 → Tableau des ordres avec statuts

### **Demande :** "Salut, comment ça va ?"
**Flux :** ChatGPT-4 direct (pas de MCP)

### **Demande :** "Explique-moi la maintenance préventive"
**Flux :** ChatGPT-4 direct (explication générale)

---

## 📊 **Statistiques du Flux**

```python
{
  "agents_used": ["MCP", "ChatGPT-4"],
  "response_time": 2.3,
  "is_technical_request": True,
  "success": True
}
```

---

## 🚀 **Test du Flux**

Pour tester ce flux :

```bash
# Démarrer l'application
python start_app.py

# Dans un autre terminal, tester
python test_flow.py
```

Ou directement via l'interface web : http://localhost:5000 