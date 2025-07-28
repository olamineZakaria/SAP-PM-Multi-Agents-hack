#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil de recherche web utilisant l'API Serper.dev
Auteur: Assistant IA
Date: 2024
Description: Outil modulaire pour effectuer des recherches web via l'API Serper.dev
"""

import http.client
import json
import os
import ssl
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlencode
import time


class RechercheWebSerper:
    """
    Classe pour effectuer des recherches web via l'API Serper.dev
    
    Cette classe fournit une interface simple pour interroger l'API Serper.dev
    et récupérer les résultats de recherche web.
    """
    
    def __init__(self, api_key: Optional[str] = None, max_results: int = 5):
        """
        Initialise l'outil de recherche web
        
        Args:
            api_key (str, optional): Clé API Serper.dev. Si None, cherche dans les variables d'environnement
            max_results (int): Nombre maximum de résultats à retourner (défaut: 5)
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.max_results = max_results
        self.base_url = "google.serper.dev"
        self.endpoint = "/search"
        
        if not self.api_key:
            raise ValueError("Clé API manquante. Fournissez une clé API ou définissez SERPER_API_KEY")

    def _get_api_key_from_env(self) -> Optional[str]:
        """
        Récupère la clé API depuis les variables d'environnement
        
        Returns:
            str: Clé API ou None si non trouvée
        """
        return os.getenv('SERPER_API_KEY','1353b078cf784853e65953d76546742c2788aa81')
    
    def _create_connection(self) -> http.client.HTTPSConnection:
        """
        Crée une connexion HTTPS sécurisée
        
        Returns:
            http.client.HTTPSConnection: Connexion HTTPS configurée
        """
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        return http.client.HTTPSConnection(
            self.base_url,
            context=context,
            timeout=30
        )
    
    def _make_api_request(self, query: str) -> Dict:
        """
        Effectue une requête à l'API Serper.dev
        
        Args:
            query (str): Requête de recherche
            
        Returns:
            Dict: Réponse de l'API
            
        Raises:
            ConnectionError: Erreur de connexion
            ValueError: Erreur de réponse API
            Exception: Autres erreurs
        """
        # Préparation des données de la requête
        payload = {
            "q": query,
            "num": self.max_results
        }
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        connection = None
        try:
            # Création de la connexion
            connection = self._create_connection()
            
            # Encodage des données
            json_payload = json.dumps(payload)
            
            # Envoi de la requête
            connection.request(
                "POST",
                self.endpoint,
                body=json_payload,
                headers=headers
            )
            
            # Récupération de la réponse
            response = connection.getresponse()
            
            # Vérification du code de statut
            if response.status != 200:
                error_msg = f"Erreur API: {response.status} - {response.reason}"
                try:
                    error_data = json.loads(response.read().decode('utf-8'))
                    if 'message' in error_data:
                        error_msg += f" - {error_data['message']}"
                except:
                    pass
                raise ValueError(error_msg)
            
            # Lecture et parsing de la réponse
            response_data = response.read().decode('utf-8')
            return json.loads(response_data)
            
        except http.client.HTTPException as e:
            raise ConnectionError(f"Erreur HTTP lors de la connexion à l'API: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing de la réponse JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur inattendue: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def _extract_results(self, api_response: Dict) -> List[Dict[str, str]]:
        """
        Extrait les résultats de recherche de la réponse API
        
        Args:
            api_response (Dict): Réponse brute de l'API
            
        Returns:
            List[Dict[str, str]]: Liste des résultats formatés
        """
        results = []
        
        try:
            # Extraction des résultats organiques
            organic_results = api_response.get('organic', [])
            
            for i, result in enumerate(organic_results[:self.max_results]):
                title = result.get('title', f'Résultat {i+1}')
                link = result.get('link', '')
                
                results.append({
                    'titre': title,
                    'lien': link,
                    'position': i + 1
                })
            
            # Si pas assez de résultats organiques, ajouter des résultats de recherche
            if len(results) < self.max_results:
                search_results = api_response.get('searchResults', [])
                for i, result in enumerate(search_results[:self.max_results - len(results)]):
                    title = result.get('title', f'Résultat de recherche {len(results) + i + 1}')
                    link = result.get('link', '')
                    
                    results.append({
                        'titre': title,
                        'lien': link,
                        'position': len(results) + i + 1
                    })
                    
        except Exception as e:
            print(f"Attention: Erreur lors de l'extraction des résultats: {str(e)}")
        
        return results
    
    def chercher(self, requete: str) -> List[Dict[str, str]]:
        """
        Effectue une recherche web
        
        Args:
            requete (str): Requête de recherche en langage naturel
            
        Returns:
            List[Dict[str, str]]: Liste des résultats avec titre et lien
            
        Raises:
            ValueError: Erreur de validation ou API
            ConnectionError: Erreur de connexion
            Exception: Autres erreurs
        """
        if not requete or not requete.strip():
            raise ValueError("La requête ne peut pas être vide")
        
        try:
            # Effectuer la requête API
            api_response = self._make_api_request(requete.strip())
            
            # Extraire et formater les résultats
            results = self._extract_results(api_response)
            
            return results
            
        except Exception as e:
            # Relancer l'exception avec plus de contexte
            raise type(e)(f"Erreur lors de la recherche '{requete}': {str(e)}")
    
    def chercher_avec_retry(self, requete: str, max_retries: int = 3, delay: float = 1.0) -> List[Dict[str, str]]:
        """
        Effectue une recherche avec retry en cas d'échec
        
        Args:
            requete (str): Requête de recherche
            max_retries (int): Nombre maximum de tentatives
            delay (float): Délai entre les tentatives en secondes
            
        Returns:
            List[Dict[str, str]]: Résultats de recherche
        """
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return self.chercher(requete)
            except (ConnectionError, http.client.HTTPException) as e:
                last_exception = e
                if attempt < max_retries - 1:
                    print(f"Tentative {attempt + 1} échouée, nouvelle tentative dans {delay} secondes...")
                    time.sleep(delay)
                    delay *= 2  # Backoff exponentiel
            except Exception as e:
                # Pour les autres erreurs, ne pas retry
                raise e
        
        # Si toutes les tentatives ont échoué
        raise last_exception


