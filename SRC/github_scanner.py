import requests
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .config import Config

class GitHubScanner:
    """Scanner GitHub"""
    
    def __init__(self, github_token: str = None):
        self.config = Config()
        self.token = github_token or self.config.GITHUB_TOKEN
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_base = self.config.GITHUB_API_URL
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = datetime.now()
    
    def search_ai_repos(self, max_repos: int = 50, skip_filter: callable = None) -> List[Dict]:
        """Recherche les dépôts liés à l'IA"""
        print("🔍 Recherche des dépôts AI...")
        
        search_queries = [
            'openai api', 'langchain', 'llm', 'large language model',
            'chatgpt', 'anthropic', 'claude', 'gemini ai',
            'machine learning', 'deep learning', 'ai project',
            'transformers', 'huggingface', 'llama', 'gpt-4'
        ]
        
        all_repos = []
        seen_repos = set()
        
        for query in search_queries:
            if len(all_repos) >= max_repos:
                break
            
            try:
                repos = self._search_repositories(query, max_repos - len(all_repos))
                for repo in repos:
                    repo_full_name = repo['full_name']
                    
                    # Évite les doublons
                    if repo_full_name in seen_repos:
                        continue
                    
                    # Applique le filtre de skip
                    if skip_filter and skip_filter(repo_full_name):
                        continue
                    
                    all_repos.append(repo)
                    seen_repos.add(repo_full_name)
                    
                    if len(all_repos) >= max_repos:
                        break
                
                time.sleep(1)  # Respect du rate limiting
                
            except Exception as e:
                print(f"⚠️ Erreur lors de la recherche avec '{query}': {e}")
                continue
        
        print(f"✅ Trouvé {len(all_repos)} dépôts AI")
        return all_repos
    
    def _search_repositories(self, query: str, per_page: int = 30) -> List[Dict]:
        """Exécute une recherche GitHub"""
        url = f"{self.api_base}/search/repositories"
        params = {
            'q': query,
            'sort': 'updated',
            'order': 'desc',
            'per_page': min(per_page, 100)
        }
        
        self._check_rate_limit()
        response = requests.get(url, headers=self.headers, params=params)
        self._update_rate_limit(response.headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            print(f"❌ Erreur API GitHub: {response.status_code}")
            return []
    
    def get_repo_contents(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        """Récupère le contenu d'un dépôt"""
        url = f"{self.api_base}/repos/{owner}/{repo}/contents/{path}"
        
        self._check_rate_limit()
        response = requests.get(url, headers=self.headers)
        self._update_rate_limit(response.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur lors de la récupération du contenu: {response.status_code}")
            return []
    
    def get_file_content(self, owner: str, repo: str, file_path: str) -> Optional[str]:
        """Récupère le contenu d'un fichier"""
        url = f"{self.api_base}/repos/{owner}/{repo}/contents/{file_path}"
        
        self._check_rate_limit()
        response = requests.get(url, headers=self.headers)
        self._update_rate_limit(response.headers)
        
        if response.status_code == 200:
            content_data = response.json()
            if content_data.get('encoding') == 'base64':
                import base64
                content = base64.b64decode(content_data['content']).decode('utf-8')
                return content
        else:
            print(f"❌ Erreur lors de la récupération du fichier {file_path}: {response.status_code}")
        
        return None
    
    def _check_rate_limit(self):
        """Vérifie et respecte les limites de rate limiting"""
        if self.rate_limit_remaining < 10:
            reset_time = datetime.fromtimestamp(self.rate_limit_reset)
            now = datetime.now()
            
            if reset_time > now:
                wait_seconds = (reset_time - now).total_seconds() + 1
                print(f"⏳ Attente de {wait_seconds:.0f} secondes (rate limit)...")
                time.sleep(wait_seconds)
    
    def _update_rate_limit(self, headers: Dict):
        """Met à jour les informations de rate limiting"""
        if 'X-RateLimit-Remaining' in headers:
            self.rate_limit_remaining = int(headers['X-RateLimit-Remaining'])
        
        if 'X-RateLimit-Reset' in headers:
            self.rate_limit_reset = int(headers['X-RateLimit-Reset'])