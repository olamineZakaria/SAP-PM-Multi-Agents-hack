#!/usr/bin/env python3
"""
Script de démarrage pour l'application Flask avec MCP + ChatGPT-4
"""

import os
import sys
import subprocess
import time
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_openai_config():
    """Vérifie la configuration OpenAI"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ **ERREUR**: OPENAI_API_KEY non configurée")
        print("   Ajoutez votre clé API OpenAI dans le fichier .env")
        return False
    
    if api_key == "your-openai-api-key-here":
        print("❌ **ERREUR**: OPENAI_API_KEY n'est pas configurée")
        print("   Remplacez 'your-openai-api-key-here' par votre vraie clé API")
        return False
    
    print("✅ Configuration OpenAI OK")
    return True

def check_sap_pm_server():
    """Vérifie si le serveur SAP PM est accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur SAP PM accessible")
            return True
        else:
            print("❌ Serveur SAP PM non accessible")
            return False
    except requests.exceptions.RequestException:
        print("❌ Serveur SAP PM non accessible")
        print("   Assurez-vous que le serveur SAP PM est démarré sur le port 8000")
        return False

def check_mcp_server():
    """Vérifie si le serveur MCP est accessible"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur MCP accessible")
            return True
        else:
            print("❌ Serveur MCP non accessible")
            return False
    except requests.exceptions.RequestException:
        print("❌ Serveur MCP non accessible")
        print("   Assurez-vous que le serveur MCP est démarré sur le port 8001")
        return False

def start_sap_pm_server():
    """Démarre le serveur SAP PM"""
    print("🚀 Démarrage du serveur SAP PM...")
    
    sap_pm_dir = "SAP PM"
    if not os.path.exists(sap_pm_dir):
        print(f"❌ Répertoire {sap_pm_dir} non trouvé")
        return False
    
    try:
        # Changer vers le répertoire SAP PM
        os.chdir(sap_pm_dir)
        
        # Démarrer le serveur
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Revenir au répertoire parent
        os.chdir("..")
        
        # Attendre un peu pour que le serveur démarre
        time.sleep(3)
        
        # Vérifier si le serveur répond
        if check_sap_pm_server():
            print("✅ Serveur SAP PM démarré avec succès")
            return True
        else:
            print("❌ Échec du démarrage du serveur SAP PM")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur SAP PM: {str(e)}")
        return False

def start_mcp_server():
    """Démarre le serveur MCP"""
    print("🚀 Démarrage du serveur MCP...")
    
    if not os.path.exists("main_mcp.py"):
        print("❌ Fichier main_mcp.py non trouvé")
        return False
    
    try:
        # Démarrer le serveur MCP
        process = subprocess.Popen(
            [sys.executable, "main_mcp.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre un peu pour que le serveur démarre
        time.sleep(3)
        
        # Vérifier si le serveur répond
        if check_mcp_server():
            print("✅ Serveur MCP démarré avec succès")
            return True
        else:
            print("❌ Échec du démarrage du serveur MCP")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur MCP: {str(e)}")
        return False

def start_flask_app():
    """Démarre l'application Flask"""
    print("🚀 Démarrage de l'application Flask avec MCP + ChatGPT-4...")
    
    try:
        # Démarrer l'application Flask
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("✅ Application Flask démarrée")
        print("🌐 Application disponible sur: http://localhost:5000")
        print("🤖 MCP + ChatGPT-4 intégrés et prêts à l'utilisation")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de Flask: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🤖 **Agent de Maintenance Intelligente avec MCP + ChatGPT-4**")
    print("=" * 70)
    
    # Vérifier la configuration OpenAI
    if not check_openai_config():
        return
    
    # Vérifier le serveur SAP PM
    if not check_sap_pm_server():
        print("\n🔄 Tentative de démarrage du serveur SAP PM...")
        if not start_sap_pm_server():
            print("❌ Impossible de démarrer le serveur SAP PM")
            print("   Vérifiez que le répertoire 'SAP PM' existe et contient main.py")
            return
    
    # Vérifier le serveur MCP
    if not check_mcp_server():
        print("\n🔄 Tentative de démarrage du serveur MCP...")
        if not start_mcp_server():
            print("❌ Impossible de démarrer le serveur MCP")
            print("   Vérifiez que le fichier main_mcp.py existe")
            return
    
    # Démarrer l'application Flask
    print("\n🚀 Démarrage de l'application...")
    if start_flask_app():
        print("\n🎉 **Application prête !**")
        print("   - Interface web: http://localhost:5000")
        print("   - Serveur MCP: http://localhost:8001")
        print("   - Serveur SAP PM: http://localhost:8000")
        print("   - ChatGPT-4: Intégré et fonctionnel")
        print("\n💡 Exemples de questions:")
        print("   • 'Salut, comment ça va ?' (ChatGPT-4)")
        print("   • 'Donne-moi tous les équipements' (MCP)")
        print("   • 'Explique-moi la maintenance préventive' (ChatGPT-4)")
        print("   • 'Montre-moi les ordres de maintenance ouverts' (MCP)")
    else:
        print("❌ Échec du démarrage de l'application")

if __name__ == "__main__":
    main() 