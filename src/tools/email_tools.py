"""
Outils de lecture d'emails pour l'ADK (Agent Development Kit)
Permet aux agents de lire et analyser les emails entrants
"""

import os
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import re
from adk.api.tool_manager import tool

# Configuration des serveurs email
EMAIL_CONFIGS = {
    "gmail": {
        "imap_server": "imap.gmail.com",
        "smtp_server": "smtp.gmail.com",
        "port": 993
    },
    "outlook": {
        "imap_server": "outlook.office365.com", 
        "smtp_server": "smtp.office365.com",
        "port": 993
    },
    "yahoo": {
        "imap_server": "imap.mail.yahoo.com",
        "smtp_server": "smtp.mail.yahoo.com", 
        "port": 993
    }
}

@tool
async def read_new_emails(
    email_provider: str = "gmail",
    folder: str = "INBOX",
    max_emails: int = 10,
    days_back: int = 1,
    search_keywords: Optional[str] = None
) -> str:
    """
    Lit les nouveaux emails depuis la boîte de réception.
    Utilisez cet outil pour surveiller les emails entrants et détecter les demandes de maintenance.
    
    Args:
        email_provider: Fournisseur email ('gmail', 'outlook', 'yahoo')
        folder: Dossier à lire ('INBOX', 'Sent', 'Drafts', etc.)
        max_emails: Nombre maximum d'emails à lire
        days_back: Nombre de jours en arrière pour chercher
        search_keywords: Mots-clés pour filtrer les emails (optionnel)
    
    Returns:
        Résumé des emails lus avec les informations importantes
    """
    try:
        # Récupération des credentials depuis les variables d'environnement
        email_address = os.getenv(f"{email_provider.upper()}_EMAIL")
        password = os.getenv(f"{email_provider.upper()}_PASSWORD")
        
        if not email_address or not password:
            return f"❌ Configuration email manquante pour {email_provider}. Configurez {email_provider.upper()}_EMAIL et {email_provider.upper()}_PASSWORD"
        
        config = EMAIL_CONFIGS.get(email_provider.lower())
        if not config:
            return f"❌ Fournisseur email non supporté: {email_provider}"
        
        # Connexion au serveur IMAP
        mail = imaplib.IMAP4_SSL(config["imap_server"], config["port"])
        mail.login(email_address, password)
        mail.select(folder)
        
        # Recherche des emails récents
        date_since = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
        search_criteria = f'(SINCE "{date_since}")'
        
        if search_keywords:
            search_criteria += f' (SUBJECT "{search_keywords}")'
        
        _, message_numbers = mail.search(None, search_criteria)
        email_list = message_numbers[0].split()
        
        # Limitation du nombre d'emails
        email_list = email_list[-max_emails:] if len(email_list) > max_emails else email_list
        
        emails_summary = []
        
        for num in email_list:
            _, msg_data = mail.fetch(num, '(RFC822)')
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extraction des informations
            subject = email_message.get('subject', 'Sans objet')
            sender = email_message.get('from', 'Expéditeur inconnu')
            date = email_message.get('date', 'Date inconnue')
            
            # Extraction du contenu
            content = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        break
            else:
                content = email_message.get_payload(decode=True).decode()
            
            # Analyse du contenu pour détecter les demandes de maintenance
            maintenance_keywords = [
                'maintenance', 'réparation', 'panne', 'défaut', 'problème',
                'équipement', 'machine', 'pompe', 'moteur', 'urgent',
                'arrêt', 'dysfonctionnement', 'bruit', 'vibration'
            ]
            
            is_maintenance_related = any(
                keyword.lower() in content.lower() or keyword.lower() in subject.lower()
                for keyword in maintenance_keywords
            )
            
            email_info = {
                "subject": subject,
                "sender": sender,
                "date": date,
                "content_preview": content[:200] + "..." if len(content) > 200 else content,
                "is_maintenance_related": is_maintenance_related,
                "priority": "HIGH" if is_maintenance_related else "NORMAL"
            }
            
            emails_summary.append(email_info)
        
        mail.close()
        mail.logout()
        
        # Formatage de la réponse
        maintenance_emails = [e for e in emails_summary if e["is_maintenance_related"]]
        total_emails = len(emails_summary)
        
        result = f"📧 {total_emails} emails lus depuis {folder}\n"
        result += f"🔧 {len(maintenance_emails)} emails liés à la maintenance détectés\n\n"
        
        if maintenance_emails:
            result += "🚨 EMAILS DE MAINTENANCE DÉTECTÉS:\n"
            for i, email_info in enumerate(maintenance_emails, 1):
                result += f"{i}. De: {email_info['sender']}\n"
                result += f"   Objet: {email_info['subject']}\n"
                result += f"   Date: {email_info['date']}\n"
                result += f"   Contenu: {email_info['content_preview']}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de la lecture des emails: {str(e)}"

@tool
async def send_maintenance_notification_email(
    recipient_email: str,
    subject: str,
    message: str,
    priority: str = "normal",
    equipment_id: Optional[str] = None,
    order_id: Optional[str] = None
) -> str:
    """
    Envoie un email de notification de maintenance.
    Utilisez cet outil pour informer les équipes des actions de maintenance.
    
    Args:
        recipient_email: Adresse email du destinataire
        subject: Objet de l'email
        message: Contenu du message
        priority: Priorité ('low', 'normal', 'high', 'urgent')
        equipment_id: ID de l'équipement concerné (optionnel)
        order_id: ID de l'ordre de travail (optionnel)
    
    Returns:
        Confirmation de l'envoi de l'email
    """
    try:
        # Configuration par défaut (Gmail)
        email_address = os.getenv("GMAIL_EMAIL")
        password = os.getenv("GMAIL_PASSWORD")
        
        if not email_address or not password:
            return "❌ Configuration email manquante. Configurez GMAIL_EMAIL et GMAIL_PASSWORD"
        
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Ajout des informations de contexte
        context_info = ""
        if equipment_id:
            context_info += f"\nÉquipement concerné: {equipment_id}"
        if order_id:
            context_info += f"\nOrdre de travail: {order_id}"
        
        # Formatage selon la priorité
        priority_indicators = {
            "low": "🟢",
            "normal": "🟡", 
            "high": "🟠",
            "urgent": "🔴"
        }
        
        priority_indicator = priority_indicators.get(priority.lower(), "🟡")
        formatted_message = f"{priority_indicator} NOTIFICATION DE MAINTENANCE\n\n{message}{context_info}"
        
        msg.attach(MIMEText(formatted_message, 'plain', 'utf-8'))
        
        # Envoi via SMTP
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, password)
        
        text = msg.as_string()
        server.sendmail(email_address, recipient_email, text)
        server.quit()
        
        return f"✅ Email envoyé avec succès à {recipient_email}\nObjet: {subject}\nPriorité: {priority}"
        
    except Exception as e:
        return f"❌ Erreur lors de l'envoi de l'email: {str(e)}"

@tool
async def analyze_email_content(
    email_content: str,
    extract_entities: bool = True,
    detect_sentiment: bool = True
) -> str:
    """
    Analyse le contenu d'un email pour extraire les informations importantes.
    Utilisez cet outil pour comprendre les demandes dans les emails.
    
    Args:
        email_content: Contenu de l'email à analyser
        extract_entities: Extraire les entités (équipements, dates, etc.)
        detect_sentiment: Détecter le sentiment (urgent, normal, etc.)
    
    Returns:
        Analyse structurée du contenu de l'email
    """
    try:
        analysis = {
            "entities": {},
            "sentiment": "neutral",
            "urgency_level": "normal",
            "maintenance_keywords": [],
            "equipment_mentioned": [],
            "dates_mentioned": []
        }
        
        # Extraction des entités
        if extract_entities:
            # Détection des équipements (patterns comme P-101, EQ-123, etc.)
            equipment_pattern = r'\b[A-Z]+-\d+\b'
            equipment_matches = re.findall(equipment_pattern, email_content)
            analysis["equipment_mentioned"] = list(set(equipment_matches))
            
            # Détection des dates
            date_patterns = [
                r'\d{1,2}/\d{1,2}/\d{4}',
                r'\d{1,2}-\d{1,2}-\d{4}',
                r'\d{4}-\d{2}-\d{2}',
                r'aujourd\'hui',
                r'demain',
                r'urgent',
                r'immédiat'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, email_content, re.IGNORECASE)
                if matches:
                    analysis["dates_mentioned"].extend(matches)
        
        # Détection des mots-clés de maintenance
        maintenance_keywords = [
            'maintenance', 'réparation', 'panne', 'défaut', 'problème',
            'équipement', 'machine', 'pompe', 'moteur', 'urgent',
            'arrêt', 'dysfonctionnement', 'bruit', 'vibration',
            'fuite', 'température', 'pression', 'niveau'
        ]
        
        found_keywords = []
        for keyword in maintenance_keywords:
            if keyword.lower() in email_content.lower():
                found_keywords.append(keyword)
        
        analysis["maintenance_keywords"] = found_keywords
        
        # Analyse du sentiment et de l'urgence
        if detect_sentiment:
            urgent_words = ['urgent', 'immédiat', 'critique', 'arrêt', 'panne', 'défaut']
            normal_words = ['maintenance', 'préventif', 'planifié', 'routine']
            
            urgent_count = sum(1 for word in urgent_words if word.lower() in email_content.lower())
            normal_count = sum(1 for word in normal_words if word.lower() in email_content.lower())
            
            if urgent_count > normal_count:
                analysis["sentiment"] = "urgent"
                analysis["urgency_level"] = "high"
            elif normal_count > urgent_count:
                analysis["sentiment"] = "normal"
                analysis["urgency_level"] = "low"
            else:
                analysis["sentiment"] = "neutral"
                analysis["urgency_level"] = "normal"
        
        # Formatage de la réponse
        result = "📊 ANALYSE DE L'EMAIL:\n\n"
        
        if analysis["equipment_mentioned"]:
            result += f"🏭 Équipements mentionnés: {', '.join(analysis['equipment_mentioned'])}\n"
        
        if analysis["dates_mentioned"]:
            result += f"📅 Dates/échéances: {', '.join(analysis['dates_mentioned'])}\n"
        
        if analysis["maintenance_keywords"]:
            result += f"🔧 Mots-clés maintenance: {', '.join(analysis['maintenance_keywords'])}\n"
        
        result += f"🎯 Sentiment: {analysis['sentiment']}\n"
        result += f"⚡ Niveau d'urgence: {analysis['urgency_level']}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de l'analyse de l'email: {str(e)}"

@tool
async def setup_email_monitoring(
    email_provider: str = "gmail",
    monitoring_folders: List[str] = ["INBOX"],
    keywords_to_monitor: List[str] = None,
    auto_respond: bool = False
) -> str:
    """
    Configure la surveillance automatique des emails.
    Utilisez cet outil pour mettre en place une surveillance continue.
    
    Args:
        email_provider: Fournisseur email à surveiller
        monitoring_folders: Dossiers à surveiller
        keywords_to_monitor: Mots-clés pour filtrer les emails
        auto_respond: Activer les réponses automatiques
    
    Returns:
        Confirmation de la configuration
    """
    try:
        # Validation de la configuration
        if email_provider not in EMAIL_CONFIGS:
            return f"❌ Fournisseur non supporté: {email_provider}"
        
        # Sauvegarde de la configuration
        config = {
            "email_provider": email_provider,
            "monitoring_folders": monitoring_folders,
            "keywords_to_monitor": keywords_to_monitor or [
                'maintenance', 'réparation', 'panne', 'défaut', 'problème',
                'équipement', 'machine', 'pompe', 'moteur', 'urgent'
            ],
            "auto_respond": auto_respond,
            "last_check": datetime.now().isoformat()
        }
        
        # Sauvegarde dans un fichier de configuration
        config_file = "email_monitoring_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        result = f"✅ Surveillance email configurée:\n"
        result += f"📧 Fournisseur: {email_provider}\n"
        result += f"📁 Dossiers surveillés: {', '.join(monitoring_folders)}\n"
        result += f"🔍 Mots-clés: {', '.join(config['keywords_to_monitor'])}\n"
        result += f"🤖 Réponses automatiques: {'Activées' if auto_respond else 'Désactivées'}\n"
        result += f"💾 Configuration sauvegardée dans {config_file}"
        
        return result
        
    except Exception as e:
        return f"❌ Erreur lors de la configuration: {str(e)}" 