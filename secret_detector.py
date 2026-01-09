
"""
Module de détection d'informations sensibles
"""
import re
from typing import List, Dict, Optional
from config import MODELES_SENSIBLES, EXTENSIONS_EXCLUES, DOSSIERS_EXCLUS


class DetecteurSecret:
    """Détecteur d'informations sensibles"""
    
    def __init__(self, modeles: List[str] = MODELES_SENSIBLES):
        """
        Initialisation du détecteur
        
        Args:
            modeles: Liste de motifs d'expressions régulières
        """
        self.modeles = [re.compile(modele) for modele in modeles]
        self.extensions_exclues = EXTENSIONS_EXCLUES
        self.dossiers_exclus = DOSSIERS_EXCLUS
    
    def devrait_analyser_fichier(self, chemin_fichier: str) -> bool:
        """
        Déterminer si un fichier doit être analysé
        
        Args:
            chemin_fichier: Chemin du fichier
            
        Returns:
            Si le fichier doit être analysé
        """
        # Vérifier l'extension du fichier
        for ext in self.extensions_exclues:
            if chemin_fichier.lower().endswith(ext):
                return False
        
        # Vérifier le répertoire
        parties_chemin = chemin_fichier.split('/')
        for dossier_exclu in self.dossiers_exclus:
            if dossier_exclu in parties_chemin:
                return False
        
        return True
    
    def detecter_secrets_dans_texte(self, texte: str, chemin_fichier: str = "") -> List[Dict]:
        """
        Détecter les informations sensibles dans un texte
        
        Args:
            texte: Contenu texte à analyser
            chemin_fichier: Chemin du fichier (pour le rapport)
            
        Returns:
            Liste des informations sensibles détectées
        """
        if not texte:
            return []
        
        decouvertes = []
        lignes = texte.split('\n')
        
        for numero_ligne, ligne in enumerate(lignes, 1):
            for modele in self.modeles:
                correspondances = modele.finditer(ligne)
                for correspondance in correspondances:
                    # Extraire la clé correspondante
                    secret = correspondance.group(0)
                    
                    # Vérifier si c'est probablement un commentaire ou un exemple
                    if self._est_probablement_exemple(ligne, secret):
                        continue
                    
                    decouvertes.append({
                        'chemin_fichier': chemin_fichier,
                        'numero_ligne': numero_ligne,
                        'contenu_ligne': ligne.strip(),
                        'secret': secret,
                        'modele': modele.pattern,
                        'confiance': self._calculer_confiance(secret, ligne)
                    })
        
        return decouvertes
    
    def _est_probablement_exemple(self, ligne: str, secret: str) -> bool:
        """
        Déterminer si c'est probablement du code d'exemple
        
        Args:
            ligne: Ligne de code
            secret: Clé détectée
            
        Returns:
            Si c'est probablement un exemple
        """
        ligne_minuscules = ligne.lower()
        
        # Vérifier la présence de mots-clés liés aux exemples
        mots_cles_exemples = [
            'exemple', 'sample', 'demo', 'test', 'placeholder',
            'your_api_key', 'your-api-key', 'xxx', 'yyy',
            'todo', 'replace', 'change_me', 'changeme'
        ]
        
        for mot_cle in mots_cles_exemples:
            if mot_cle in ligne_minuscules:
                return True
        
        # Vérifier si la clé contient des modèles évidents de texte de substitution
        modeles_substitution = [
            r'x{10,}',  # Plusieurs x
            r'_+',      # Plusieurs underscores
            r'\*{3,}',  # Plusieurs astérisques
        ]
        
        for modele in modeles_substitution:
            if re.search(modele, secret, re.IGNORECASE):
                return True
        
        return False
    
    def _calculer_confiance(self, secret: str, ligne: str) -> str:
        """
        Calculer le niveau de confiance
        
        Args:
            secret: Clé détectée
            ligne: Ligne de code
            
        Returns:
            Niveau de confiance (elevee/moyenne/faible)
        """
        # Confiance élevée : format de clé complet et pas dans un commentaire
        if (secret.startswith('sk-') and len(secret) > 40 and 
            not ligne.strip().startswith('#') and 
            not ligne.strip().startswith('//')):
            return 'elevee'
        
        # Confiance moyenne : correspond au modèle de base
        if len(secret) >= 30:
            return 'moyenne'
        
        # Confiance faible
        return 'faible'
    
    def filtrer_confiance_elevee(self, decouvertes: List[Dict]) -> List[Dict]:
        """
        Filtrer les découvertes avec un haut niveau de confiance
        
        Args:
            decouvertes: Liste des résultats de détection
            
        Returns:
            Résultats avec confiance élevée
        """
        return [d for d in decouvertes if d['confiance'] in ['elevee', 'moyenne']]
    
    def dedoubler_decouvertes(self, decouvertes: List[Dict]) -> List[Dict]:
        """
        Supprimer les découvertes en double
        
        Args:
            decouvertes: Liste des résultats de détection
            
        Returns:
            Résultats sans doublons
        """
        vus = set()
        decouvertes_uniques = []
        
        for decouverte in decouvertes:
            # Utiliser le secret et le chemin du fichier comme identifiant unique
            cle = (decouverte['secret'], decouverte['chemin_fichier'])
            if cle not in vus:
                vus.add(cle)
                decouvertes_uniques.append(decouverte)
        
        return decouvertes_uniques
