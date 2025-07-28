#!/usr/bin/env python3
"""
Script de test pour démontrer le flux MCP → ChatGPT-4
"""

import requests
import json
from datetime import datetime

def test_mcp_to_gpt_flow():
    """Test du flux complet MCP → ChatGPT-4"""
    
    print("🧪 **Test du Flux MCP → ChatGPT-4**")
    print("=" * 50)
    
    # Exemple de question utilisateur
    user_question = "Pourrais-tu me fournir la liste des équipements sous forme de tableau ?"
    
    print(f"📝 Question utilisateur: {user_question}")
    print()
    
    # Simuler l'appel à l'API Flask
    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={"message": user_question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ **Réponse du système:**")
            print(f"📊 Agents utilisés: {', '.join(data.get('agents_used', []))}")
            print(f"⏱️ Temps de réponse: {data.get('response_time', 0):.2f}s")
            print(f"🔧 Demande technique: {data.get('is_technical_request', False)}")
            print()
            
            print("🤖 **Réponse organisée par ChatGPT-4:**")
            print("-" * 40)
            print(data.get('message', 'Aucune réponse'))
            print("-" * 40)
            
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur Flask")
        print("   Assurez-vous que l'application est démarrée sur http://localhost:5000")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def test_different_questions():
    """Test avec différentes questions"""
    
    questions = [
        "Pourrais-tu me fournir la liste des équipements sous forme de tableau ?",
        "Montre-moi les ordres de maintenance ouverts",
        "Liste toutes les notifications",
        "Salut, comment ça va ?",
        "Explique-moi la maintenance préventive"
    ]
    
    print("🧪 **Test avec différentes questions**")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 30)
        
        try:
            response = requests.post(
                "http://localhost:5000/api/chat",
                json={"message": question},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                agents = ', '.join(data.get('agents_used', []))
                print(f"🤖 Agents: {agents}")
                print(f"⏱️ Temps: {data.get('response_time', 0):.2f}s")
                
                # Afficher un extrait de la réponse
                message = data.get('message', '')
                if len(message) > 100:
                    print(f"📝 Réponse: {message[:100]}...")
                else:
                    print(f"📝 Réponse: {message}")
            else:
                print(f"❌ Erreur: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests...")
    print()
    
    # Test 1: Flux complet
    test_mcp_to_gpt_flow()
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Questions variées
    test_different_questions()
    
    print("\n✅ Tests terminés!") 