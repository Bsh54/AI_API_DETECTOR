
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from github import Github, GithubException
from config import GITHUB_TOKEN, MOTS_CLES_RECHERCHE_IA, DEPOTS_MAX_PAR_RECHERCHE, DELAI_RECHERCHE_SECONDES


class ScannerGitHub:
    """Scanner de dépôts GitHub"""
    
    def __init__(self, token: str = GITHUB_TOKEN):
        """
        Initialisation du scanner GitHub
        
        Args:
            token: GitHub Personal Access Token
        """
        if not token:
            raise ValueError("Token GitHub requis. Veuillez définir GITHUB_TOKEN dans le fichier .env")
        
        # Configuration des délais d'expiration et des tentatives pour éviter les longues attentes
        self.github = Github(
            token,
            timeout=30,  # Délai d'expiration de 30 secondes
            retry=None   # Désactive les tentatives automatiques, nous les gérons nous-mêmes
        )
        self.restant_limite_taux = None
        self.reinitialisation_limite_taux = None
        
    def obtenir_infos_limite_taux(self) -> Dict:
        """Obtenir les informations de limite de taux de l'API"""
        limite_taux = self.github.get_rate_limit()
        noyau = limite_taux.core
        
        return {
            'restant': noyau.remaining,
            'limite': noyau.limit,
            'reinitialisation': noyau.reset
        }
    
    def attendre_limite_taux(self):
        """Attendre la réinitialisation de la limite de taux"""
        infos = self.obtenir_infos_limite_taux()
        if infos['restant'] < 10:
            # infos['reinitialisation'] est un objet datetime, doit être comparé à datetime.now()
            temps_attente = (infos['reinitialisation'] - datetime.now()).total_seconds() + 10
            print(f"⚠️  Limite de taux d'API presque épuisée, attente de {temps_attente:.0f} secondes...")
            time.sleep(max(0, temps_attente))
    
    def obtenir_depots_utilisateur(self, nom_utilisateur: str) -> List[Dict]:
        """
        Obtenir tous les dépôts publics d'un utilisateur spécifique
        
        Args:
            nom_utilisateur: Nom d'utilisateur GitHub
            
        Returns:
            Liste d'informations sur les dépôts
        """
        try:
            utilisateur = self.github.get_user(nom_utilisateur)
            depots = []
            
            for depot in utilisateur.get_repos():
                if not depot.private:
                    depots.append({
                        'nom': depot.name,
                        'nom_complet': depot.full_name,
                        'url': depot.html_url,
                        'url_clone': depot.clone_url,
                        'description': depot.description,
                        'maj_le': depot.updated_at,
                    })
            
            return depots
        except GithubException as e:
            print(f"❌ Échec de récupération des dépôts utilisateur : {e}")
            return []
    
    def obtenir_depots_organisation(self, nom_organisation: str) -> List[Dict]:
        """
        Obtenir tous les dépôts publics d'une organisation spécifique
        
        Args:
            nom_organisation: Nom de l'organisation GitHub
            
        Returns:
            Liste d'informations sur les dépôts
        """
        try:
            organisation = self.github.get_organization(nom_organisation)
            depots = []
            
            for depot in organisation.get_repos():
                if not depot.private:
                    depots.append({
                        'nom': depot.name,
                        'nom_complet': depot.full_name,
                        'url': depot.html_url,
                        'url_clone': depot.clone_url,
                        'description': depot.description,
                        'maj_le': depot.updated_at,
                    })
            
            return depots
        except GithubException as e:
            print(f"❌ Échec de récupération des dépôts organisation : {e}")
            return []
    
    def rechercher_depots_ia(self, depots_max: int = DEPOTS_MAX_PAR_RECHERCHE, filtre_ignore=None) -> List[Dict]:
        """
        Rechercher des projets GitHub liés à l'IA
        
        Args:
            depots_max: Nombre maximum de dépôts à retourner
            filtre_ignore: Fonction de filtrage optionnelle, accepte le nom complet du dépôt, retourne True pour ignorer ce dépôt
            
        Returns:
            Liste d'informations sur les dépôts
        """
        tous_depots = []
        depots_vus = set()
        compte_ignores = 0
        
        for mot_cle in MOTS_CLES_RECHERCHE_IA:
            try:
                print(f"🔍 Recherche du mot-clé : {mot_cle}")
                self.attendre_limite_taux()
                
                # Recherche de code
                requete = f'{mot_cle} in:file language:python'
                resultats = self.github.search_code(requete, order='desc')
                
                # Extraire les dépôts à partir des résultats de recherche de code
                for code in resultats:
                    # Arrêter la recherche si suffisamment de dépôts ont été trouvés
                    if len(tous_depots) >= depots_max:
                        break
                    
                    depot = code.repository
                    
                    # Ignorer les dépôts privés et ceux déjà vus
                    if depot.private or depot.full_name in depots_vus:
                        continue
                    
                    depots_vus.add(depot.full_name)
                    
                    # Vérifier si le dépôt doit être ignoré si une fonction de filtrage est fournie
                    if filtre_ignore and filtre_ignore(depot.full_name):
                        compte_ignores += 1
                        print(f"  ⏭️  Ignorer déjà analysé : {depot.full_name}")
                        continue  # Ne pas compter, continuer avec le suivant
                    
                    # Ajouter à la liste des résultats
                    tous_depots.append({
                        'nom': depot.name,
                        'nom_complet': depot.full_name,
                        'url': depot.html_url,
                        'url_clone': depot.clone_url,
                        'description': depot.description,
                        'maj_le': depot.updated_at,
                    })
                
                # Délai pour éviter de déclencher la limite de taux
                time.sleep(DELAI_RECHERCHE_SECONDES)
                
                if len(tous_depots) >= depots_max:
                    print(f"✅ {len(tous_depots)} dépôts non analysés trouvés ({compte_ignores} déjà analysés ignorés)")
                    break
                    
            except GithubException as e:
                print(f"⚠️  Erreur lors de la recherche '{mot_cle}' : {e}")
                continue
        
        if compte_ignores > 0 and len(tous_depots) < depots_max:
            print(f"ℹ️  {len(tous_depots)} dépôts non analysés trouvés ({compte_ignores} déjà analysés ignorés)")
        
        return tous_depots
    
    def obtenir_fichiers_depot(self, nom_complet_depot: str, chemin: str = "") -> List[Dict]:
        """
        Obtenir la liste des fichiers dans un dépôt
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            chemin: Chemin du fichier
            
        Returns:
            Liste d'informations sur les fichiers
        """
        try:
            depot = self.github.get_repo(nom_complet_depot)
            contenus = depot.get_contents(chemin)
            
            fichiers = []
            for contenu in contenus:
                if contenu.type == "dir":
                    # Récupération récursive des fichiers des sous-répertoires
                    fichiers.extend(self.obtenir_fichiers_depot(nom_complet_depot, contenu.path))
                else:
                    fichiers.append({
                        'chemin': contenu.path,
                        'nom': contenu.name,
                        'url_telechargement': contenu.download_url,
                        'sha': contenu.sha,
                    })
            
            return fichiers
        except GithubException as e:
            # Erreur 403 ignorée directement, sans attente
            if e.status == 403:
                print(f"  ⏭️  Ignorer : accès non autorisé (403 Forbidden)")
            else:
                print(f"⚠️  Échec de récupération de la liste des fichiers : {e}")
            return []
    
    def obtenir_contenu_fichier(self, nom_complet_depot: str, chemin_fichier: str) -> Optional[str]:
        """
        Obtenir le contenu d'un fichier
        
        Args:
            nom_complet_depot: Nom complet du dépôt (proprietaire/depot)
            chemin_fichier: Chemin du fichier
            
        Returns:
            Contenu du fichier (texte)
        """
        try:
            depot = self.github.get_repo(nom_complet_depot)
            contenu = depot.get_contents(chemin_fichier)
            
            # Décoder le contenu
            try:
                return contenu.decoded_content.decode('utf-8')
            except UnicodeDecodeError:
                # Si c'est un fichier binaire, retourner None
                return None
        except GithubException as e:
            # Erreur 403 ignorée directement, sans affichage d'erreur
            if e.status == 403:
                pass  # Ignorer silencieusement
            return None
