
"""
Module principal du scanner - Intègre toutes les fonctionnalités
"""
import time
from datetime import datetime
from typing import List, Dict, Optional
from github_scanner import ScannerGitHub
from secret_detector import DetecteurSecret
from report_generator import GenerateurRapport
from scan_history import HistoriqueAnalyse


class CloudScanner:
    """Scanner cloud - Logique d'analyse principale"""
    
    def __init__(self, token_github: str, sauter_analyses: bool = True, timeout_minutes: int = 50):
        """
        Initialisation du scanner
        
        Args:
            token_github: GitHub Personal Access Token
            sauter_analyses: Ignorer les dépôts déjà analysés (par défaut: True)
            timeout_minutes: Délai d'expiration de l'analyse (minutes), par défaut 50 minutes
        """
        self.scanner_github = ScannerGitHub(token_github)
        self.detecteur_secret = DetecteurSecret()
        self.generateur_rapport = GenerateurRapport()
        self.historique_analyse = HistoriqueAnalyse()
        self.sauter_analyses = sauter_analyses
        self.timeout_secondes = timeout_minutes * 60
        self.heure_debut_analyse = None
    
    def _est_timeout(self) -> bool:
        """Vérifier si le délai d'expiration est atteint"""
        if self.heure_debut_analyse is None:
            return False
        ecoule = time.time() - self.heure_debut_analyse
        return ecoule >= self.timeout_secondes
    
    def _verifier_timeout(self, idx_actuel: int, total_depots: int) -> bool:
        """
        Vérifier si le délai d'expiration est atteint, afficher un message si c'est le cas et retourner True
        
        Args:
            idx_actuel: Index du dépôt actuellement en cours d'analyse
            total_depots: Nombre total de dépôts
            
        Returns:
            Si le délai d'expiration est atteint
        """
        if self._est_timeout():
            minutes_ecoulees = (time.time() - self.heure_debut_analyse) / 60
            print(f"\n⏰ Délai d'expiration de l'analyse atteint (exécution pendant {minutes_ecoulees:.1f} minutes)")
            print(f"✅ {idx_actuel}/{total_depots} dépôts analysés")
            print(f"💾 Données d'analyse précédentes enregistrées, {total_depots - idx_actuel} dépôts restants seront traités lors de la prochaine analyse")
            return True
        return False
    
    def analyser_utilisateur(self, nom_utilisateur: str) -> str:
        """
        Analyser tous les dépôts publics d'un utilisateur spécifique
        
        Args:
            nom_utilisateur: Nom d'utilisateur GitHub
            
        Returns:
            Chemin du fichier de rapport
        """
        print(f"🚀 Début de l'analyse de l'utilisateur : {nom_utilisateur}")
        heure_debut_analyse = datetime.now()
        self.heure_debut_analyse = time.time()  # Démarrer le chronomètre
        
        # Obtenir tous les dépôts de l'utilisateur
        depots = self.scanner_github.obtenir_depots_utilisateur(nom_utilisateur)
        print(f"📦 {len(depots)} dépôts publics trouvés")
        
        # Filtrer les dépôts déjà analysés
        depots_a_analyser, compte_ignores = self._filtrer_depots_analyses(depots)
        if compte_ignores > 0:
            print(f"⏭️  {compte_ignores} dépôts déjà analysés ignorés")
            print(f"📦 {len(depots_a_analyser)} nouveaux dépôts à analyser")
        
        # Analyser tous les dépôts
        toutes_decouvertes = []
        for idx, depot in enumerate(depots_a_analyser, 1):
            # Vérifier le délai d'expiration
            if self._verifier_timeout(idx - 1, len(depots_a_analyser)):
                break
            
            print(f"🔍 [{idx}/{len(depots_a_analyser)}] Analyse du dépôt : {depot['nom_complet']}")
            decouvertes = self._analyser_depot(depot, type_analyse=f"utilisateur:{nom_utilisateur}")
            toutes_decouvertes.extend(decouvertes)
        
        # Générer le rapport
        print(f"\n📝 Génération du rapport...")
        chemin_rapport = self.generateur_rapport.generer_rapport(
            toutes_decouvertes, 
            heure_debut_analyse,
            type_analyse=f"utilisateur:{nom_utilisateur}"
        )
        
        # Afficher le résumé
        resume = self.generateur_rapport.generer_resume(chemin_rapport, len(toutes_decouvertes))
        print(resume)
        
        return chemin_rapport
    
    def analyser_organisation(self, nom_organisation: str) -> str:
        """
        Analyser tous les dépôts publics d'une organisation spécifique
        
        Args:
            nom_organisation: Nom de l'organisation GitHub
            
        Returns:
            Chemin du fichier de rapport
        """
        print(f"🚀 Début de l'analyse de l'organisation : {nom_organisation}")
        heure_debut_analyse = datetime.now()
        self.heure_debut_analyse = time.time()  # Démarrer le chronomètre
        
        # Obtenir tous les dépôts de l'organisation
        depots = self.scanner_github.obtenir_depots_organisation(nom_organisation)
        print(f"📦 {len(depots)} dépôts publics trouvés")
        
        # Filtrer les dépôts déjà analysés
        depots_a_analyser, compte_ignores = self._filtrer_depots_analyses(depots)
        if compte_ignores > 0:
            print(f"⏭️  {compte_ignores} dépôts déjà analysés ignorés")
            print(f"📦 {len(depots_a_analyser)} nouveaux dépôts à analyser")
        
        # Analyser tous les dépôts
        toutes_decouvertes = []
        for idx, depot in enumerate(depots_a_analyser, 1):
            # Vérifier le délai d'expiration
            if self._verifier_timeout(idx - 1, len(depots_a_analyser)):
                break
            
            print(f"🔍 [{idx}/{len(depots_a_analyser)}] Analyse du dépôt : {depot['nom_complet']}")
            decouvertes = self._analyser_depot(depot, type_analyse=f"organisation:{nom_organisation}")
            toutes_decouvertes.extend(decouvertes)
        
        # Générer le rapport
        print(f"\n📝 Génération du rapport...")
        chemin_rapport = self.generateur_rapport.generer_rapport(
            toutes_decouvertes,
            heure_debut_analyse,
            type_analyse=f"organisation:{nom_organisation}"
        )
        
        # Afficher le résumé
        resume = self.generateur_rapport.generer_resume(chemin_rapport, len(toutes_decouvertes))
        print(resume)
        
        return chemin_rapport
    
    def analyser_projets_ia(self, depots_max: int = 50) -> str:
        """
        Recherche et analyse automatique de projets liés à l'IA
        
        Args:
            depots_max: Nombre maximum de dépôts à analyser
            
        Returns:
            Chemin du fichier de rapport
        """
        print(f"🚀 Début de la recherche automatique de projets liés à l'IA")
        print(f"🎯 Objectif : trouver et analyser {depots_max} dépôts non encore analysés")
        heure_debut_analyse = datetime.now()
        self.heure_debut_analyse = time.time()  # Démarrer le chronomètre
        
        # Définir la fonction de filtrage : vérifier si le dépôt est déjà analysé
        def est_analyse(nom_complet_depot: str) -> bool:
            return self.historique_analyse.est_analyse(nom_complet_depot)
        
        # Rechercher des dépôts, avec filtrage en temps réel des dépôts déjà analysés
        # Le processus de recherche ignore automatiquement les dépôts déjà analysés jusqu'à trouver suffisamment de nouveaux dépôts
        depots_a_analyser = self.scanner_github.rechercher_depots_ia(
            depots_max=depots_max,
            filtre_ignore=est_analyse if self.sauter_analyses else None
        )
        
        print(f"📦 {len(depots_a_analyser)} dépôts à analyser trouvés")
        
        # Analyser tous les dépôts
        toutes_decouvertes = []
        for idx, depot in enumerate(depots_a_analyser, 1):
            # Vérifier le délai d'expiration
            if self._verifier_timeout(idx - 1, len(depots_a_analyser)):
                break
            
            print(f"🔍 [{idx}/{len(depots_a_analyser)}] Analyse du dépôt : {depot['nom_complet']}")
            decouvertes = self._analyser_depot(depot, type_analyse="auto:projets-ia")
            toutes_decouvertes.extend(decouvertes)
        
        # Générer le rapport
        print(f"\n📝 Génération du rapport...")
        chemin_rapport = self.generateur_rapport.generer_rapport(
            toutes_decouvertes,
            heure_debut_analyse,
            type_analyse="auto:projets-ia"
        )
        
        # Afficher le résumé
        resume = self.generateur_rapport.generer_resume(chemin_rapport, len(toutes_decouvertes))
        print(resume)
        
        return chemin_rapport
    
    def analyser_depot_unique(self, nom_complet_depot: str) -> str:
        """
        Analyser un seul dépôt
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            
        Returns:
            Chemin du fichier de rapport
        """
        print(f"🚀 Début de l'analyse du dépôt : {nom_complet_depot}")
        heure_debut_analyse = datetime.now()
        
        # Construire les informations du dépôt
        infos_depot = {
            'nom_complet': nom_complet_depot,
            'url': f"https://github.com/{nom_complet_depot}",
            'url_clone': f"https://github.com/{nom_complet_depot}.git",
        }
        
        # Analyser le dépôt
        decouvertes = self._analyser_depot(infos_depot)
        
        # Générer le rapport
        print(f"\n📝 Génération du rapport...")
        chemin_rapport = self.generateur_rapport.generer_rapport(
            decouvertes,
            heure_debut_analyse,
            type_analyse=f"unique:{nom_complet_depot}"
        )
        
        # Afficher le résumé
        resume = self.generateur_rapport.generer_resume(chemin_rapport, len(decouvertes))
        print(resume)
        
        return chemin_rapport
    
    def _filtrer_depots_analyses(self, depots: List[Dict]) -> tuple:
        """
        Filtrer les dépôts déjà analysés
        
        Args:
            depots: Liste des dépôts
            
        Returns:
            (Liste des dépôts à analyser, Nombre de dépôts ignorés)
        """
        if not self.sauter_analyses:
            return depots, 0
        
        depots_a_analyser = []
        compte_ignores = 0
        
        for depot in depots:
            nom_depot = depot.get('nom_complet', '')
            if self.historique_analyse.est_analyse(nom_depot):
                compte_ignores += 1
            else:
                depots_a_analyser.append(depot)
        
        return depots_a_analyser, compte_ignores
    
    def _analyser_depot(self, depot: Dict, type_analyse: str = "inconnu") -> List[Dict]:
        """
        Analyser un seul dépôt
        
        Args:
            depot: Dictionnaire des informations du dépôt
            type_analyse: Type d'analyse
            
        Returns:
            Liste des informations sensibles découvertes
        """
        decouvertes = []
        heure_analyse = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nom_depot = depot.get('nom_complet', 'inconnu')
        
        try:
            # Obtenir la liste des fichiers du dépôt
            fichiers = self.scanner_github.obtenir_fichiers_depot(depot['nom_complet'])
            
            # Si l'obtention de la liste des fichiers échoue (par exemple erreur 403), retourner directement
            if not fichiers:
                # Enregistrer dans l'historique d'analyse pour éviter de l'analyser à nouveau
                self.historique_analyse.marquer_comme_analyse(nom_depot, 0, f"{type_analyse}:pas-acces")
                return decouvertes
            
            # Analyser chaque fichier
            for infos_fichier in fichiers:
                # Vérifier si ce fichier doit être analysé
                if not self.detecteur_secret.devrait_analyser_fichier(infos_fichier['chemin']):
                    continue
                
                # Obtenir le contenu du fichier
                contenu = self.scanner_github.obtenir_contenu_fichier(
                    depot['nom_complet'],
                    infos_fichier['chemin']
                )
                
                if contenu:
                    # Détecter les informations sensibles
                    secrets = self.detecteur_secret.detecter_secrets_dans_texte(
                        contenu,
                        infos_fichier['chemin']
                    )
                    
                    # Ajouter les informations du dépôt
                    for secret in secrets:
                        secret['url_depot'] = depot.get('url', f"https://github.com/{nom_depot}")
                        secret['nom_depot'] = depot['nom_complet']
                        secret['heure_analyse'] = heure_analyse
                        decouvertes.append(secret)
            
            # Déduplication et filtrage
            decouvertes = self.detecteur_secret.dedoubler_decouvertes(decouvertes)
            decouvertes = self.detecteur_secret.filtrer_confiance_elevee(decouvertes)
            
            if decouvertes:
                print(f"  ⚠️  {len(decouvertes)} problème(s) potentiel(s) détecté(s)")
            else:
                print(f"  ✅ Aucun problème apparent détecté")
            
            # Enregistrer dans l'historique d'analyse
            self.historique_analyse.marquer_comme_analyse(nom_depot, len(decouvertes), type_analyse)
                
        except Exception as e:
            msg_erreur = str(e)
            # Traitement silencieux des erreurs 403
            if "403" in msg_erreur or "Forbidden" in msg_erreur:
                print(f"  ⏭️  Ignorer : accès non autorisé")
                self.historique_analyse.marquer_comme_analyse(nom_depot, 0, f"{type_analyse}:interdit")
            else:
                print(f"  ❌ Échec de l'analyse : {e}")
                # Même en cas d'échec de l'analyse, enregistrer pour éviter de réessayer
                self.historique_analyse.marquer_comme_analyse(nom_depot, 0, f"{type_analyse}:echec")
        
        return decouvertes
