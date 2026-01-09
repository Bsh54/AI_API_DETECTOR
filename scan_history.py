
"""
Module de gestion de l'historique d'analyse - Suivi des dépôts déjà analysés pour éviter les analyses répétées
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Set
from pathlib import Path


class HistoriqueAnalyse:
    """Gestionnaire de l'historique d'analyse"""
    
    def __init__(self, fichier_historique: str = None):
        """
        Initialisation du gestionnaire de l'historique d'analyse
        
        Args:
            fichier_historique: Chemin du fichier d'historique, par défaut historique_analyse/depots_analyses.json
        """
        if fichier_historique is None:
            dossier_historique = Path("historique_analyse")
            dossier_historique.mkdir(exist_ok=True)
            self.fichier_historique = dossier_historique / "depots_analyses.json"
        else:
            self.fichier_historique = Path(fichier_historique)
            self.fichier_historique.parent.mkdir(exist_ok=True, parents=True)
        
        self.historique = self._charger_historique()
    
    def _charger_historique(self) -> Dict:
        """
        Charger l'historique d'analyse depuis le fichier
        
        Returns:
            Dictionnaire de l'historique
        """
        if self.fichier_historique.exists():
            try:
                with open(self.fichier_historique, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Échec du chargement de l'historique d'analyse : {e}, création d'un nouvel historique")
                return {"depots": {}, "total_analyses": 0, "derniere_mise_a_jour": None}
        else:
            return {"depots": {}, "total_analyses": 0, "derniere_mise_a_jour": None}
    
    def _sauvegarder_historique(self):
        """Sauvegarder l'historique d'analyse dans le fichier"""
        try:
            with open(self.fichier_historique, 'w', encoding='utf-8') as f:
                json.dump(self.historique, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Échec de la sauvegarde de l'historique d'analyse : {e}")
    
    def est_analyse(self, nom_complet_depot: str) -> bool:
        """
        Vérifier si un dépôt a déjà été analysé
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            
        Returns:
            True si déjà analysé, False sinon
        """
        return nom_complet_depot in self.historique["depots"]
    
    def obtenir_infos_analyse(self, nom_complet_depot: str) -> Dict:
        """
        Obtenir les informations d'analyse d'un dépôt
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            
        Returns:
            Dictionnaire des informations d'analyse, None si non analysé
        """
        return self.historique["depots"].get(nom_complet_depot)
    
    def marquer_comme_analyse(self, nom_complet_depot: str, compte_problemes: int = 0, 
                              type_analyse: str = "inconnu"):
        """
        Marquer un dépôt comme analysé
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            compte_problemes: Nombre de problèmes détectés
            type_analyse: Type d'analyse
        """
        self.historique["depots"][nom_complet_depot] = {
            "premiere_analyse": self.historique["depots"].get(nom_complet_depot, {}).get(
                "premiere_analyse", 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ),
            "derniere_analyse": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "compte_problemes": compte_problemes,
            "type_analyse": type_analyse,
            "compte_analyses": self.historique["depots"].get(nom_complet_depot, {}).get("compte_analyses", 0) + 1
        }
        
        self.historique["total_analyses"] = len(self.historique["depots"])
        self.historique["derniere_mise_a_jour"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self._sauvegarder_historique()
    
    def obtenir_depots_analyses(self) -> List[str]:
        """
        Obtenir la liste de tous les dépôts déjà analysés
        
        Returns:
            Liste des noms complets des dépôts
        """
        return list(self.historique["depots"].keys())
    
    def obtenir_compte_analyses(self) -> int:
        """
        Obtenir le nombre total de dépôts analysés
        
        Returns:
            Nombre de dépôts
        """
        return self.historique["total_analyses"]
    
    def effacer_historique(self):
        """Effacer tout l'historique d'analyse"""
        self.historique = {"depots": {}, "total_analyses": 0, "derniere_mise_a_jour": None}
        self._sauvegarder_historique()
        print("✅ Historique d'analyse effacé")
    
    def supprimer_depot(self, nom_complet_depot: str):
        """
        Supprimer un dépôt spécifique de l'historique
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
        """
        if nom_complet_depot in self.historique["depots"]:
            del self.historique["depots"][nom_complet_depot]
            self.historique["total_analyses"] = len(self.historique["depots"])
            self.historique["derniere_mise_a_jour"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._sauvegarder_historique()
            print(f"✅ Supprimé de l'historique : {nom_complet_depot}")
        else:
            print(f"⚠️  Dépôt non trouvé dans l'historique : {nom_complet_depot}")
    
    def obtenir_statistiques(self) -> Dict:
        """
        Obtenir les statistiques d'analyse
        
        Returns:
            Dictionnaire des statistiques
        """
        total_problemes = sum(
            infos_depot.get("compte_problemes", 0) 
            for infos_depot in self.historique["depots"].values()
        )
        
        depots_avec_problemes = sum(
            1 for infos_depot in self.historique["depots"].values() 
            if infos_depot.get("compte_problemes", 0) > 0
        )
        
        return {
            "total_analyses": self.historique["total_analyses"],
            "total_problemes": total_problemes,
            "depots_avec_problemes": depots_avec_problemes,
            "derniere_mise_a_jour": self.historique["derniere_mise_a_jour"]
        }
    
    def afficher_statistiques(self):
        """Afficher les statistiques d'analyse"""
        stats = self.obtenir_statistiques()
        print(f"\n📊 Statistiques de l'historique d'analyse:")
        print(f"   Dépôts analysés au total: {stats['total_analyses']}")
        print(f"   Problèmes détectés au total: {stats['total_problemes']}")
        print(f"   Dépôts avec problèmes: {stats['depots_avec_problemes']}")
        if stats['derniere_mise_a_jour']:
            print(f"   Dernière mise à jour: {stats['derniere_mise_a_jour']}")
