#!/usr/bin/env python3
"""
Script de démarrage pour l'application Flask - Agent de Maintenance Intelligente
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import flask
        import requests
        print("✅ Toutes les dépendances Flask sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        return False

def check_mcp_server():
    """Vérifie que le serveur MCP est accessible"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur MCP accessible")
            return True
        else:
            print("⚠️  Serveur MCP répond mais avec un statut non-200")
            return False
    except requests.exceptions.RequestException:
        print("❌ Serveur MCP non accessible")
        print("   Assurez-vous que le serveur MCP est démarré sur le port 8001")
        return False

def check_sap_pm_server():
    """Vérifie que le serveur SAP PM est accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur SAP PM accessible")
            return True
        else:
            print("⚠️  Serveur SAP PM répond mais avec un statut non-200")
            return False
    except requests.exceptions.RequestException:
        print("❌ Serveur SAP PM non accessible")
        print("   Assurez-vous que le serveur SAP PM est démarré sur le port 8000")
        return False

def start_flask_app():
    """Démarre l'application Flask"""
    print("🚀 Démarrage de l'application Flask...")
    try:
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Application Flask démarrée (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de l'application Flask: {e}")
        return None

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🤖 AGENT DE MAINTENANCE INTELLIGENTE - APPLICATION FLASK")
    print("=" * 60)
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🔍 Vérification des serveurs...")
    
    # Vérifier les serveurs (optionnel)
    mcp_ok = check_mcp_server()
    sap_pm_ok = check_sap_pm_server()
    
    if not mcp_ok or not sap_pm_ok:
        print("\n⚠️  ATTENTION: Certains serveurs ne sont pas accessibles")
        print("   L'application Flask peut fonctionner mais avec des limitations")
        print("   Pour une expérience complète, démarrez d'abord les serveurs:")
        print("   python start_servers.py")
        
        response = input("\nVoulez-vous continuer quand même ? (y/n): ")
        if response.lower() != 'y':
            print("Arrêt du démarrage")
            sys.exit(0)
    
    # Démarrer l'application Flask
    flask_process = start_flask_app()
    if not flask_process:
        print("❌ Impossible de démarrer l'application Flask")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 APPLICATION FLASK DÉMARRÉE AVEC SUCCÈS!")
    print("=" * 60)
    print("📊 URLs d'accès:")
    print("   • Application Flask: http://localhost:5000")
    print("   • Interface de chat: http://localhost:5000")
    print("   • API Flask: http://localhost:5000/api/")
    print("\n💡 Fonctionnalités:")
    print("   • Interface de chat intuitive")
    print("   • Questions en langage naturel")
    print("   • Formatage automatique des réponses")
    print("   • Indicateurs de statut en temps réel")
    print("   • Exemples de questions intégrés")
    print("\n⏹️  Appuyez sur Ctrl+C pour arrêter l'application")
    print("=" * 60)
    
    try:
        # Attendre que le processus se termine
        flask_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application Flask...")
        flask_process.terminate()
        print("✅ Application Flask arrêtée")

if __name__ == "__main__":
    main() 