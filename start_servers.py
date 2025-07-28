#!/usr/bin/env python3
"""
Script de démarrage pour les serveurs MCP et SAP PM
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import fastapi
        import uvicorn
        import openai
        import httpx
        import pydantic
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        return False

def check_env_file():
    """Vérifie la présence du fichier .env"""
    if not os.path.exists(".env"):
        print("⚠️  Fichier .env non trouvé")
        print("Créez un fichier .env basé sur env_example.txt")
        print("N'oubliez pas de configurer votre clé OpenAI API")
        return False
    return True

def start_sap_pm_server():
    """Démarre le serveur SAP PM"""
    print("🚀 Démarrage du serveur SAP PM...")
    sap_pm_dir = Path("SAP PM")
    if not sap_pm_dir.exists():
        print("❌ Dossier SAP PM non trouvé")
        return None
    
    try:
        # Changer vers le dossier SAP PM
        os.chdir(sap_pm_dir)
        
        # Démarrer le serveur SAP PM
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Revenir au répertoire racine
        os.chdir("..")
        
        print(f"✅ Serveur SAP PM démarré (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur SAP PM: {e}")
        return None

def start_mcp_server():
    """Démarre le serveur MCP"""
    print("🚀 Démarrage du serveur MCP...")
    try:
        process = subprocess.Popen([
            sys.executable, "main_mcp.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Serveur MCP démarré (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur MCP: {e}")
        return None

def wait_for_servers():
    """Attend que les serveurs soient prêts"""
    print("⏳ Attente du démarrage des serveurs...")
    time.sleep(5)
    print("✅ Serveurs prêts!")

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🔧 DÉMARRAGE DES SERVEURS TEAL HACK")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_file():
        print("Continuez avec les valeurs par défaut...")
    
    # Démarrer les serveurs
    sap_pm_process = start_sap_pm_server()
    if not sap_pm_process:
        print("❌ Impossible de démarrer le serveur SAP PM")
        sys.exit(1)
    
    # Attendre un peu avant de démarrer le serveur MCP
    time.sleep(2)
    
    mcp_process = start_mcp_server()
    if not mcp_process:
        print("❌ Impossible de démarrer le serveur MCP")
        sap_pm_process.terminate()
        sys.exit(1)
    
    # Attendre que les serveurs soient prêts
    wait_for_servers()
    
    print("\n" + "=" * 50)
    print("🎉 SERVEURS DÉMARRÉS AVEC SUCCÈS!")
    print("=" * 50)
    print("📊 URLs d'accès:")
    print("   • SAP PM API: http://localhost:8000")
    print("   • SAP PM Docs: http://localhost:8000/docs")
    print("   • MCP Server: http://localhost:8001")
    print("   • MCP Docs: http://localhost:8001/docs")
    print("\n💡 Exemples d'utilisation:")
    print("   • Créer une session: POST http://localhost:8001/session")
    print("   • Poser une question: POST http://localhost:8001/ask")
    print("   • Voir les équipements: GET http://localhost:8000/equipment/")
    print("\n⏹️  Appuyez sur Ctrl+C pour arrêter les serveurs")
    print("=" * 50)
    
    try:
        # Attendre que les processus se terminent
        sap_pm_process.wait()
        mcp_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        sap_pm_process.terminate()
        mcp_process.terminate()
        print("✅ Serveurs arrêtés")

if __name__ == "__main__":
    main() 