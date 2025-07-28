#!/usr/bin/env python3
"""
Exemple de test pour montrer le formatage markdown
"""

import requests
import json

def test_markdown_formatting():
    """Test du formatage markdown"""
    
    print("🎨 **Test du Formatage Markdown**")
    print("=" * 50)
    
    # Exemple de question qui devrait générer un tableau bien formaté
    questions = [
        "Pourrais-tu me fournir la liste des équipements sous forme de tableau ?",
        "Montre-moi les ordres de maintenance ouverts",
        "Liste toutes les notifications avec leurs statuts"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://localhost:5000/api/chat",
                json={"message": question},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ **Réponse formatée :**")
                print("```markdown")
                print(data.get('message', 'Aucune réponse'))
                print("```")
                
                print(f"\n📊 Agents utilisés: {', '.join(data.get('agents_used', []))}")
                print(f"⏱️ Temps de réponse: {data.get('response_time', 0):.2f}s")
                
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")

def show_markdown_example():
    """Affiche un exemple de markdown bien formaté"""
    
    example_markdown = """
## 🏭 Liste des Équipements

Voici la liste complète des équipements disponibles dans le système de maintenance :

| ID | Nom | Description | Asset ID | Centre de Coût |
|----|-----|-------------|----------|----------------|
| df261fe9-66a5-4ab3-b580-de0177d34e33 | Pompe Centrifuge P-001 | Pompe principale du circuit de refroidissement | ASSET001 | CC001 |
| fef85973-f19d-4001-923d-cf1b71882c91 | Moteur Électrique M-001 | Moteur principal de production | ASSET002 | CC002 |
| edfb427d-7981-423c-8b98-fcabe84eb21f | Réservoir Stockage R-001 | Réservoir principal de stockage | ASSET003 | CC003 |

📊 **Résumé des données :**
- **Total d'équipements :** 3
- **Centres de coût actifs :** CC001, CC002, CC003
- **Types d'équipements :** Pompes, Moteurs, Réservoirs

🔧 **Informations techniques :**
- Tous les équipements sont opérationnels
- Maintenance préventive programmée
- Capteurs IoT connectés

✅ **Source :** Données récupérées avec succès via le serveur MCP et organisées selon votre demande.
"""
    
    print("📝 **Exemple de Markdown Bien Formaté**")
    print("=" * 50)
    print(example_markdown)

if __name__ == "__main__":
    print("🚀 Test du formatage markdown...")
    print()
    
    # Afficher l'exemple
    show_markdown_example()
    
    print("\n" + "="*60 + "\n")
    
    # Tester avec l'API réelle
    test_markdown_formatting()
    
    print("\n✅ Test terminé!") 