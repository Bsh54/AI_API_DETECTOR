import os
import time
from datetime import datetime
from typing import List, Dict, Optional
from src.config import Config
from src.secret_detector import SecretDetector
from src.github_scanner import GitHubScanner
from src.report_generator import ReportGenerator
from src.scan_history import ScanHistory

class CloudScanner:
    """Scanner principal"""
    
    def __init__(self, github_token: str = None, skip_scanned: bool = True):
        self.config = Config()
        self.github_token = github_token or self.config.GITHUB_TOKEN
        self.skip_scanned = skip_scanned
        
        # Initialisation des composants
        self.secret_detector = SecretDetector()
        self.github_scanner = GitHubScanner(self.github_token)
        self.report_generator = ReportGenerator()
        self.scan_history = ScanHistory()
        
        # Suivi du temps
        self.scan_start_time = time.time()
        self.timeout_minutes = self.config.TIMEOUT_MINUTES
    
    def scan_ai_projects(self, max_repos: int = 50) -> str:
        """Scan automatique des projets AI"""
        print("🚀 Démarrage du scan automatique des projets AI")
        scan_start_time = datetime.now()
        
        # Définition du filtre de dépôts déjà scannés
        def is_scanned(repo_full_name: str) -> bool:
            return self.scan_history.is_scanned(repo_full_name) if self.skip_scanned else False
        
        # Recherche des dépôts AI
        repos_to_scan = self.github_scanner.search_ai_repos(
            max_repos=max_repos,
            skip_filter=is_scanned if self.skip_scanned else None
        )
        
        if not repos_to_scan:
            print("❌ Aucun dépôt AI trouvé à scanner")
            return ""
        
        # Scan de tous les dépôts
        all_findings = []
        for idx, repo in enumerate(repos_to_scan, 1):
            # Vérification du timeout
            if self._check_timeout(idx, len(repos_to_scan)):
                break
            
            print(f"🔍 [{idx}/{len(repos_to_scan)}] Scanning du dépôt: {repo['full_name']}")
            
            try:
                findings = self._scan_repository(repo, scan_type="auto:ai-projects")
                all_findings.extend(findings)
                
                # Marque comme scanné
                self.scan_history.mark_as_scanned(
                    repo['full_name'],
                    len(findings),
                    "auto:ai-projects"
                )
                
                # Petite pause pour éviter le rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Erreur lors du scan de {repo['full_name']}: {e}")
                continue
        
        # Génération du rapport
        report_path = self.report_generator.generate_report(
            all_findings, scan_start_time, scan_type="auto:ai-projects"
        )
        
        # Nettoyage de l'historique
        self.scan_history.clear_old_entries()
        
        return report_path
    
    def scan_user_repos(self, username: str, max_repos: int = 30) -> str:
        """Scan les dépôts d'un utilisateur spécifique"""
        print(f"👤 Scanning des dépôts de l'utilisateur: {username}")
        scan_start_time = datetime.now()
        
        # Récupération des dépôts de l'utilisateur
        repos = self._get_user_repos(username, max_repos)
        
        all_findings = []
        for idx, repo in enumerate(repos, 1):
            if self._check_timeout(idx, len(repos)):
                break
            
            print(f"🔍 [{idx}/{len(repos)}] Scanning: {repo['full_name']}")
            
            findings = self._scan_repository(repo, scan_type=f"user:{username}")
            all_findings.extend(findings)
            
            self.scan_history.mark_as_scanned(
                repo['full_name'],
                len(findings),
                f"user:{username}"
            )
            
            time.sleep(0.5)
        
        report_path = self.report_generator.generate_report(
            all_findings, scan_start_time, scan_type=f"user:{username}"
        )
        
        return report_path
    
    def scan_organization(self, org_name: str, max_repos: int = 50) -> str:
        """Scan les dépôts d'une organisation"""
        print(f"🏢 Scanning de l'organisation: {org_name}")
        scan_start_time = datetime.now()
        
        repos = self._get_org_repos(org_name, max_repos)
        
        all_findings = []
        for idx, repo in enumerate(repos, 1):
            if self._check_timeout(idx, len(repos)):
                break
            
            print(f"🔍 [{idx}/{len(repos)}] Scanning: {repo['full_name']}")
            
            findings = self._scan_repository(repo, scan_type=f"org:{org_name}")
            all_findings.extend(findings)
            
            self.scan_history.mark_as_scanned(
                repo['full_name'],
                len(findings),
                f"org:{org_name}"
            )
            
            time.sleep(0.5)
        
        report_path = self.report_generator.generate_report(
            all_findings, scan_start_time, scan_type=f"org:{org_name}"
        )
        
        return report_path
    
    def scan_single_repo(self, repo_full_name: str) -> str:
        """Scan un dépôt unique"""
        print(f"📦 Scanning du dépôt unique: {repo_full_name}")
        scan_start_time = datetime.now()
        
        owner, repo_name = repo_full_name.split('/')
        repo_data = {
            'full_name': repo_full_name,
            'owner': {'login': owner},
            'name': repo_name
        }
        
        findings = self._scan_repository(repo_data, scan_type="single")
        
        report_path = self.report_generator.generate_report(
            findings, scan_start_time, scan_type=f"repo:{repo_full_name}"
        )
        
        return report_path
    
    def _scan_repository(self, repo: Dict, scan_type: str = "manual") -> List[Dict]:
        """Scan un dépôt GitHub"""
        owner = repo['owner']['login']
        repo_name = repo['name']
        repo_full_name = repo['full_name']
        
        print(f"   📁 Analyse de la structure du dépôt...")
        
        # Récupération de tous les fichiers
        files_to_scan = self._get_all_files(owner, repo_name)
        
        findings = []
        scanned_files = 0
        
        for file_path in files_to_scan:
            # Vérifie si c'est un fichier à scanner
            if not self._should_scan_file(file_path):
                continue
            
            try:
                # Récupère le contenu du fichier
                content = self.github_scanner.get_file_content(owner, repo_name, file_path)
                if content:
                    # Détecte les secrets
                    file_findings = self.secret_detector.detect_secrets_in_text(content, file_path)
                    
                    for finding in file_findings:
                        finding.update({
                            'repo_url': f"https://github.com/{repo_full_name}",
                            'repo_name': repo_full_name,
                            'scan_type': scan_type
                        })
                        findings.append(finding)
                    
                    scanned_files += 1
                    
            except Exception as e:
                print(f"   ⚠️ Erreur avec le fichier {file_path}: {e}")
                continue
        
        print(f"   ✅ Scanné {scanned_files} fichiers, trouvé {len(findings)} problèmes")
        return findings
    
    def _get_all_files(self, owner: str, repo_name: str, path: str = "") -> List[str]:
        """Récupère récursivement tous les fichiers d'un dépôt"""
        all_files = []
        
        try:
            contents = self.github_scanner.get_repo_contents(owner, repo_name, path)
            
            for item in contents:
                if item['type'] == 'file':
                    all_files.append(item['path'])
                elif item['type'] == 'dir':
                    dir_name = item['name']
                    
                    # Vérifie si c'est un répertoire à exclure
                    if dir_name in self.config.EXCLUDE_DIRS or \
                       any(dir_name.startswith(exclude) for exclude in self.config.EXCLUDE_DIRS):
                        continue
                    
                    # Scan récursif
                    sub_files = self._get_all_files(owner, repo_name, item['path'])
                    all_files.extend(sub_files)
        
        except Exception as e:
            print(f"   ⚠️ Erreur lors de la récupération des fichiers: {e}")
        
        return all_files
    
    def _should_scan_file(self, file_path: str) -> bool:
        """Détermine si un fichier doit être scanné"""
        # Vérifie l'extension
        has_valid_extension = any(file_path.endswith(ext) for ext in self.config.SCAN_EXTENSIONS)
        if not has_valid_extension:
            return False
        
        # Vérifie les répertoires exclus
        for exclude_dir in self.config.EXCLUDE_DIRS:
            if f"/{exclude_dir}/" in file_path or file_path.startswith(f"{exclude_dir}/"):
                return False
        
        # Vérifie les fichiers exclus
        for exclude_pattern in self.config.EXCLUDE_FILES:
            if exclude_pattern.startswith('*'):
                if file_path.endswith(exclude_pattern[1:]):
                    return False
            elif exclude_pattern in file_path:
                return False
        
        return True
    
    def _get_user_repos(self, username: str, max_repos: int) -> List[Dict]:
        """Récupère les dépôts d'un utilisateur"""
        url = f"{self.config.GITHUB_API_URL}/users/{username}/repos"
        params = {
            'type': 'all',
            'sort': 'updated',
            'per_page': min(max_repos, 100)
        }
        
        response = requests.get(url, headers=self.github_scanner.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur lors de la récupération des dépôts de {username}: {response.status_code}")
            return []
    
    def _get_org_repos(self, org_name: str, max_repos: int) -> List[Dict]:
        """Récupère les dépôts d'une organisation"""
        url = f"{self.config.GITHUB_API_URL}/orgs/{org_name}/repos"
        params = {
            'type': 'all',
            'sort': 'updated',
            'per_page': min(max_repos, 100)
        }
        
        response = requests.get(url, headers=self.github_scanner.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur lors de la récupération des dépôts de {org_name}: {response.status_code}")
            return []
    
    def _check_timeout(self, current_idx: int, total_repos: int) -> bool:
        """Vérifie si le timeout est atteint"""
        elapsed_minutes = (time.time() - self.scan_start_time) / 60
        
        if elapsed_minutes >= self.timeout_minutes:
            print(f"⏰ Timeout atteint ({elapsed_minutes:.1f} minutes)")
            print(f"📊 Progression: {current_idx}/{total_repos} dépôts scannés")
            print("💾 Les données sont sauvegardées, reprise au prochain scan")
            return True
        
        return False