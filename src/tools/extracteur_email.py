#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil d'extraction d'emails depuis du texte
Auteur: Assistant IA
Date: 2024
Description: Outil modulaire pour extraire et valider les adresses email depuis du texte
"""

import re
import os
from typing import List, Dict, Optional, Set, Tuple
from urllib.parse import urlparse
import json
from datetime import datetime


class ExtracteurEmail:
    """
    Classe pour extraire et valider les adresses email depuis du texte
    
    Cette classe fournit des méthodes pour identifier, extraire et valider
    les adresses email dans différents formats de texte.
    """
    
    def __init__(self, validation_stricte: bool = True, deduplication: bool = True):
        """
        Initialise l'extracteur d'emails
        
        Args:
            validation_stricte (bool): Utilise une validation stricte des emails (défaut: True)
            deduplication (bool): Supprime les doublons (défaut: True)
        """
        self.validation_stricte = validation_stricte
        self.deduplication = deduplication
        
        # Patterns regex pour différents types d'emails
        self.patterns = {
            'standard': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'avec_espaces': r'\b[A-Za-z0-9._%+\s-]+@[A-Za-z0-9.\s-]+\.[A-Z|a-z]{2,}\b',
            'avec_parentheses': r'\([^)]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}[^)]*\)',
            'avec_crochets': r'\[[^\]]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}[^\]]*\]',
            'avec_guillemets': r'"[^"]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}[^"]*"',
            'html': r'<[^>]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}[^>]*>',
            'markdown': r'\[[^\]]*\]\([^)]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}[^)]*\)'
        }
        
        # Domaines de messagerie courants pour validation
        self.domaines_courants = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com',
            'aol.com', 'icloud.com', 'protonmail.com', 'tutanota.com',
            'yandex.com', 'mail.ru', 'qq.com', '163.com', '126.com',
            'orange.fr', 'free.fr', 'laposte.net', 'wanadoo.fr', 'sfr.fr',
            'bouyguestelecom.fr', 'numericable.fr', 'neuf.fr'
        }
        
        # Caractères spéciaux autorisés dans les emails
        self.caracteres_speciaux = set('._%+-')
    
    def _nettoyer_email(self, email: str) -> str:
        """
        Nettoie une adresse email en supprimant les espaces et caractères indésirables
        
        Args:
            email (str): Email à nettoyer
            
        Returns:
            str: Email nettoyé
        """
        # Supprimer les espaces au début et à la fin
        email = email.strip()
        
        # Supprimer les espaces autour du @
        email = re.sub(r'\s*@\s*', '@', email)
        
        # Supprimer les espaces dans le nom d'utilisateur et le domaine
        email = re.sub(r'\s+', '', email)
        
        # Supprimer les caractères de ponctuation autour de l'email
        email = re.sub(r'^[\[\("\s]+|[\]\)"\s]+$', '', email)
        
        # Convertir en minuscules
        email = email.lower()
        
        return email
    
    def _valider_email(self, email: str) -> bool:
        """
        Valide une adresse email selon différents critères
        
        Args:
            email (str): Email à valider
            
        Returns:
            bool: True si l'email est valide, False sinon
        """
        if not email or '@' not in email:
            return False
        
        # Séparer le nom d'utilisateur et le domaine
        try:
            username, domain = email.split('@', 1)
        except ValueError:
            return False
        
        # Validation du nom d'utilisateur
        if not username or len(username) > 64:
            return False
        
        # Validation du domaine
        if not domain or len(domain) > 255:
            return False
        
        # Vérifier que le domaine a au moins un point
        if '.' not in domain:
            return False
        
        # Validation stricte si activée
        if self.validation_stricte:
            # Vérifier les caractères autorisés dans le nom d'utilisateur
            if not re.match(r'^[A-Za-z0-9._%+-]+$', username):
                return False
            
            # Vérifier les caractères autorisés dans le domaine
            if not re.match(r'^[A-Za-z0-9.-]+$', domain):
                return False
            
            # Vérifier que le domaine ne commence ou ne finit pas par un point
            if domain.startswith('.') or domain.endswith('.'):
                return False
            
            # Vérifier que le TLD a au moins 2 caractères
            tld = domain.split('.')[-1]
            if len(tld) < 2:
                return False
        
        return True
    
    def _extraire_avec_pattern(self, texte: str, pattern: str) -> List[str]:
        """
        Extrait les emails avec un pattern regex spécifique
        
        Args:
            texte (str): Texte à analyser
            pattern (str): Pattern regex à utiliser
            
        Returns:
            List[str]: Liste des emails trouvés
        """
        emails = []
        matches = re.finditer(pattern, texte, re.IGNORECASE)
        
        for match in matches:
            email_brut = match.group()
            
            # Extraire l'email du contexte (parentheses, crochets, etc.)
            if pattern in [self.patterns['avec_parentheses'], 
                          self.patterns['avec_crochets'], 
                          self.patterns['avec_guillemets'],
                          self.patterns['html'],
                          self.patterns['markdown']]:
                # Chercher l'email dans le match
                email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', email_brut)
                if email_match:
                    email_brut = email_match.group()
            
            # Nettoyer l'email
            email_propre = self._nettoyer_email(email_brut)
            
            # Valider l'email
            if self._valider_email(email_propre):
                emails.append(email_propre)
        
        return emails
    
    def extraire_emails(self, texte: str) -> List[str]:
        """
        Extrait toutes les adresses email valides d'un texte
        
        Args:
            texte (str): Texte à analyser
            
        Returns:
            List[str]: Liste des emails trouvés et validés
        """
        if not texte:
            return []
        
        tous_emails = []
        
        # Extraire avec tous les patterns
        for pattern_name, pattern in self.patterns.items():
            emails_pattern = self._extraire_avec_pattern(texte, pattern)
            tous_emails.extend(emails_pattern)
        
        # Supprimer les doublons si activé
        if self.deduplication:
            tous_emails = list(dict.fromkeys(tous_emails))  # Garde l'ordre
        
        return tous_emails
    
    def extraire_emails_avec_contexte(self, texte: str, contexte_lignes: int = 2) -> List[Dict[str, str]]:
        """
        Extrait les emails avec leur contexte dans le texte
        
        Args:
            texte (str): Texte à analyser
            contexte_lignes (int): Nombre de lignes de contexte à inclure
            
        Returns:
            List[Dict[str, str]]: Liste des emails avec contexte
        """
        if not texte:
            return []
        
        emails_avec_contexte = []
        lignes = texte.split('\n')
        
        for i, ligne in enumerate(lignes):
            emails_ligne = self.extraire_emails(ligne)
            
            for email in emails_ligne:
                # Calculer le contexte
                debut = max(0, i - contexte_lignes)
                fin = min(len(lignes), i + contexte_lignes + 1)
                contexte = '\n'.join(lignes[debut:fin])
                
                emails_avec_contexte.append({
                    'email': email,
                    'ligne': i + 1,
                    'contexte': contexte,
                    'ligne_exacte': ligne.strip()
                })
        
        return emails_avec_contexte
    
    def analyser_domaines(self, emails: List[str]) -> Dict[str, int]:
        """
        Analyse les domaines des emails extraits
        
        Args:
            emails (List[str]): Liste des emails
            
        Returns:
            Dict[str, int]: Dictionnaire domaine -> nombre d'occurrences
        """
        domaines = {}
        
        for email in emails:
            try:
                domaine = email.split('@')[1]
                domaines[domaine] = domaines.get(domaine, 0) + 1
            except (IndexError, AttributeError):
                continue
        
        return dict(sorted(domaines.items(), key=lambda x: x[1], reverse=True))
    
    def filtrer_par_domaine(self, emails: List[str], domaines: List[str]) -> List[str]:
        """
        Filtre les emails par domaine
        
        Args:
            emails (List[str]): Liste des emails
            domaines (List[str]): Liste des domaines à inclure
            
        Returns:
            List[str]: Emails filtrés
        """
        domaines_set = set(domaine.lower() for domaine in domaines)
        
        return [
            email for email in emails 
            if email.split('@')[1].lower() in domaines_set
        ]
    
    def exporter_json(self, emails: List[str], fichier_sortie: str) -> bool:
        """
        Exporte les emails au format JSON
        
        Args:
            emails (List[str]): Liste des emails
            fichier_sortie (str): Chemin du fichier de sortie
            
        Returns:
            bool: True si l'export a réussi, False sinon
        """
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'nombre_emails': len(emails),
                'emails': emails,
                'domaines': self.analyser_domaines(emails)
            }
            
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'export JSON: {str(e)}")
            return False
    
    def exporter_txt(self, emails: List[str], fichier_sortie: str) -> bool:
        """
        Exporte les emails au format texte simple
        
        Args:
            emails (List[str]): Liste des emails
            fichier_sortie (str): Chemin du fichier de sortie
            
        Returns:
            bool: True si l'export a réussi, False sinon
        """
        try:
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                f.write(f"# Emails extraits le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Nombre total: {len(emails)}\n\n")
                
                for i, email in enumerate(emails, 1):
                    f.write(f"{i}. {email}\n")
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'export TXT: {str(e)}")
            return False

